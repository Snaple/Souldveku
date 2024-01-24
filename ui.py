import tkinter as tk
import tkinter.messagebox
from sudoku import Solver


window = tk.Tk()
window.title('Souldveku_wwz')
# current: the number which is selected currently
current = tk.StringVar()
current.set('_')


def boxClick(var):
    row, col = var
    n = current.get()
    if n == '_':
        n = ''
    grid[row][col].config(fg=fg_dict.get(int(n)) if n else 'black')
    gridvar[row][col].set(n)


def setCurrent(n):
    current_label.config(fg=fg_dict.get(n, 'black'))
    current.set(n)


def setQuestion(question):
    array = [[j for j in i.strip()] for i in question.split(',')]
    # print(array)
    for i in range(9):
        for j in range(9):
            n = array[i][j]
            n = '' if n == '0' else n
            gridvar[i][j].set(n)
            grid[i][j].config(fg=fg_dict.get(int(n)) if n else 'black')


def clear():
    [[i.set('') for i in j] for j in gridvar]
    [[i.config(fg='black') for i in j] for j in grid]
    setCurrent('_')


def run():
    board = [[(j.get() if j.get() else '0') for j in i] for i in gridvar]
    question = ','.join([''.join(i) for i in board])
    print(question)
    try:
        s = Solver(question)
        s.start()
    except:
        if tk.messagebox.askokcancel(title='No kidding...', message='Please give me a valid question.'):
            clear()
    else:
        [[gridvar[r][c].set(s.board[r][c]) for r in range(9)] for c in range(9)]


# UI component
frametop = tk.Frame(window)
frames = [tk.Frame(frametop) for row in range(9)]
# 9x9 grid text, it should be dynamic, so StringVar was used.
gridvar = [[tk.StringVar() for col in range(9)] for row in range(9)]

# font ground color, key: number, value: color code(RGB)
fg_dict = {1: '#CD6800', 2: '#CD96CD', 3: '#CD8162', 4: '#CD00CD', 5: '#C71585',
           6: '#B03060', 7: '#6B8E23', 8: '#696969', 9: '#FF0000'}
# background color, key: block(3x3 grid) seq, value: color code(RGB), just for comfortable visual.
bg_dict = {1: '#E0EEEE', 2: '#00FFFF', 3: '#E0EEEE', 4: '#00FFFF', 5: '#76EEC6',
           6: '#00FFFF', 7: '#E0EEEE', 8: '#00FFFF', 9: '#E0EEEE'}
# numbers 1~9 buttons and button `_`
numButtons = [tk.Button(width=3, text=('' if n == '_' else n), fg=fg_dict.get(n),
                        command=(lambda num=n: setCurrent(num)))
              for n in list(range(1, 10))+['_']]
# 9x9 buttons
grid = [[tk.Button(frames[row], width=3, textvariable=gridvar[row][col], relief='groove', fg='black',
                   background=bg_dict.get(row//3*3+col//3+1), command=(lambda var=(row, col): boxClick(var)),
                   font=('Helvetica', '12'))
         for col in range(9)] for row in range(9)]
# show the currently selected number
current_label = tk.Label(textvariable=current)
current_label.pack(side='top')
# grid layout
for row in range(9):
    frames[row].pack(side='top')
    for col in range(9):
        grid[row][col].pack(side='left')
frametop.pack(side='top', pady=10)

# number 1~9 button layout
for bt in numButtons:
    bt.pack(side='left')
a = tk.Frame(frametop)
a.pack(side='left')
# sample questions
question_1 = '000670080, 060000047, 705800000, 020041000, 080520004, 907000102, 030005260, 000008470, 602090000'
question_2 = '300000051, 005008307, 060005800, 000006209, 800090000, 100200000, 018704000, 004050160, 000600002'
question_3 = '963000000, 000000507, 000438000, 000000802, 050300010, 104000070, 000100720, 706000008, 080020000'
# `sample`, `clear`, `run` buttons layout
tk.Button(a, width=9, text='Sample_1', command=(lambda func=setQuestion: func(question_1))).pack(side='left')
tk.Button(a, width=9, text='Sample_2', command=(lambda func=setQuestion: func(question_2))).pack(side='left')
tk.Button(a, width=9, text='Sample_3', command=(lambda func=setQuestion: func(question_3))).pack(side='left')
tk.Button(a, width=5, text='Clear', command=clear).pack(side='left')
tk.Button(a, width=5, text='Run', command=run).pack(side='left')
# bind key 1-9 to set current number
[window.bind(f'<Key-{i}>', (lambda e, n=i: setCurrent(n))) for i in range(1, 10)]
# bind <delete> to clear current number
window.bind('<Delete>', (lambda e: setCurrent('_')))


window.mainloop()
