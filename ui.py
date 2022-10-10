import tkinter as tk
import tkinter.messagebox
from sudoku import Solver

# new window
window = tk.Tk()
window.title('数独_wwz')
# current selected number which you want to put
global current
current = tk.StringVar()
current.set('_')
# new a frame in window
frametop = tk.Frame(window)
gridvar = [[tk.StringVar() for col in range(9)] for row in range(9)]


def boxClick(var):
    n = current.get()
    if n == '_':
        n = ''
    var.set(n)


def setCurrent(n):
    global current
    current.set(n)


def setQuestion(question):
    array = [[j for j in i.strip()] for i in question.split(',')]
    print(array)
    for i in range(9):
        for j in range(9):
            n = array[i][j]
            n = '' if n=='0' else n
            gridvar[i][j].set(n)


def clear():
    [[i.set('') for i in j] for j in gridvar]
    setCurrent('_')


def run():
    board = [[(j.get() if j.get() else '0') for j in i] for i in gridvar]
    question = ','.join([''.join(i) for i in board])
    print(question)
    try:
        s = Solver(question)
        s.start()
    except:
        if tk.messagebox.askokcancel(title='No kidding...', message='Please give me right question.'):
            clear()
    else:
        [[gridvar[r][c].set(s.board[r][c]) for r in range(9)] for c in range(9)]


# UI layout
frame = [tk.Frame(frametop) for row in range(9)]
numButtons = [tk.Button(width=3, text=('' if n == '_' else n), command=(lambda num=n: setCurrent(num))) for n in list(range(1, 10))+['_']]
grid = [[tk.Button(frame[row], width=3, textvariable=gridvar[row][col], relief='groove',
        command=(lambda var=gridvar[row][col]: boxClick(var)), font=('Helvetica', '12'))for col in range(9)]
        for row in range(9)]
tk.Label(textvariable=current).pack(side='top')
for row in range(9):
    frame[row].pack(side='top')
    for col in range(9):
        grid[row][col].pack(side='left')
frametop.pack(side='top', pady=10)
for bt in numButtons:
    bt.pack(side='left')
a = tk.Frame(frametop)
a.pack(side='left')
question_1 = '000670080, 060000047, 705800000, 020041000, 080520004, 907000102, 030005260, 000008470, 602090000'
question_2 = '300000051, 005008307, 060005800, 000006209, 800090000, 100200000, 018704000, 004050160, 000600002'
question_3 = '963000000, 000000507, 000438000, 000000802, 050300010, 104000070, 000100720, 706000008, 080020000'
tk.Button(a, width=9, text='Sample_1', command=(lambda func=setQuestion: func(question_1))).pack(side='left')
tk.Button(a, width=9, text='Sample_2', command=(lambda func=setQuestion: func(question_2))).pack(side='left')
tk.Button(a, width=9, text='Sample_3', command=(lambda func=setQuestion: func(question_3))).pack(side='left')
tk.Button(a, width=5, text='Clear', command=clear).pack(side='left')
tk.Button(a, width=5, text='Run', command=run).pack(side='left')

window.mainloop()

