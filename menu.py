import tkinter as tk
from PIL import ImageTk, Image
import os

root = tk.Tk()
root.geometry('1920x1080')
canv = tk.Canvas(root, bg='grey')
canv.pack(fill=tk.BOTH, expand=1)

def start():
    os.system('python3 graphics.py')


def draw_tutorial():
    pass

def read_scene(filename='scene.cfg'):
    with open(filename, 'r') as file:
        s = file.read()
    fw, fh = [int(x) for x in s.split('\n')[0].split(' ')]
    field = [[-1] * fh for x in range(fw)]
    for line in s.split('\n')[1:]:
        command, args = line.split(' ', 1)
        if command == 'brick':
            x, y, tid = [int(x) for x in args.split(' ')]
            field[x][y] = tid
    return field


def draw_map():
    global field
    scale = 1
    a = 500
    n = len(field)
    k = len(field[0])
    dx = a / n * scale
    dy = a / k * scale
    for i in range(n):
        for j in range(k):
            if field[i][j] != -1:
                canv.create_rectangle(
                    500 + i * dx, 200 + j * dy,
                    500 + (i + 1) * dx, 200 + (j + 1) * dy,
                    fill='black'
                )
            if field[i][j] == 2:
                canv.create_rectangle(
                    500 + i * dx, 200 + j * dy,
                    500 + (i + 1) * dx, 200 + (j + 1) * dy,
                    fill='blue'
                )


global field
field = read_scene()
pilImage = Image.open("hell.jpg")
bg = ImageTk.PhotoImage(pilImage)
canv.create_image(700, 210, image=bg)
start_button = tk.Button(
    root, text='Start',
    width=15, height=2,
    bg='grey', fg='black',
    activeforeground='red', activebackground='grey',
    command=start
)
start_button.place(x=650, y=40)
map_button = tk.Button(
    root, text='Reroll map',
    width=15, height=2,
    bg='grey', fg='black',
    activeforeground='red', activebackground='grey',
    command=draw_map
)
map_button.place(x=650, y=90)
tutorial_button = tk.Button(
    root, text='Tutorial',
    width=15, height=2,
    bg='grey', fg='black',
    activeforeground='red', activebackground='grey',
    command=draw_tutorial
)
tutorial_button.place(x=650, y=140)

root.mainloop()
