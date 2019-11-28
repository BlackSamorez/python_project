from common_classes import *
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
root.geometry('64x48')
canv = tk.Canvas(root,bg='black')
canv.pack(fill = tk.BOTH,expand = 1)


def _from_rgb(rgb): #HEX from rgb
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])   

class Vector2D: #vectors
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __add__(self, o):
		return Vector2D(self.x + o.x, self.y + o.y)
	def __sub__(self, o):
		return Vector2D(self.x - o.x, self.y - o.y)
	def __truediv__(self, a):
		return Vector2D(self.x / a, self.y / a)
	def __mul__(self, o):
		if isinstance(o, Vector2D):
			return self.x * o.x + self.y * o.y
		else:
			return Vector2D(self.x * o, self.y * o)
	def __mod__(self, o):
		return self.x * o.y - self.y * o.x
	def __str__(self):
		return '(' + str(self.x) + ', ' + str(self.y) + ')'

#Vector operations
def v_abs2(x):
	return x * x
def v_abs(x):
	return sqrt(x * x)
def v_norm(x):
	return x / v_abs(x)
def v_rot(x):
	return Vector2D(-x.y, x.x)

#what we control
class Player:
	def __init__(self, look, position, health):
		self.look = look
		self.position = position
		self.health = health
		self.forward = 0
		self.right = 0
		self.rot = 0

#not used yet
class Entity:
	def __init__(self, look, position):
		self.look = look
		self.position = position

#map object
class Scene:
	def __init__(self, filename = None):
		self.width = 64
		self.height = 48
		self.camx = pi / 3
		self.camy = self.camx * 1080 / 1920
		with open(filename, 'r') as file:
			s = file.read()
		self.fw, self.fh = [int(x) for x in s.split('\n')[0].split(' ')]
		self.field = [[-1] * self.fh for x in range(self.fw)]
		for line in s.split('\n')[1:]:
			command, args = line.split(' ', 1)
			if command == 'brick':
				x, y, tid = [int(x) for x in args.split(' ')]
				self.field[x][y] = tid
			if command == 'player':
				lx, ly, x, y = [float(x) for x in args.split(' ')]
				self.player = Player(v_norm(Vector2D(lx, ly)), Vector2D(x, y), PLAYER_HEALTH_DEFAULT)
		
		self.image = np.zeros((self.height, self.width, 3), np.uint8)
		self.image2 = np.zeros((self.height * 2, self.width * 2, 3), np.uint8)
		self.bg = np.zeros((self.height, self.width, 3), np.uint8)

	def display(self):
		canv.delete("all")
		x_old = -1
		for x_ in range(0, self.width):
			debug = (x_ == self.width // 2)

			player = self.player
			to = v_norm(v_rot(player.look) * sin(self.camx * x_ / self.width - 0.5) + player.look * cos(self.camx * x_ / self.width - 0.5))
			ok_walls = []
			x = player.position
			deltaDistX = abs(1 / to.x)
			deltaDistY = abs(1 / to.y)
			mapX = int(x.x)
			mapY = int(x.y)
			if to.x < 0:
				stepX = -1
				sideDistX = (x.x - int(x.x)) * deltaDistX;
			else:
				stepX = 1
				sideDistX = (-(x.x - int(x.x)) + 1) * deltaDistX;
			if to.y < 0:
				stepY = -1
				sideDistY = (x.y - int(x.y)) * deltaDistY;
			else:
				stepY = 1
				sideDistY = (-(x.y - int(x.y)) + 1) * deltaDistY;
			hit = -1
			side = 0
			while hit == -1:
				if sideDistX < sideDistY:
					sideDistX += deltaDistX
					mapX += stepX
					side = 0
				else:
					sideDistY += deltaDistY
					mapY += stepY
					side = 1
				if mapX < 0 or mapX >= self.fw or mapY < 0 or mapY >= self.fh:
					break
				if self.field[mapX][mapY] != -1:
					hit = self.field[mapX][mapY]
			
			if hit != -1:
				if side == 0:
					perpWallDist = (mapX - x.x + (1 - stepX) / 2) / to.x;
				else:
					perpWallDist = (mapY - x.y + (1 - stepY) / 2) / to.y;
				lh = int(1 / perpWallDist / self.camy * self.height / 2)
				brightness = abs(to.x if side == 0 else to.y)

				if (side == 0):
					wallX = x.y + perpWallDist * to.y;
				else:
					wallX = x.x + perpWallDist * to.x;
				wallX = wallX - int(wallX)


				
				canv.create_line(x_, (self.height // 2 - lh), x_, (self.height // 2 + lh), fill=_from_rgb([int(0), int(255 * brightness), int(0)]))
		canv.update()

#start moving
def move_detect(event):
	global player
	if event.char == 'w':
		s.player.forward = 1
		
	if event.char == 'a':
		s.player.right = 1
		
	if event.char == 's':
		s.player.forward = -1
		
	if event.char == 'd':
		s.player.right = -1

	if event.char == 'q':
		s.player.rot = 1

	if event.char == 'e':
		s.player.rot = -1

#stop moving
def move_undetect(event):
	global player, a

	if event.char == 'w':
		s.player.forward = 0
		
	if event.char == 'a':
		s.player.right = 0
		
	if event.char == 's':
		s.player.forward = 0
		
	if event.char == 'd':
		s.player.right = 0

	if event.char == 'q':
		s.player.rot = 0

	if event.char == 'e':
		s.player.rot = 0

#move itself
def player_move():
	global player, a
	if s.player.forward == 1:
		s.player.position = s.player.position + s.player.look * 0.05
	
	if s.player.forward == -1:
		s.player.position = s.player.position - s.player.look * 0.05

	if s.player.right == 1:
		s.player.position = s.player.position - v_rot(s.player.look) * 0.05
	
	if s.player.right == -1:
		s.player.position = s.player.position + v_rot(s.player.look) * 0.05

	if s.player.rot == 1:
		a -= 2 / 180 * pi
		s.player.look = Vector2D(cos(a), sin(a))

	if s.player.rot == -1:
		a += 2 / 180 * pi
		s.player.look = Vector2D(cos(a), sin(a))


#main body
if __name__ == "__main__":
	s = Scene('scene.cfg')
	a = atan2(s.player.look.x, s.player.look.y)
	frame = 0
	begin = time.time()
	canv.bind("<KeyPress>", move_detect)
	canv.bind("<KeyRelease>", move_undetect)


	while True:
		s.display()
		#if n != -1:
		#	print(n)
		'''if n == 97:
			s.player.position = s.player.position - v_rot(s.player.look) * 0.5
		if n == 119:
			s.player.position = s.player.position + s.player.look * 0.5
		if n == 100:
			s.player.position = s.player.position + v_rot(s.player.look) * 0.5
		if n == 115:
			s.player.position = s.player.position - s.player.look * 0.5
		if n == 81:
			a -= 2 / 180 * pi
			#print(1)
			s.player.look = Vector2D(cos(a), sin(a))
		if n == 83:
			a += 2 / 180 * pi
			s.player.look = Vector2D(cos(a), sin(a))'''
		frame += 1
		if frame % 60 == 0:
			print(frame / (time.time() - begin))
		player_move()

	root.mainloop()

