mport random
import numpy as np

def update_coin_list(coin_list,move):
    pile,coins_to_remove = move
    coin_list[pile-1] = max(0,coin_list[pile-1]-coins_to_remove)
    return coin_list

def checkGameFinish(coin_list):
    isGameFinish = True
    for c in coin_list:
        if c>0:
            isGameFinish=False
    return isGameFinish

def display_pile(coin_list):
    max_val = max(coin_list)
    for i in range(max_val):
        max_val = max_val-i;
        for coins in coin_list:
            if(coins>=max_val):
                print(' | ',end='')
            else:
                print('   ',end='')
        print()
    for coins in coin_list:
        print('___',end='')
    print()

def getNimScore(coin_list):
    ans = coin_list[0]
    for c in coin_list[1:]:
        ans=ans^c
    return ans

def display(coin_list):
    print(coin_list)
    print('NimSum:',getNimScore(coin_list))

def move_random(coin_list,player):
    pile = random.randint(1,len(coin_list))
    if(coin_list[pile-1]==0):
        return move(coin_list,player)
    if(coin_list[pile-1]==1):
        coins_to_pick=1
    else:
        coins_to_pick = random.randint(1,coin_list[pile-1])
    return (pile,coins_to_pick)
