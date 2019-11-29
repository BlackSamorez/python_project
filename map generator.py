import cv2
import numpy as np
from math import *
import time
from random import randrange as rnd,choice
import tkinter as tk
import math
import time


root = tk.Tk()
fr = tk.Frame(root)
root.geometry('1000x1000')
canv = tk.Canvas(root,bg='black')
canv.pack(fill = tk.BOTH,expand = 1)



n = int(input())
k = int(input())
dx = 1000 / n
dy = 1000 / k

field = [[-1] * n for x in range(k)]

def targeting(event):
	global mx, my
	mx = event.x
	my = event.y

def click(event):
	global mx, my, n, k, dx, dy, field
	i = int(mx // dx)
	j = int(my // dy)
	if field[i][j] == -1:
		field[i][j] = 0
	else:
		field[i][j] = -1


def draw():
	global dx, dy, field
	canv.delete("all")
	for i in range(len(field)):
		for j in range(len(field[0])):
			if field[i][j] == 0:
				canv.create_rectangle(dx * i, dy * j, dx * (i + 1), dy * (j + 1), fill = 'red')

	canv.update()
	root.after(30, draw)

def enter(event):
	global field, n, k, dy, dx
	with open('scene.cfg', 'r') as file:
		s = file.read()
	n, k = [int(x) for x in s.split('\n')[0].split(' ')]
	field = [[-1] * k for x in range(n)]
	for line in s.split('\n')[1:]:
		command, args = line.split(' ', 1)
		if command == 'brick':
			x, y, tid = [int(x) for x in args.split(' ')]
			field[x][y] = tid
	dx = 1000 / n
	dy = 1000 / k

def exit(event):
	global field, n, k
	print('saved')
	with open('scene.cfg', 'w') as file:
		file.write(str(n))
		file.write(' ')
		file.write(str(k))
		file.write('\n')
		file.write('player 1 1 ')
		file.write(str(floor(n / 2)))
		file.write(' ')
		file.write(str(floor(k / 2)))
		for i in range(n):
			for j in range(k):
				if field[i][j] == 0:
					file.write('\n')
					file.write('brick ')
					file.write(str(i))
					file.write(' ')
					file.write(str(j))
					file.write(' 0')


canv.bind('<Return>', exit)
canv.bind('<Escape>', enter)
canv.bind('<Motion>',targeting)
canv.bind('<Button-1>', click)

draw()

root.mainloop()