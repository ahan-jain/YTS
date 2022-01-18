'''
Level 3&4: Taking input from user (W,A,S,D).
         Display error if user inputs anything other than W,A,S,D.
         In the end, finally modifying it to make it a fully functioning game.
'''
import numpy as np
import random
pos = 10
maze = np.zeros((pos,pos), dtype = int)
for rows in range(pos):
    for columns in range(pos):
        a = random.randint(0,10)
        if 0<=a<=6:
            maze[rows,columns]= 0
        elif 7<=a<=10:
            maze[rows,columns]= 1
print("\n",maze)
start_row = (random.randint(1, 10))-1
start_col = (random.randint(1, 10))-1
end_row = (random.randint(1, 10))-1
end_col = (random.randint(1, 10))-1
while(1):
   if (start_col == end_col and start_row == end_row):
       start_row = (random.randint(1, 10)) - 1
       start_col = (random.randint(1, 10)) - 1
       end_row = (random.randint(1, 10)) - 1
       end_col = (random.randint(1, 10)) - 1
   else:
       break
print("\n Starting point is row", start_row + 1, ", column ", start_col + 1)
maze[start_row, start_col] = 5

print("\n Ending is row", end_row + 1, ", column ", end_col + 1)
maze[end_row, end_col] = 5
print ("\n",maze)
print("Enter W,A,S,D to move, X to exit")
try:
    while (1):
        x = input("What would you like to do?: ")
        if x == "W" or x == "w":
            start_row -= 1
            if (maze[start_row, start_col] == 1):
                print("game over, you hit the wall")
                break
            elif (maze[start_row, start_col] == 5):
                print("You've reached the end! GG")
                break
            else:
                maze[start_row, start_col] = 5
                maze[start_row + 1, start_col] = 0
                print("\n", maze)
                continue
        elif x == "A" or x == "a":
            start_col -= 1
            if (maze[start_row, start_col] == 1):
                print("game over, you hit the wall")
                break
            elif (maze[start_row, start_col] == 5):
                print("You've reached the end! GG")
                break
            else:
                maze[start_row, start_col] = 5
                maze[start_row, start_col + 1] = 0
                print("\n", maze)
                continue
        elif x == "S" or x == "s":
            start_row += 1
            if (maze[start_row, start_col] == 1):
                print("game over, you hit the wall")
                break
            elif (maze[start_row, start_col] == 5):
                print("You've reached the end! GG")
                break
            else:
                maze[start_row, start_col] = 5
                maze[start_row - 1, start_col] = 0
                print("\n", maze)
                continue
        elif x == "D" or x == "d":
            start_col += 1
            if (maze[start_row, start_col] == 1):
                print("game over, you hit the wall")
                break
            elif (maze[start_row, start_col] == 5):
                print("You've reached the end! GG")
                break
            else:
                maze[start_row, start_col] = 5
                maze[start_row, start_col - 1] = 0
                print("\n", maze)
                continue
        elif x == "X" or x == "x":
            print("Exiting game...")
            break
except:
    print("Out of Bounds! Game Over.")
