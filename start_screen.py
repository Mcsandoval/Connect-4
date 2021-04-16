from math import *
import connect_4
import sys

def data_screen():
    print('#################################')
    print('#################################')
    print('########   Connect 4    #########')
    print('########  -New Game     #########')
    print('########  -Load Data    #########')
    print('#################################')
    print('#################################')
    print('#################################')
    print()


data_screen()
user_input = str(input('Please enter an option [New game/Load data]  '))
user_input = user_input.lower()

while user_input != 'load data':
    if user_input == 'new game':
        break
    else:
        print('Sorry unexpected input. Try again')
        user_input = str(input('Please enter an option [New game/Load game]  '))
        user_input = user_input.lower()

if user_input == 'new game':
    new_file = 'Connect 4.csv'
    file = open(new_file,'a+')
    players = input('How many players are there[1 or 2] ?  ')
    players = ceil(float(players))
    player_names = []
    for p in range(players):
        names = input('Enter player names  ')
        file.write(names)
        file.write('\n')
        player_names.append(names)
    print(player_names)
    #title_screen()
    file.close()

else:
    file_name = input('Enter name of the file ')
    try:
        f = open(file_name+'.csv','r')
    except FileNotFoundError:
        print('Sorry, file not found. Try again or create a new game')
    else:
        file = open(file_name+'.csv','r')
        lines = file.readlines()
        names = []
        high_score = []
        for i in range(len(lines)):
            temp = lines[i].split(',')
            names.append(temp[0])
            high_score.append(temp[-1])
        print(names)
        print(high_score)






