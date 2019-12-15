import tkinter as tk
from PIL import ImageTk, Image
import os
import subprocess
import sys

root = tk.Tk()
root.geometry('1280x720')
canv = tk.Canvas(root, bg='grey')
canv.pack(fill=tk.BOTH, expand=1)


def start():
    if sys.platform.startswith('linux'):
        os.system('python3 graphics.py')
    else:
        theproc = subprocess.Popen([sys.executable, "graphics.py"])
        theproc.communicate()


def draw_tutorial():
    if sys.platform.startswith('linux'):
        os.system('python3 tutorial.py')
    else:
        theproc = subprocess.Popen([sys.executable, "tutorial.py"])
        theproc.communicate()


def reroll():
    if sys.platform.startswith('linux'):
        os.system("python3 auto_generator.py")
    else:
        theproc = subprocess.Popen([sys.executable, "auto_generator.py"])
        theproc.communicate()
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

    root.mainloop()


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
    command=draw_tutorial
)
pilImage = Image.open("images/hell.jpg")
bg = ImageTk.PhotoImage(pilImage)

main()
