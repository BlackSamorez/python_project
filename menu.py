import tkinter as tk
from PIL import ImageTk, Image
import os

root = tk.Tk()
root.geometry('1920x1080')
canv = tk.Canvas(root, bg='grey')
canv.pack(fill=tk.BOTH, expand=1)

def start():
    os.system('graphics.py')


def draw_tutorial():
    os.system('tutorial.py')

def reroll():
    os.system("auto_generator.py")
    os.system("menu.py")

def draw_map(filename='scene.cfg'):
    with open(filename, 'r') as file:
        s = file.read()
    fw, fh = [int(x) for x in s.split('\n')[0].split(' ')]
    field = [[-1] * fh for x in range(fw)]
    for line in s.split('\n')[1:]:
        command, args = line.split(' ', 1)
        if command == 'brick':
            x, y, tid = [int(x) for x in args.split(' ')]
            field[x][y] = tid

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



pilImage = Image.open("hell.jpg")
bg = ImageTk.PhotoImage(pilImage)
canv.create_image(700, 210, image=bg)
draw_map("scene.cfg")
im_start = ImageTk.PhotoImage(file="start.png")
start_button = tk.Button(
    root, image=im_start,
    command=start
)
start_button.place(x=647, y=40)
im_reroll = ImageTk.PhotoImage(file="reroll.png")
map_button = tk.Button(
    root, image=im_reroll,
    command=reroll
)
map_button.place(x=590, y=90)
im_tutorial = ImageTk.PhotoImage(file="tutorial.png")
tutorial_button = tk.Button(
    root, image=im_tutorial,
    command=draw_tutorial
)
tutorial_button.place(x=617, y=140)

root.mainloop()
