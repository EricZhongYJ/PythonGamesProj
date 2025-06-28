from math import sin, cos
from threading import Timer
from tkinter import Tk, Canvas, Menu
from PIL.ImageTk import Image as im, PhotoImage as photo


# The function of Mouse and Keyboard
def click(e):  # Left Click
    if not B[0] and 284 < e.x < 468 and 190 < e.y < 365:  # Click Start
        level(1 - n)
    elif B[0] == 2 and 874 < e.x < 1037 and 92 < e.y < 171:  # Click Next Level
        level(1)
    elif B[0] == 1 and cheatId + 1:  # Put something Cheating
        global mine
        tempId = ca.create_image(e.x, e.y, image=pic[cheatId])
        mine += [[cheatId, e.x, e.y, tempId]]


def move(e):  # Move Mouse
    if B[0] == 1 and cheatId + 1:  # Show something Cheating
        global cheatPic
        ca.delete(cheatPic)
        cheatPic = ca.create_image(e.x, e.y, image=pic[cheatId])


def clickDel(e):  # Delete something by Right Click
    if B[0] == 1 and cheatId + 1:
        for m in mine:
            if (e.x - m[1]) ** 2 + (e.y - m[2]) ** 2 < 400:
                ca.delete(m[3])
                mine.remove(m)
                break
    else:
        print(e.x, e.y)


def down(_e):  # Push a hook
    if B[0] == 1 and B[1]:
        B[1] = B[2] = 0


def up(_e):  # Throw the dynamite
    global bombLoc
    if at + 1 and bombId and not bombLoc:
        bombLoc = [573, 111, bombId[-1]]
        bombId.pop(-1)


# Functions for playing
def init():  # Initialize
    global B, score, bombId, cheatId
    B = [0] * 3
    score, cheatId = 0, -1
    bombId = [0, 0]
    # Setting for binding the events
    ca.bind('<ButtonRelease-1>', click)
    ca.bind('<Motion>', move)
    ca.bind('<Button-3>', clickDel)
    root.bind('<KeyRelease-S>', down)
    root.bind('<KeyRelease-s>', down)
    root.bind('<KeyRelease-W>', up)
    root.bind('<KeyRelease-w>', up)
    ca.delete('all')
    ca.create_image(564, 369, image=pic[8])


def level(i=1):  # Choose the levels
    global B, n, v, mine, time, target
    B = [1, 1, 0]
    n += i
    v = 0.05
    data[0] = -1.3
    data[1] = 32
    ca.delete('all')
    if n == 1:  # variables: mine = [[Type 0~4, x, y, index=0]]
        target = 2000
        mine = [[0, 564, 369, 0], [0, 194, 388, 0], [0, 270, 473, 0], [1, 357, 520, 0], [2, 488, 512, 0],
                [1, 373, 361, 0], [3, 838, 422, 0], [4, 801, 493, 0], [1, 704, 375, 0], [0, 933, 288, 0]]
    else:  # todo You can add your own level here
        global score
        score, target = 'Like', 'Thumbs up'
        mine = [[4, 81, 466, 0], [4, 81, 523, 0], [4, 82, 577, 0], [4, 155, 465, 0], [4, 156, 522, 0], [4, 157, 581, 0],
                [4, 194, 523, 0], [4, 196, 427, 0], [4, 200, 463, 0], [4, 200, 579, 0], [4, 221, 367, 0],
                [4, 231, 309, 0], [4, 232, 522, 0], [4, 242, 460, 0], [4, 243, 411, 0], [4, 244, 577, 0],
                [4, 256, 359, 0], [4, 269, 521, 0], [4, 286, 461, 0], [4, 289, 577, 0], [4, 308, 520, 0],
                [4, 329, 460, 0], [4, 430, 469, 0], [4, 431, 410, 0], [4, 447, 503, 0], [4, 449, 377, 0],
                [4, 473, 545, 0], [4, 475, 336, 0], [4, 490, 489, 0], [4, 493, 377, 0], [4, 519, 305, 0],
                [4, 519, 574, 0], [4, 528, 454, 0], [4, 542, 377, 0], [4, 565, 295, 0], [4, 567, 405, 0],
                [4, 567, 465, 0], [4, 567, 524, 0], [4, 567, 582, 0], [4, 589, 377, 0], [4, 609, 452, 0],
                [4, 613, 302, 0], [4, 615, 575, 0], [4, 635, 374, 0], [4, 643, 482, 0], [4, 658, 330, 0],
                [4, 658, 541, 0], [4, 683, 372, 0], [4, 685, 498, 0], [4, 702, 405, 0], [4, 702, 463, 0],
                [4, 804, 393, 0], [4, 829, 581, 0], [4, 843, 534, 0], [4, 851, 446, 0], [4, 853, 394, 0],
                [4, 874, 556, 0], [4, 879, 510, 0], [4, 901, 449, 0], [4, 902, 392, 0], [4, 904, 335, 0],
                [4, 927, 511, 0], [4, 929, 277, 0], [4, 953, 448, 0], [4, 954, 391, 0], [4, 956, 334, 0],
                [4, 976, 509, 0], [4, 986, 553, 0], [4, 1002, 445, 0], [4, 1005, 391, 0], [4, 1015, 533, 0],
                [4, 1019, 587, 0], [4, 1055, 390, 0]]

    time = 46
    ca.create_image(564, 369, image=tip)
    ca.create_text(570, 339, text='Level ' + str(n) + '\nTarget Scores:' + str(target) + '\nScores:' + str(score),
                   font='-size 32')
    Timer(1, draw).start()


def draw():  # Draw the mines
    ca.delete('all')
    ca.create_image(564, 369, image=pic[9])
    ca.create_text(183, 42, text='Level: ' + str(n), font='22')
    for m in mine:  # Draw the mines
        # if m[0] + 1:
        m[3] = ca.create_image(m[1], m[2], image=pic[m[0]])
    for j in range(len(bombId)):  # Draw the dynamite
        bombId[j] = ca.create_image(724 + 20 * j, 90, image=pic[5])
    text[1] = ca.create_text(947, 42, text='Scores: ' + str(score), font='22')
    ca.create_text(947, 94, text='Target Scores: ' + str(target), font='22')
    timer()
    loop()


def timer():  # Time Left
    global time, text
    if time > 0 and B[0] == 1:
        time -= 1
        ca.delete(text[0])
        text[0] = ca.create_text(183, 94, text=f'Time Left:{time:2d} sec', font='22')
        Timer(0.99, timer).start()
    elif time == 0:
        B[0] = 2
        Timer(0.03, end).start()


def loop():  # Draw in a loop
    global B, v, vy, at, data, mine, score, hookPic, text, bombLoc
    if B[0] == 1:
        ca.delete(data[-2], data[-1])
        hookPic = photo(hook.rotate(57.3 * data[0]))
        hookLoc = 573 + (9 + data[1]) * sin(data[0]), 111 + (9 + data[1]) * cos(data[0])
        if B[1]:
            if not -1.4 < data[0] < 1.4:  # Rotate the hook
                v = -v
            data[0] += v
        else:
            if B[2]:  # Hook turns up
                data[1] -= vy
                if data[1] <= 32:  # Hook stops
                    data[1] = 32
                    B[1] = 1
                    if at + 1:  # Sell mines
                        score += mark[mine[at][0]]
                        ca.delete(text[1])
                        text[1] = ca.create_text(947, 42, text='Scores: ' + str(score), font='22')
                        ca.delete(mine[at][3])
                        mine.pop(at)
                        at = -1
                elif at + 1:  # Hook brings mines
                    ca.delete(mine[at][3])
                    mine[at][1] -= vy * sin(data[0])
                    mine[at][2] -= vy * cos(data[0])
                    mine[at][3] = ca.create_image(mine[at][1], mine[at][2], image=pic[mine[at][0]])
                if bombLoc:  # Push the dynamite
                    bombLoc[0] += 16 * sin(data[0])
                    bombLoc[1] += 16 * cos(data[0])
                    ca.delete(bombLoc[2])
                    if bombLoc[1] < hookLoc[1]:
                        bombLoc[2] = ca.create_image(bombLoc[0], bombLoc[1], image=pic[5])
                    else:
                        bombLoc = []
                        bang(hookLoc)
            else:  # Hook turns down
                vy = 7
                data[1] += vy
                for m in mine:  # Judge if hook get the mine
                    if (hookLoc[0] - m[1]) ** 2 + (hookLoc[1] - m[2]) ** 2 < dis[m[0]]:
                        at = mine.index(m)
                        B[2] = 1
                        if m[0] == 4:  # Judge if it is dynamite
                            bang(m[1:3])
                        elif m[0] == 1:  # Judge if it is a stone
                            vy = 3
                        break
                if not (15 < hookLoc[0] < 1110 and hookLoc[1] < 720):  # Judge if it is at boundary
                    vy = 11
                    B[2] = 1
        data[-2] = ca.create_line(573, 111, 573 + data[1] * sin(data[0]), 111 + data[1] * cos(data[0]), width=3)
        data[-1] = ca.create_image(hookLoc, image=hookPic)
        Timer(0.02, loop).start()


def end():  # End the level
    B[0] = -1
    ca.delete('all')
    ca.create_image(564, 369, image=tip)
    if score < target or score == 'Like':
        ca.create_text(570, 339,
                       text='Sorry. You have not reach\nthe target.\nTarget Scores: ' + str(target) + '\nScores: ' + str(
                           score),
                       font='-size 32')
    else:
        ca.create_text(570, 339, text='Congratulations. You\nreached the target.\nTarget Scores: ' + str(
            target) + '\nScores: ' + str(score),
                       font='-size 32')
        Timer(1, shops).start()


def shops():  # Shopping in the store todo
    B[0] = 2
    ca.delete('all')
    ca.create_image(564, 369, image=shop)


def cheat(n):  # Cheating
    global mine, time, cheatId, bombId, score
    if n == 0:  # Clear the mines
        for m in mine:
            ca.delete(m[3])
        mine = []
    elif n == 1:  # Set Time Left as -1
        time = -1
    elif n == 2:  # Add one dynamite
        bombId += [ca.create_image(724 + 20 * len(bombId), 90, image=pic[5])]
    elif n == 3:  # Set Score to Target
        if B[0] == 1:
            score = target
            ca.delete(text[1])
            text[1] = ca.create_text(947, 42, text='Score: ' + str(score), font='22')
    elif n == 4:  # Information of mines
        temp = []
        for m in mine:
            temp += [m[:3] + [0]]
        print('mine =', sorted(temp))
    else:  # Cheating
        cheatId = n - 6
        ca.delete(cheatPic)


def Quit():  # Quit Game
    global time
    B[0] = -1
    time = -1
    Timer(0.02, root.quit).start()


# Function of dynamite
def bang(loc):  # Explode
    global at, vy
    vy = 12
    if at + 1:  # In case of at=-1
        ca.delete(mine[at][3])
        mine.pop(at)
    at = -1
    Id = ca.create_image(loc, image=bangPic)
    Timer(0.15, lambda: judge(Id, loc)).start()


def judge(Id, loc):  # Judge something near the dynamite
    for m in mine:
        if (loc[0] - m[1]) ** 2 + (loc[1] - m[2]) ** 2 < 9000:
            mine.remove(m)
            ca.delete(m[3])
            if m[0] == 4:  # Explode the other near tnt
                bang(m[1:3])
    Timer(0.15, lambda: ca.delete(Id)).start()


if __name__ == '__main__':
    # Initialize
    n, at, cheatId = 1, -1, -1
    v = vy = time = target = score = hookPic = cheatPic = 0
    mine = bombId = bombLoc = []
    pic, B, data, text = [object()] * 10, [0] * 3, [0.0] * 4, [0] * 2
    # B = [0 Status(0 Start,1 Dig,2 Store); 1 Swing; 2 Up]
    # data = [0 Degree; 1 Length; -2 LineIndex; -1 HookIndex]
    name = ['gold', 'stone', 'diamond', 'bag', 'tnt', 'bomb', 'drink', 'book', 'cover', 'bg']
    dis = [1900, 1000, 1000, 1200, 1200]
    mark = [500, 20, 800, 300, 0]
    root = Tk(className='[Gold Miner]')
    ca = Canvas(root, bg='black', width=1125, height=734)
    ca.pack()
    # Pictures
    for i in range(10):
        pic[i] = photo(file='pic/' + name[i] + '.png')
    hook = im.open('pic/hook.png')
    tip = photo(im.open('pic/tip.jpg').resize((1123, 732), 1))
    shop = photo(im.open('pic/shop.jpg').resize((1123, 732), 1))
    bangPic = photo(im.open('pic/bang.png').resize((192, 132), 1))
    init()
    # Menus
    menu = Menu(root)
    begin = Menu(root, tearoff=0)
    edit = Menu(root, tearoff=0)
    begin.add_command(label='Restart', command=init)
    begin.add_command(label='Next Level', command=end)
    begin.add_command(label='Quit', command=Quit)
    label = ['Clear Mines', 'Infinite Time Left', 'Add a Dynamite', 'Reach Target', 'Mine Information', 'Turn off Cheating',
             'LeftClick GoldMine', 'LeftClick Stone', 'LeftClick Diamond', 'LeftClick Bag', 'LeftClick TNT']
    for i in range(11):
        edit.add_command(label=label[i], command=lambda j=i: cheat(j))
        if i == 4:
            edit.add_separator()
    menu.add_cascade(label='Start', menu=begin)
    menu.add_cascade(label='Develop Mode', menu=edit)
    menu.add_command(label='Thumbs up', command=lambda: cheat(3))
    root.config(menu=menu)
    # Show Window
    root.resizable(0, 0)
    root.geometry("+190+20")
    root.protocol("WM_DELETE_WINDOW", Quit)
    root.mainloop()
