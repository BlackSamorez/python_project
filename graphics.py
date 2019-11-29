from math import *
import time
from random import randrange as rnd,choice
import tkinter as tk
import math
import time


root = tk.Tk()
fr = tk.Frame(root)
root.geometry('640x480')
canv = tk.Canvas(root,bg='grey')
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
	def __init__(self, look, position):
		self.look = look
		self.position = position
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
		self.width = 640
		self.height = 480
		self.camx = pi / 3
		self.camy = self.camx * 480 / 640
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
				self.player = Player(v_norm(Vector2D(lx, ly)), Vector2D(x, y))
		
		

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
					if self.field[mapX][mapY] == 0:
						self.field[mapX][mapY] = 1
			
			if hit != -1:
				if side == 0:
					perpWallDist = (mapX - x.x + (1 - stepX) / 2) / to.x;
				else:
					perpWallDist = (mapY - x.y + (1 - stepY) / 2) / to.y;
				lh = int(1 / (perpWallDist + 0.0001) / self.camy * self.height / 2)
				if perpWallDist > 1:
					brightness = abs(to.x if side == 0 else to.y) / perpWallDist
				else:
					brightness = abs(to.x if side == 0 else to.y)

				if (side == 0):
					wallX = x.y + perpWallDist * to.y;
				else:
					wallX = x.x + perpWallDist * to.x;
				wallX = wallX - int(wallX)


				
				canv.create_line(x_, (self.height // 2 - lh), x_, (self.height // 2 + lh), fill=_from_rgb([int(255 * brightness), int(255 * brightness), int(255 * brightness)]))
				#canv.create_line(x_, self.height, x_, 0, fill=_from_rgb([int(255 * brightness), int(255 * brightness), int(255 * brightness)]))
		canv.update()

#start moving
def move_detect(event):
	global player, show_minimap
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

	if event.char == 'm':
		show_minimap = 1


#stop moving
def move_undetect(event):
	global player, a, show_minimap

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

	if event.char == 'm':
		show_minimap = 0

#move itself
def player_move():
	global player, a
	if s.player.forward == 1 and s.field[floor(s.player.position.x + s.player.look.x * 0.1)][floor(s.player.position.y + s.player.look.y * 0.1)] == -1:
		s.player.position = s.player.position + s.player.look * 0.1
	
	if s.player.forward == -1 and s.field[floor(s.player.position.x - s.player.look.x * 0.1)][floor(s.player.position.y - s.player.look.y * 0.1)] == -1:
		s.player.position = s.player.position - s.player.look * 0.1

	if s.player.right == 1 and s.field[floor(s.player.position.x - v_rot(s.player.look).x * 0.1)][floor(s.player.position.y - v_rot(s.player.look).y * 0.1)] == -1:
		s.player.position = s.player.position - v_rot(s.player.look) * 0.1
	
	if s.player.right == -1 and s.field[floor(s.player.position.x + v_rot(s.player.look).x * 0.1)][floor(s.player.position.y + v_rot(s.player.look).y * 0.1)] == -1:
		s.player.position = s.player.position + v_rot(s.player.look) * 0.1



	if s.player.rot == 1:
		a -= 5 / 180 * pi
		s.player.look = Vector2D(cos(a), sin(a))

	if s.player.rot == -1:
		a += 5 / 180 * pi
		s.player.look = Vector2D(cos(a), sin(a))

class minimap():
	def __init__(self, scene, scenewidth = 0, sceneheight = 0):
		self.scale = 2
		self.a = 100
		self.player = scene.player
		self.field = scene.field
		self.n = len(self.field)
		self.k = len(self.field[0])
		self.dx = self.a / self.n * self.scale
		self.dy = self.a / self.k * self.scale
		self.obzor = scene.camy
		print(self.dx, self.dy)
	def draw(self):
		for i in range(self.n):
			for j in range(self.k):
				if self.field[i][j] == 1:
					canv.create_rectangle(i * self.dx, j * self.dy, (i + 1) * self.dx, (j + 1) * self.dy, fill = 'red')
					canv.update()

		canv.create_line(self.player.position.x * self.a * self.scale / self.n, self.player.position.y * self.a * self.scale / self.k, self.player.position.x * self.a * self.scale / self.n + self.player.look.x * 10 * self.scale, self.player.position.y * self.a * self.scale / self.k + self.player.look.y * 10 * self.scale, width = 5, fill = 'blue')
		



#main body
if __name__ == "__main__":
	s = Scene('scene.cfg')
	a = atan2(s.player.look.x, s.player.look.y)
	frame = 0
	begin = time.time()
	canv.bind("<KeyPress>", move_detect)
	canv.bind("<KeyRelease>", move_undetect)
	mnmp = minimap(s)
	show_minimap = 0
	mnmp.draw()
	time1 = 0

	while True:
		frame += 1
		if frame % 60 == 0:
			print(60 / (time.time() - time1))
			time1 = time.time()
		
		if show_minimap:
			mnmp.draw()
		else:
			s.display()
			player_move()

	root.mainloop()

