"""
2048 Game Implementation in Python
==================================

Author: Yuanji Zhong
Date: 2025-04-05
GitHub: https://github.com/yourusername/2048-python
Python Version: 3.9+

Description:
------------
A tkinter GUI-based implementation of the classic 2048 puzzle game.
The game supports:
- Move logic for all four directions by the keyboard recognizing
- Automatic merging and scoring
- Save & load game state to/from local file
- Autosave & autoload game when closing and opening the game
- Undo functionality to revert the last move

This project was created for educational purposes and as a coding portfolio piece.

License: MIT
"""
from os.path import exists
from random import randint
from tkinter import Tk, Canvas, Menu
from tkinter.filedialog import askopenfile as op, asksaveasfilename as sa
from tkinter.messagebox import askretrycancel as ask


# Initial and build the structure of data
def initData():
    global data
    data.clear()
    for i in range(n):
        data.append([0] * n)


# Initial the games: new = -1 for load, 0 for Undo, 1 for restart
def init(new=1):
    global data, score, count
    if new:  # New game
        initData()
        if new == 1:
            count = 0
            step.clear()
    elif len(step) > 1:  # Load or Undo
        initData()
        count -= 1
        step.pop(-1)
        score.pop(-1)
    else:
        return
    # Clear and repaint the grids
    ca.delete('all')
    for i in range(n):
        for j in range(n):
            ca.create_rectangle(5 + i * wide, 5 + j * wide, 5 + (i + 1) * wide, 5 + (j + 1) * wide, fill='white',
                                width=2)
    # Repaint the blocks
    if new < 1:
        for i in range(n):
            for j in range(n):
                exp = step[-1][i][j]
                if exp:
                    data[i][j] = [exp, show(i, j, exp)]
    else:
        randStep()
        score = [randStep()]
        # Given beginning: replace the above
        # data[0][0] = [2, show(0, 0, 2)]
        # data[0][1] = [2, show(0, 1, 2)]
        # score = [2]
        step.append([[d[j][0] if d[j] else 0 for j in range(n)] for d in data])
    text()
    ca.create_text(780, 330, text='Undo', font='Times 25')


# Load from a txt file
def load(f=None):
    global count, score, step
    if not f: f = op()
    if not f: return
    read = f.read().split('\n\n')
    f.close()
    count = int(read[0])
    score = [int(e) for e in read[1].split(',')[:-1]]
    step = [[[int(a) for a in b.split(' ')[:-1]] for b in c.split(',')[:-1]] for c in read[2].split('\n')[:-1]]
    init(-1)


# Save to a txt file
def save(path=None):
    if not path: path = sa()
    if not path: return
    if not path.endswith('.txt'): path += '.txt'
    with open(path, 'w') as f:
        f.write(str(count) + '\n\n')
        for s in score:
            f.write(str(s) + ',')
        f.write('\n\n')
        for c in step:
            for b in c:
                for a in b:
                    f.write(str(a) + ' ')
                f.write(',')
            f.write('\n')
        f.close()


# Randomly generate 2 or 4 after a step
def randStep():
    global tempPic
    sc = 0
    empty = []
    for i in range(n):
        for j in range(n):
            if not data[i][j]:
                empty += [[i, j]]
            else:
                sc += 2 ** data[i][j][0]
    exp = randint(1, 2)
    x, y = empty[randint(0, len(empty) - 1)]
    data[x][y] = [exp, show(x, y, exp)]
    tempPic += show(x, y, exp, 'pink')
    # If there is no available movement
    if len(empty) == 1:
        end()
    return sc + 2 ** exp


# Merging the blocks with the same value
def combine(xList, yList):
    exp = 0
    at = 0
    last = 0
    ret = 0
    for i in range(4):
        obj = data[xList[i]][yList[i]]
        if obj:  # There is a block at i
            clear(xList[i], yList[i])
            last = i
            if exp:  # The former one exists
                if exp == obj[0]:  # With the same value
                    data[xList[at]][yList[at]] = [exp + 1, show(xList[at], yList[at], exp + 1)]
                    ret = 1
                    exp = 0
                else:
                    data[xList[at]][yList[at]] = [exp, show(xList[at], yList[at], exp)]
                    exp = obj[0]
                at += 1
            else:
                exp = obj[0]
        if i == len(xList) - 1 and exp:  # Set to the last one
            data[xList[at]][yList[at]] = [exp, show(xList[at], yList[at], exp)]
            if last != at: ret = 1
    return ret


# Check if it ends when the board is full, without any available movements
def end():
    for i in range(n):
        for j in range(1, n):
            if data[i][j][0] == data[i][j - 1][0]: return
            if data[j][i][0] == data[j - 1][i][0]: return
    if ask('Game Over', 'Steps: %d, Scores: %d' % (count, score[-1])):
        init()
    return 1


# Listener for the left click
def click(e):
    if 730 < e.x < 830 and 305 < e.y < 350:
        init(0)  # Undo


# Listener for the keyboard
def key(e):
    global count, tempPic, step, score
    canDo = 0
    if e.keycode == 87 or e.keycode == 38:  # Up
        for i in range(4):
            canDo += combine([i] * 4, range(4))
    elif e.keycode == 83 or e.keycode == 40:  # Down
        for i in range(4):
            canDo += combine([i] * 4, [3, 2, 1, 0])
    elif e.keycode == 65 or e.keycode == 37:  # Left
        for i in range(4):
            canDo += combine(range(4), [i] * 4)
    elif e.keycode == 68 or e.keycode == 39:  # Right
        for i in range(4):
            canDo += combine([3, 2, 1, 0], [i] * 4)
    if canDo:
        count += 1
        text(1)
        step.append([[d[j][0] if d[j] else 0 for j in range(n)] for d in data])
    # save('./autosave.txt')  # Autosave for each steps if needed


# UGI part: Show the blocks with number 2^exp in different colors
def show(i, j, exp, color=None):
    if not color:
        color = COLOR[exp]
    return [ca.create_rectangle(7 + i * wide, 7 + j * wide, 2 + (i + 1) * wide, 2 + (j + 1) * wide, fill=color),
            ca.create_text(5 + (i + 0.5) * wide, 5 + (j + 0.5) * wide, text=str(2 ** exp), font='0 20', fill='red')]


# Clear the original blocks
def clear(i, j):
    ca.delete(data[i][j][1][0], data[i][j][1][1])
    data[i][j] = 0


# Show the text
def text(ra=0):
    global tempPic, score
    for i in tempPic:
        ca.delete(i)
    tempPic = [ca.create_text(780, 120, text='Steps: %d' % count, font='Times 40')]  # Prompt
    if ra: score += [randStep()]
    if score[-1]:
        tempPic += [ca.create_text(780, 190, text='Scores: %d' % score[-1], font='Times 40')]


# Some constant
n = 4
wide = 600 / n
COLOR = [0, '#E7FF6F', '#C9FF6A', '#BDFF82', '#9AFF9C', '#A6FFC9', '#A0FFF7', '#92D7F8', '#7D9EF8', '#7C72FF',
         '#B466FF', '#FD8BFF', '#FFA3D2', '#FF9FAA']
# Some variables
count = 0  # Number of steps
tempPic = []
data, step, score = [], [], []  # data[x][y] = [1, [l1, l2]] for row y column x with painting index l1, l2
# GUI window
root = Tk(className="[2048]")
ca = Canvas(root, width=950, height=610)  # 5~605
ca.pack()
ca.bind('<Button-1>', click)
# ca.bind('<Button-3>', lambda e: print(e.x, e.y))  # Get the position by the right click
root.bind('<KeyRelease>', key)
# Menu
menu = Menu(root)
start = Menu(menu, tearoff=0)
start.add_command(label='Restart', command=init)
menu.add_cascade(label='Start', menu=start)
menu.add_command(label='Load', command=load)
menu.add_command(label='Save', command=save)
root.config(menu=menu)
root.geometry('+285+79')
root.resizable(0, 0)
if __name__ == '__main__':
    # Autoload
    if exists('./autosave.txt'):
        load(open('./autosave.txt', 'r'))
    else:
        init()
    # Show GUI
    root.mainloop()
    # Autosave
    save('./autosave.txt')
