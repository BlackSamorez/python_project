from math import *
import time
from random import randrange as rnd,choice
import tkinter as tk


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
		self.targeted = Vector2D(0, 0)
		self.trap_coord = [0, 0, 0, 0]
		

	def display(self):
		special = 0
		x_old = -1
		x_ = 0
		schitat = 0
		veiw = 0
		while x_ < self.width:
			if x_ < 0: 
				x_ = 0
			to = v_norm(v_rot(self.player.look) * sin(self.camx * x_ / self.width - self.camx / 2) + self.player.look * cos(self.camx * x_ / self.width - self.camx / 2))
			
			tan = atan2(to.y, to.x)
			x = floor(self.player.position.x)
			y = floor(self.player.position.y)
			i = 0
			self.targeted = Vector2D(-1, -1)
			targetx = [1000, 1000]
			targety = [1000, 1000]
			if to.x > 0:
				i = 0
				while x + i + 1 < self.fw and y + floor(tan * i) < self.fh and y + floor(tan * i) > 0:
					if self.field[x + i][y + floor(tan * i)] != -1:
						targetx = [int(x + i), y + floor(tan * i)]
						schitat = 1
						break
					i +=1
				i = 0
				while y + i + 1 < self.fh and x + floor(i / tan) < self.fw and x + floor(i / tan) > 0:
					if self.field[x + floor(i / tan)][y + i] != -1:
						targety = [x + floor(i / tan), int(y + i)]
						schitat = 1
						break
					i +=1

				if targetx[0] < targety[0]:
					self.targeted = Vector2D(targetx[0], targetx[1])
					
				else:
					self.targeted = Vector2D(targety[0], targety[1])
			else:
				i = 0
				while x + i - 1 > 0 and y + floor(tan * i) > 0 and y + floor(tan * i) < self.fh:
					if self.field[x + i][y + floor(tan * i)] != -1:
						targetx = [int(x + i), y + floor(tan * i)]
						schitat = 1
						break
					i = i - 1
				i = 0
				while y + i - 1 > 0 and x + floor(i / tan) > 0 and x + floor(i / tan) < self.fw:
					if self.field[x + floor(i / tan)][y + i] != -1:
						targety = [x + floor(i / tan), int(y + i)]
						schitat = 1
						break
					i = i - 1

				if targetx[0] < targety[0]:
					self.targeted = Vector2D(targetx[0], targetx[1])
					
				else:
					self.targeted = Vector2D(targety[0], targety[1])
				if speccial != 1:
					special = 1
					canv.create_line(x_ , 0, x_ , 400, fill = 'blue', width = 10)

	
			if schitat:
				#print(self.targeted)
				self.targeted = self.targeted - self.player.position
				sasas = 0
				if self.targeted.x + 0.5 > 0:
					if self.targeted.y + 0.5 > 0:
						print(1)
						sasas = 1
						trap1 = (atan2(self.targeted.y, self.targeted.x + 1) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist1 = v_abs(self.targeted + Vector2D(1, 0))
						trap2 = (atan2(self.targeted.y, self.targeted.x) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist2 = v_abs(self.targeted + Vector2D(0, 0))
						trap3 = (atan2(self.targeted.y + 1, self.targeted.x) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist3 = v_abs(self.targeted + Vector2D(0, 1))
					else:
						print(2)
						sasas = 2
						trap1 = (atan2(self.targeted.y, self.targeted.x) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist1 = v_abs(self.targeted + Vector2D(0, 0))
						trap2 = (atan2(self.targeted.y + 1, self.targeted.x) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist2 = v_abs(self.targeted + Vector2D(0, 1))
						trap3 = (atan2(self.targeted.y + 1, self.targeted.x + 1) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist3 = v_abs(self.targeted + Vector2D(1, 1))
				else:
					if self.targeted.y > 0:
						print(3)
						sasas = 3
						trap1 = (atan2(self.targeted.y + 1, self.targeted.x + 1) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist1 = v_abs(self.targeted + Vector2D(1, 1))
						trap2 = (atan2(self.targeted.y, self.targeted.x + 1) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist2 = v_abs(self.targeted + Vector2D(1, 0))
						trap3 = (atan2(self.targeted.y, self.targeted.x) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist3 = v_abs(self.targeted + Vector2D(0, 0))

					else:
						print(4)
						sasas = 4
						trap1 = (atan((self.targeted.y + 1) / self.targeted.x) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist1 = v_abs(self.targeted + Vector2D(0, 1))
						trap2 = (atan((self.targeted.y + 1) /  (self.targeted.x + 1)) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist2 = v_abs(self.targeted + Vector2D(1, 1))
						trap3 = (atan(self.targeted.y / (self.targeted.x + 1)) - atan2(self.player.look.y, self.player.look.x)) * self.width / (self.camx / 2) + self.width / 2
						dist3 = v_abs(self.targeted + Vector2D(1, 0))


				
				trap1, trap2, trap3 = sorted([trap1, trap2, trap3])
				mass = sorted([trap1, trap2, trap3])

				print(sasas)

				h1 = atan2(0.5, dist1) / (self.camy / 2) * self.height
				h2 = atan2(0.5, dist2) / (self.camy / 2) * self.height
				h3 = atan2(0.5, dist3) / (self.camy / 2) * self.height

				if 0 == 0:
					canv.create_polygon((trap1), (self.height / 2 + h1), (trap2), (self.height / 2 + h2), (trap2), (self.height / 2 - h2), (trap1), (self.height / 2 - h1), outline="black", fill = 'red', width = 1)
					canv.create_polygon((trap2), (self.height / 2 + h2), (trap3), (self.height / 2 + h3), (trap3), (self.height / 2 - h3), (trap2), (self.height / 2 - h2), outline="black", fill = 'red', width = 1)
					#canv.create_line(trap3, 0, trap3, 400, fill = 'green')
					x_ = trap3 + 1
					#print(x_)
					#canv.create_line(x_, 0, x_ + 10, 400, fill = 'green')
					schitat = 0
				
			
			x_ += 1
			canv.create_line(x_ , 0, x_ , 400, fill = 'green')
			
			
			


			'''if side == 0:
				perpWallDist = (mapX - x.x + (1 - stepX) / 2) / to.x;
			else:
				perpWallDist = (mapY - x.y + (1 - stepY) / 2) / to.y;
			lh = int(1 / (perpWallDist + 0.0001) / self.camy * self.height / 2)'''


		canv.update()
		time.sleep(0.01)
		canv.delete("all")
			


		


#start moving
def move_detect(event):
	global s, show_minimap
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
	global s, a, show_minimap

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
	global s, a
	if s.player.forward == 1 and s.field[floor(s.player.position.x + s.player.look.x * 1)][floor(s.player.position.y + s.player.look.y * 1)] == -1:
		s.player.position = s.player.position + s.player.look * 0.1
	
	if s.player.forward == -1 and s.field[floor(s.player.position.x - s.player.look.x * 1)][floor(s.player.position.y - s.player.look.y * 1)] == -1:
		s.player.position = s.player.position - s.player.look * 0.1

	if s.player.right == 1 and s.field[floor(s.player.position.x - v_rot(s.player.look).x * 1)][floor(s.player.position.y - v_rot(s.player.look).y * 1)] == -1:
		s.player.position = s.player.position - v_rot(s.player.look) * 0.1
	
	if s.player.right == -1 and s.field[floor(s.player.position.x + v_rot(s.player.look).x * 1)][floor(s.player.position.y + v_rot(s.player.look).y * 1)] == -1:
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
			#print(60 / (time.time() - time1))
			time1 = time.time()
		
		if show_minimap:
			mnmp.draw()
		else:
			s.display()
			player_move()

	root.mainloop()

