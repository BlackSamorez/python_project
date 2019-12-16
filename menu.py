import tkinter as tk
from PIL import ImageTk, Image
import os
import subprocess
import sys
import graphics
import auto_generator

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('1280x720')
canv = tk.Canvas(root, bg='grey')
canv.pack(fill=tk.BOTH, expand=1)

graphics.root = root
graphics.canv = canv


def start():
    canv.delete("all")
    start_button.place(x=-100, y=-100)
    map_button.place(x=-100, y=-100)
    tutorial_button.place(x=-100, y=-100)
    graphics.main()
    main()


def reroll():
    auto_generator.main()
    main()


def draw_map(filename='images/scene.cfg'):
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
                    400 + i * dx, 200 + j * dy,
                    400 + (i + 1) * dx, 200 + (j + 1) * dy,
                    fill='black'
                )
            if field[i][j] == 2:
                canv.create_rectangle(
                    400 + i * dx, 200 + j * dy,
                    400 + (i + 1) * dx, 200 + (j + 1) * dy,
                    fill='blue'
                )

def main():
    canv.delete("all")
    canv.create_image(640, 360, image=bg)
    draw_map("scene.cfg")
    start_button.place(x=620, y=10)
    map_button.place(x=575, y=70)
    tutorial_button.place(x=600, y=122)
    got_button.place(x=-100, y=-100)

    root.mainloop()

def tutorial():
    start_button.place(x=-100, y=-100)
    map_button.place(x=-100, y=-100)
    tutorial_button.place(x=-100, y=-100)
    canv.delete("all")
    canv.create_image(440, 360, image=sas)
    got_button.place(x=600, y=320)

im_start = ImageTk.PhotoImage(file="images/start_new.png")
start_button = tk.Button(
    root, image=im_start,
    command=start
)
im_reroll = ImageTk.PhotoImage(file="images/reroll_map_new.png")
map_button = tk.Button(
    root, image=im_reroll,
    command=reroll
)
im_tutorial = ImageTk.PhotoImage(file="images/tutorial_new.png")
tutorial_button = tk.Button(
    root, image=im_tutorial,
    command=tutorial
)
im_got = ImageTk.PhotoImage(file="images/got_it.png")
got_button = tk.Button(
    root, image=im_got,
    command=main
)
pilImage = Image.open("images/hell.jpg")
bg = ImageTk.PhotoImage(pilImage)
pilImage1 = Image.open("images/text.png")
sas = ImageTk.PhotoImage(pilImage1)

main()
