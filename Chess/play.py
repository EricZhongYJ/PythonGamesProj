from tkinter import Tk, Canvas, Menu
from tkinter.messagebox import askretrycancel as ask
from PIL.ImageTk import Image as im, PhotoImage as photo
from Soldiers import *


# Only for 2 Players, todo for adding exchanging the King and Rook, eating pass Pawn, judging check and limiting choices when checked
def init(new=1):  # Initialize the graph
    global tempPic, wide, at, count
    # setN(len(step))
    at = []  # The position of the mouse
    if new:
        setN(8)
        step.clear()
        wide = 600 / n[0]  # Width of blocks
        count = 0  # number of steps
        step.append([[4, 8, 6, 2, 0, 6, 8, 4], [10] * 8, [-1] * 8, [-1] * 8, [-1] * 8, [-1] * 8, [11] * 8,
                     [5, 9, 7, 3, 1, 7, 9, 5]])  # Information of each step
    elif len(step) > 1:
        setN(8)
        count -= 1
        step.pop(-1)
    else:
        return
    ca.delete('all')
    for i in range(n[0]):  # Paint each block
        for j in range(n[0]):
            color = '#B67F47' if (i + j) % 2 else '#EFCEAF'
            ca.create_rectangle(5 + i * wide, 5 + j * wide, 5 + (i + 1) * wide, 5 + (j + 1) * wide, fill=color, width=0)
    for i in range(12):  # Load pictures
        pic[i] = im.open('pic/' + str(i) + '.png')
        pic[i] = photo(pic[i].resize([e * 6 // n[0] for e in pic[i].size], 1))
    for i in range(n[0]):  # Load the chess
        for j in range(n[0]):
            Id = step[-1][i][j]
            p = 2 * (Id % 2) - 1
            if Id + 1:
                data[i][j] = [Id, sold[Id // 2](i, j, p, show(j, i, Id))]
    tempPic += [ca.create_text(780, 120, text='Step %d' % count, font='* 40')]  # Prompt
    who = 'Blue' if count % 2 else 'Yellow'
    tempPic += [ca.create_text(780, 190, text='%s\'s Turn' % who, font='* 40')]
    ca.create_text(780, 330, text='Undo', font='* 40')


def click(e):  # Left Click
    global tempPic, at, count
    x = int((e.x - 5) / wide)
    y = int((e.y - 5) / wide)
    for t in tempPic:
        ca.delete(t)
    tempPic = []
    if 0 <= x < n[0] and 0 <= y < n[0]:  # Choose chess
        obj = data[y][x]
        if at and [y, x] in data[at[0]][at[1]][1].touch() and (count % 2) != (data[at[0]][at[1]][1].player > 0):  # Be Chosen
            count += 1
            objAt = data[at[0]][at[1]]
            ca.delete(objAt[1].Id)
            Id = objAt[0]
            data[at[0]][at[1]] = 0
            data[y][x] = [Id, sold[Id // 2](y, x, 2 * (Id % 2) - 1, show(x, y, Id))]
            at = []
            step.append([[e1[0] if e1 else -1 for e1 in e2] for e2 in data])
            if obj:  # Eat
                ca.delete(obj[1].Id)
                if obj[0] < 2:  # Judge if win
                    end(obj[0])
                # check(0)
                # check(1)
        elif obj:  # Choose nothing or choose again
            at = [y, x]
            tempPic += [ca.create_rectangle(8 + x * wide, 8 + y * wide,
                                            2 + (x + 1) * wide, 2 + (y + 1) * wide, outline='green', width=6)]
            for t in obj[1].touch():
                color = '#819A34' if (t[0] + t[1]) % 2 else '#A7D17B'
                tempPic += [ca.create_rectangle(5 + t[1] * wide, 5 + t[0] * wide,
                                                5 + (t[1] + 1) * wide, 5 + (t[0] + 1) * wide, fill=color, width=0)]
                if data[t[0]][t[1]]:
                    Id = data[t[0]][t[1]][0]
                    tempPic += [show(t[1], t[0], Id)]
    elif 730 < e.x < 830 and 305 < e.y < 350:
        init(0)
    tempPic += [ca.create_text(780, 120, text='Step %d' % count, font='* 40')]  # Prompt
    who = 'Blue' if count % 2 else 'Yellow'
    tempPic += [ca.create_text(780, 190, text='%s\'s Turn' % who, font='* 40')]


def show(i, j, Id):  # Paint chess
    return ca.create_image(5 + (i + 0.5) * wide, 5 + (j + 0.5) * wide, image=pic[Id])


# def check(n):  # Check if there is no chess left
#     for i in data:
#         for j in i:
#             if j and j[0] > 1 and j[0] % 2 == n and j[1].touch():
#                 return
#     end(n)


def end(b):  # Ending the game
    who = 'Blue' if b else 'Yellow'
    if ask('Game over', who + ' Won'):
        init()


wide = count = at = 0  # WidthOfBlock/NumberOfSteps/PositionOfMouse
pic = [0] * 12  # Objects of pictures
tempPic = []  # Temporary picture indexes
sold = [king, queen, che, xiang, ma, bing]  # Classes Indexes
root = Tk(className="[Chess] by Eric Zhong")
ca = Canvas(root, width=950, height=610)  # 5~605
ca.pack()
ca.bind('<Button-1>', click)
ca.bind('<Button-3>', lambda e: print(e.x, e.y))  # todo
init()
# Menus
menu = Menu(root)
start = Menu(menu, tearoff=0)
start.add_command(label='Restart', command=init)
menu.add_cascade(label='Start', menu=start)
root.config(menu=menu)
root.geometry('+285+79')
root.resizable(0, 0)
root.mainloop()
