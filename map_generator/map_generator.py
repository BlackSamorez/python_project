from math import *
import time
from random import randrange as rnd,choice
import tkinter as tk




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
	global field, name, n, k, dy, dx
	with open(name, 'r') as file:
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
	global field, name, n, k, player
	print('saved')
	with open(name, 'w') as file:
		file.write(str(n))
		file.write(' ')
		file.write(str(k))
		if player:
			print('playered')
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


def import_rooms():
	room = [[[-1] * 13 for x in range(11)] for y in range(11)]
	for i in range(12):
		with open(('room' + str(i + 1) + '.cfg'), 'r') as file:
			s = file.read()
		
		for line in s.split('\n')[1:]:

			command, args = line.split(' ', 1)
			if command == 'brick':
				x, y, tid = [int(x) for x in args.split(' ')]
				room[x][y][i+ 1] = tid 

	return room


def create_floor(event):
	global field, name, n, k ,player, dx, dy, percentage
	print('level creation has begun')

	room = import_rooms()

	field = [[-1] * (6 * n + 1) for x in range(((k * 6) + 1))]
	subfield = [[-1] * n for x in range(k)]

	for i in range(n):
		field[(6 * i + 3)][0] = 0
	for i in range(k):
		field[0][6 * i + 3] = 0
	for i in range(6 * n):
		field[i + 1][6 * k] = 0
	for i in range(6 * k):
		field[6 * n][i + 1] = 0
	field[0][6 * k] = 0
	field[6 * n][0] = 0


	for a in range(n):
		for b in range(k):
			field[(6 * a) + 0][(6 * b) + 0] = 0
			field[(6 * a) + 1][(6 * b) + 0] = 0
			field[(6 * a) + 0][(6 * b) + 1] = 0
			field[(6 * a) + 2][(6 * b) + 0] = 0
			field[(6 * a) + 0][(6 * b) + 2] = 0
			field[(6 * a) + 4][(6 * b) + 0] = 0
			field[(6 * a) + 0][(6 * b) + 4] = 0
			field[(6 * a) + 5][(6 * b) + 0] = 0
			field[(6 * a) + 0][(6 * b) + 5] = 0

	boss_n = rnd(0, n - 3)
	boss_k = rnd(0, k - 3)


	for a in range(n):
		for b in range(k):
			if subfield[a][b] == -1:
				subfield[a][b] = rnd(1, 7)
				if a != n - 1 and b != k - 1:
					luck = rnd(1,100)
					if luck > percentage:
						subfield[a][b] = rnd(1, 7)
					else:
						subfield[a][b] = rnd(8, 12)

				

				if subfield[a][b] in [8, 9, 10, 11, 12]:
					subfield[a + 1][b] = subfield[a][b]
					subfield[a + 1][b + 1] = subfield[a][b]
					subfield[a][b + 1] = subfield[a][b]

					for l in range(11):
						for m in range(11):
							field[(6 * a + 1) + l][(6 * b + 1) + m] = room[l][m][subfield[a][b]]

				if subfield[a][b] in [1, 2, 3, 4, 5, 6, 7]:
					for l in range(5):
						for m in range(5):
							z = room[l][m][subfield[a][b]]
							field[(6 * a + 1) + l][(6 * b + 1) + m] = z


	boss_n = rnd(0, n - 3)
	boss_k = rnd(0, k - 3)
	for i in range(17):
		for j in range(17):
			field[6 * boss_n + i + 1][6 * boss_k + j + 1] = -1

	dx = 1000 / (6 * n + 1)
	dy = 1000 / (6 * k + 1)

	print('level creation has ended')








if __name__ == "__main__":
	root = tk.Tk()
	fr = tk.Frame(root)
	root.geometry('1000x1000')
	canv = tk.Canvas(root,bg='black')
	canv.pack(fill = tk.BOTH,expand = 1)

	player = int(input())
	name = input()
	n = int(input())
	k = int(input())
	dx = 1000 / n
	dy = 1000 / k
	percentage = 80

	field = [[-1] * n for x in range(k)]


	canv.bind('<Return>', exit)
	canv.bind('<Escape>', enter)
	canv.bind('<Motion>',targeting)
	canv.bind('<Button-1>', click)
	canv.bind('<F2>', create_floor)

	draw()

	root.mainloop()


