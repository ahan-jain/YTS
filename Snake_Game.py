import pygame
import random
import numpy as np
import serial

pygame.init()
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake game')
FPS=25
fpsClock=pygame.time.Clock()

background_color = (0,139,0)
snake_color=(0,0,255)
snake_mouth = [200,150]
snake_height = 20
snake_width = 20
display.fill(background_color)
game_over = False
SPEED = 5
snake=[]
direction_list=[]
snake.append(snake_mouth)

#variable decl
data = []

turn_dict={}
turn_dict[(1,1)]=4
turn_dict[(1,-1)]=3
turn_dict[(2,1)]=1
turn_dict[(2,-1)]=2

count =0
queue = []
queuesize = 100
windowSize = 50
alpha = 0.2
x_axis_g = 0
y_axis_g = 0
z_axis_g = 0

smallCnt=10


'''
1:left
2:right
3:up
4:down
'''
#serial port config
s = serial.Serial('COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False,
                  rtscts=False)
#serial port open
if not s.isOpen():
    print("was closed")
    s.open()

direction = 2

direction_list.append(direction)

def update_snake(new_snake_mouth,snake):
    if (new_snake_mouth[0] < 0):
        new_snake_mouth[0] = width
    if (new_snake_mouth[1] < 0):
        new_snake_mouth[1] = height
    if (new_snake_mouth[0] > width):
        new_snake_mouth[0] = 0
    if (new_snake_mouth[1] > height):
        new_snake_mouth[1] = 0

    new_snake=[]

    new_snake.append(new_snake_mouth)
    for i in range(len(snake)-1):
        new_snake.append(snake[i])
    return new_snake

def move_cell(direction,posn):
    new_x = posn[0]
    new_y = posn[1]
    if direction == 1:
        new_x -= SPEED
    if direction == 2:
        new_x += SPEED
    if direction == 3:
        new_y -= SPEED
    if direction == 4:
        new_y += SPEED
    return [new_x,new_y]

def move(direction,snake):
    updated_mouth = move_cell(direction,snake[0])
    return update_snake(updated_mouth,snake)

food_color = (139,0,0)
def add_food():
    food_x =random.randint(50,width-50)
    food_y =random.randint(50,height-50)
    return [food_x,food_y]

food_posn = add_food()

def update_food(snake,direction_list,direction):
    last_block = snake[-1]
    if direction == 1:
        new_block = [last_block[0] + snake_width, last_block[1]]
    if direction == 2:
        new_block = [last_block[0] - snake_width, last_block[1]]
    if direction == 3:
        new_block = [last_block[0], last_block[1] + snake_height]
    if direction == 4:
        new_block = [last_block[0], last_block[1] - snake_height]
    snake.append(new_block)
    direction_list.append(direction)
    return snake,direction_list


def is_food_present(snake,food_posn):
    snake_mouth = snake[0]
    snake_mouth_center = [snake_mouth[0],snake_mouth[1]]
    distance = ((food_posn[0]-snake_mouth_center[0])**2 + (food_posn[1]-snake_mouth_center[1])**2)**0.5
    print(snake_mouth)
    if distance<25:
        return False
    else:
        return True
#fun process
def processRawData(adc_value,g):
    # g_value = ( ( ((adc_value * 5)/1024) - 1.65 ) / 0.330 )
    g_value = adc_value
    processValue= (g_value * alpha + (g * (1.0-alpha)))
    return processValue

def get_dir_axis(window):
    max = window.max()
    min = window.min()
    min_ind = window.argmin()
    max_ind = window.argmax()
    diff = abs(max-min)
    if(diff>150):
        if(min_ind<max_ind):
            return 1,diff
        else:
            return -1,diff
    else:
        return 0,0

res = s.readline()
while not game_over:
    display.fill(background_color)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

    #integration point
    #read data

    res = s.readline()
    res = (res.rstrip()).lstrip()
    res = res.decode("utf-8")
    data = res.split(",")

    if len(data) == 0:
        continue
    data = [int(x) for x in data]

    data[0]=processRawData(data[0],x_axis_g)
    x_axis_g= data[0]
    data[1]=processRawData(data[1],y_axis_g)
    y_axis_g = data[1]
    data[2]=processRawData(data[2],z_axis_g)
    z_axis_g = data[2]

    #store in array
    print(len(queue), "queue length")
    queue.append(data)
    if (len(queue) > queuesize):
        print(data, "data")
        queue.pop(0)
        if (count % smallCnt == 0):
            windowData = np.array(queue[0:windowSize])
            print(windowData.shape)
            diff_max = -1
            turn = -1
            dir_sense_turn = -1
            for axis in range(1, 3):
                dir_sense, diff = get_dir_axis(windowData[:, axis])
                if (dir_sense != 0):
                    if (diff_max < diff):
                        diff_max = diff
                        turn = axis
                        dir_sense_turn = dir_sense
            if (turn != -1):
                print(turn_dict[(turn, dir_sense_turn)])
                queue = queue[windowSize+1:]
                direction = turn_dict[(turn, dir_sense_turn)]
            else:
                queue= queue[windowSize+1:]


    # integration point
    snake = move(direction,snake)
    #print(snake)
    is_food= is_food_present(snake,food_posn)
    #print('is_food_present:',is_food)
    if (is_food):
        pygame.draw.circle(display, food_color, food_posn, 10)
    else:
        snake,direction_list = update_food(snake,direction_list,direction)
        food_posn = add_food()
    for snake_posn in snake:
        pygame.draw.rect(display, snake_color, [snake_posn[0]-int(snake_width/2), snake_posn[1]-int(snake_height/2), snake_width, snake_height])
    pygame.draw.rect(display, [255,255,255],[snake[0][0], snake[0][1], 2, 2])

    if(not is_food):
        print(snake)
    pygame.display.update()
    #fpsClock.tick(FPS)

pygame.quit()
quit()
