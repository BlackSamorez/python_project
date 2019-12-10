from math import *
import time
from random import randrange as rnd,choice
import tkinter as tk





def exit():
	global field, name, n, k, p_n, p_k
	with open(name, 'w') as file:
		file.write(str(6 * n + 1))
		file.write(' ')
		file.write(str(6 * k + 1))
		file.write('\n')
		file.write('player 1 1 ')
		file.write(str(p_n))
		file.write(' ')
		file.write(str(p_k))
		for i in range(6 * n + 1):
			for j in range(6 * k + 1):
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
		with open(('./map_generator/room' + str(i + 1) + '.cfg'), 'r') as file:
			s = file.read()
		
		for line in s.split('\n')[1:]:

			command, args = line.split(' ', 1)
			if command == 'brick':
				x, y, tid = [int(x) for x in args.split(' ')]
				room[x][y][i+ 1] = tid 

	return room


def create_floor():
	global field, name, n, k ,player, dx, dy, percentage, boss_n, boss_k, subfield, p_n, p_k
	

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

	p_n = 6 * boss_n + 5
	p_k = 6 * boss_k + 5

	level_cut()



def level_cut():
	global field, name, n, k ,player, dx, dy, percentage, subfield, boss_n, boss_k, p_n, p_k
	for i in range(n):
		for j in range(k):
			if rnd(0,100) > 60:
				field[6 * i + 3][6 * j] = 0
				field[6 * i][6 * j + 3] = 0
	
	subfield[boss_n][boss_k] = -1
	subfield[boss_n][boss_k + 1] = -1
	subfield[boss_n][boss_k + 2] = -1
	subfield[boss_n + 1][boss_k] = -1
	subfield[boss_n + 1][boss_k + 1] = -1
	subfield[boss_n + 1][boss_k + 2] = -1
	subfield[boss_n + 2][boss_k] = -1
	subfield[boss_n + 2][boss_k + 1] = -1
	subfield[boss_n + 2][boss_k + 1] = -1

	for m in range(2 * n):
		for i in range(n):
			for j in range(k):
				if i !=0 and j!= 0 and i != n-1 and j != k-1:
					if (subfield[i+1][j] == -1 and field[6 * i + 6][6 * j + 3] == -1) or (subfield[i-1][j] == -1 and field[6 * i][6 * j + 3] == -1) or (subfield[i][j+1] == -1 and field[6 * i + 3][6 * j + 6] == -1) or (subfield[i][j-1] == -1 and field[6 * i + 3][6 * j] == -1):
						subfield[i][j] = -1
						far_end = [i, j]

	field[6 * far_end[0] + 3][6 * far_end[1] + 3] = -1
	p_n = 6 * far_end[0] + 3
	p_k = 6 * far_end[1] + 3

	for i in range(n):
			for j in range(k):
				if subfield[i][j] != -1:
					for l in range(6):
						for m in range(6):
							field[6 * i + l][6 * j + m] = 0

	for i in range(1, 6 * n):
			for j in range(1, 6 * k):
				if field[i][j + 1] in [0, -2] and field[i + 1][j] in [0, -2] and field[i][j - 1] in [0, -2] and field[i - 1][j] in [0, -2] and field[i - 1][j - 1] in [0, -2] and field[i - 1][j + 1] in [0, -2] and field[i + 1][j - 1] in [0, -2] and field[i + 1][j + 1] in [0, -2]:
					field[i][j] = -2
	for i in range(1, 6 * n):
			for j in range(1, 6 * k):
				if field[i][j] == -2:
					field[i][j] = -1




name = 'scene.cfg'
percentage = 90
n = 10
k = 10

create_floor()
exit()