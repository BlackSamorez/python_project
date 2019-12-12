from math import *
import time
import tkinter as tk
import os

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('1920x1080')
canv = tk.Canvas(root, bg='grey')
canv.pack(fill=tk.BOTH, expand=1)


def return_dist(ent):
	return ent.dist

def _from_rgb(rgb):  # HEX from rgb
	return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


class Vector2D:  # vectors
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


# Vector operations
def v_abs2(x):
	return x * x


def v_abs(x):
	return sqrt(x * x)


def v_norm(x):
	return x / v_abs(x)


def v_rot(x):
	return Vector2D(-x.y, x.x)


# what we control
class Player:
	def __init__(self, look, position):
		self.look = look
		self.position = position
		self.forward = 0
		self.right = 0
		self.rot = 0
		self.ammo = 100
		self.healt = 100
		self.equip = []
	
	def fire(targets):
		for tar in targets:
			tar.death()


	def apt(event):
		pass


class Entity:
	def __init__(self, position=Vector2D(0, 0), idef = -1):
		self.position = position
		self.dist = 0.5
		self.height = 1
		self.width = 0.5
		self.id = idef
		self.color = [0, 100, 100]
		self.lh = 1
		self.a = 0
		self.altitude = 0.5

	def rotate(self):
		if self.a < 36:
			self.a += 1
		else:
			self.a = 0
		self.width = 0.1 * cos(self.a / 36 * 2 * pi) + 0.4 

		root.after(50, self.rotate)


	def difference(self):
		if self.id == 1:
			self.height = 0.3
			self.width = 0.75 * cos(self.a / 360 * 2 * pi)
			self.color = [200, 0, 0]
			self.widespread = 0.3
			self.altitude = 0.2

		if self.id == 2:
			self.height = 0.3
			self.width = 0.75 * cos(self.a / 360 * 2 * pi)
			self.color = [200, 0, 0]
			self.widespread = 0.6
			self.altitude = 0.2

		elif self.id == 3:
			self.height = 0.8
			self.width = 0.25 * cos(self.a / 360 * 2 * pi)
			self.color = [225, 155, 75]
			self.altitude = 0.4


class target(Entity):
	def death(self):
		for i in range(10):
			self.height = 0.9 * self.height
			self.width = 0.9 * self.width
			for c in range(3):
				self.color[c] = self.color[c] * 0.9




# map object
class Scene:
	def __init__(self, filename=None):
		self.renderwidth = 20
		self.width = 1920
		self.height = 1080
		self.camx = pi / 3
		self.camy = self.camx * 480 / 640
		self.entities = []
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
			if command == 'entity':
				x, y, idef = [int(x) for x in args.split(' ')]
				self.entities += [Entity(Vector2D(x, y), idef)]
		self.lines = 3
		self.color = [[] * 3 for x in range(self.lines)]
		self.edges = [0, 0, 0]
		self.bc = [255, 255, 255]
		self.entity_trace = [[Entity()] for x in range(self.width // self.renderwidth)]

	def target_entities(self):
		self.entity_trace = [[Entity()] for x in range(self.width // self.renderwidth)]
		for ent in self.entities:
			phi = atan2((ent.position.y - self.player.position.y), (ent.position.x - self.player.position.x)) - atan2(
				self.player.look.y, self.player.look.x)
			if phi < self.camx / 2 and phi > - self.camx:
				x_ = int((self.camx / 2 + phi) / self.camx * self.width) // self.renderwidth
				ent.dist = sqrt(
					(ent.position.x - self.player.position.x) ** 2 + (ent.position.y - self.player.position.y) ** 2)
				ent.lh = int(ent.height / (ent.dist + 0.0001) / self.camy * self.height / 2)
				# canv.create_rectangle(x_ * self.renderwidth - self.renderwidth // 2, self.height // 2 - lh , x_ * self.renderwidth + self.renderwidth // 2, self.height // 2 + lh , fill = _from_rgb([int(ent.color[0]), int(ent.color[1]), int(ent.color[2])]))
				deltaphi = int((atan2(ent.width, ent.dist) / self.camx) * self.width / self.renderwidth) // 2
				for i in range(2 * deltaphi):
					if (x_ - deltaphi + i) > -1 and (x_ - deltaphi + i) < (self.width // self.renderwidth):
						self.entity_trace[x_ - deltaphi + i] += [ent]

	def display_cubes(self):
		canv.delete("all")

		canv.create_rectangle(0, self.height // 2, self.width, self.height, fill='black')

		self.edges = [0, 20, 80, 100]
		self.color[0] = [87, 31, 0]
		self.color[1] = [255, 255, 255]
		self.color[2] = [87, 31, 0]
		self.bc = [255, 0, 0]

		x_old = -1
		for x_ in range(int(self.width // self.renderwidth)):
			debug = (x_ == self.width // 2)

			player = self.player
			to = v_norm(
				v_rot(player.look) * sin(self.camx * x_ * self.renderwidth / self.width - 0.5) + player.look * cos(
					self.camx * x_ * self.renderwidth / self.width - 0.5))
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
					brightness = abs(to.x if side == 0 else to.y) / sqrt(perpWallDist)
				else:
					brightness = abs(to.x if side == 0 else to.y)

				if (side == 0):
					wallX = x.y + perpWallDist * to.y;
				else:
					wallX = x.x + perpWallDist * to.x;
				wallX = wallX - int(wallX)
				brightness = brightness * sqrt(abs(cos(x_ * self.renderwidth / (self.width / 2) + pi / 2)))

				self.entity_trace[x_] += [Entity(Vector2D(0,0), 238)]
				self.entity_trace[x_][-1].dist = perpWallDist
				self.entity_trace[x_] = sorted(self.entity_trace[x_], key = return_dist, reverse = True)
				
				for ent in self.entity_trace[x_]:
					if ent.id != -1:
						if ent.dist < 30:
							if ent.id == 238:
								if hit in [0, 1]:
									for i in range(len(self.edges) - 1):
										canv.create_rectangle(x_ * self.renderwidth - self.renderwidth / 2,
															  self.height // 2 - lh + 2 * lh * (self.edges[i] / 100),
															  x_ * self.renderwidth + self.renderwidth / 2,
															  self.height / 2 - lh + 2 * lh * (self.edges[i + 1] / 100),
															  fill=_from_rgb([int(self.color[i][0] * brightness),
																			  int(self.color[i][1] * brightness),
																			  int(self.color[i][2] * brightness)]), outline="")
								if hit == 2:
									canv.create_rectangle(x_ * self.renderwidth - self.renderwidth / 2,
														  self.height // 2 - lh / 2,
														  x_ * self.renderwidth + self.renderwidth / 2,
														  self.height / 2 + lh / 2, fill=_from_rgb(
											[int(self.bc[0] * brightness), int(self.bc[1] * brightness),
											 int(self.bc[2] * brightness)]), outline="")
							else:
								canv.create_rectangle(x_ * self.renderwidth - self.renderwidth // 2,
													  self.height // 2 - ent.lh // 2,
													  x_ * self.renderwidth + self.renderwidth // 2,
													  self.height // 2 + ent.lh // 2, fill=_from_rgb(
										[int(ent.color[0]), int(ent.color[1]), int(ent.color[2])]), outline="")


		canv.update()


# start moving
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


# stop moving
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


# move itself
def player_move():
	global player, a
	if s.player.forward == 1 and s.field[floor(s.player.position.x + s.player.look.x * 0.3)][
		floor(s.player.position.y + s.player.look.y * 0.3)] == -1:
		s.player.position = s.player.position + s.player.look * 0.2

	if s.player.forward == -1 and s.field[floor(s.player.position.x - s.player.look.x * 0.3)][
		floor(s.player.position.y - s.player.look.y * 0.3)] == -1:
		s.player.position = s.player.position - s.player.look * 0.2

	if s.player.right == 1 and s.field[floor(s.player.position.x - v_rot(s.player.look).x * 0.3)][
		floor(s.player.position.y - v_rot(s.player.look).y * 0.3)] == -1:
		s.player.position = s.player.position - v_rot(s.player.look) * 0.2

	if s.player.right == -1 and s.field[floor(s.player.position.x + v_rot(s.player.look).x * 0.3)][
		floor(s.player.position.y + v_rot(s.player.look).y * 0.3)] == -1:
		s.player.position = s.player.position + v_rot(s.player.look) * 0.2

	if s.player.rot == 1:
		a -= 5 / 180 * pi
		s.player.look = Vector2D(cos(a), sin(a))

	if s.player.rot == -1:
		a += 5 / 180 * pi
		s.player.look = Vector2D(cos(a), sin(a))


class minimap():
	def __init__(self, scene, scenewidth=0, sceneheight=0):
		self.war_mist = 0
		self.scale = 2
		self.a = 500
		self.player = scene.player
		self.field = scene.field
		self.n = len(self.field)
		self.k = len(self.field[0])
		self.dx = self.a / self.n * self.scale
		self.dy = self.a / self.k * self.scale
		self.obzor = scene.camy

	def draw(self):
		for i in range(self.n):
			for j in range(self.k):
				if self.war_mist:
					if self.field[i][j] not in [-1, 0]:
						canv.create_rectangle(i * self.dx, j * self.dy, (i + 1) * self.dx, (j + 1) * self.dy,
											  fill='red')
					if self.field[i][j] == 2:
						canv.create_rectangle(i * self.dx, j * self.dy, (i + 1) * self.dx, (j + 1) * self.dy,
											  fill='blue')
				else:
					if self.field[i][j] != -1:
						canv.create_rectangle(i * self.dx, j * self.dy, (i + 1) * self.dx, (j + 1) * self.dy,
											  fill='red')
					if self.field[i][j] == 2:
						canv.create_rectangle(i * self.dx, j * self.dy, (i + 1) * self.dx, (j + 1) * self.dy,
											  fill='blue')

		canv.create_line(self.player.position.x * self.a * self.scale / self.n,
						 self.player.position.y * self.a * self.scale / self.k,
						 self.player.position.x * self.a * self.scale / self.n + self.player.look.x * 10 * self.scale,
						 self.player.position.y * self.a * self.scale / self.k + self.player.look.y * 10 * self.scale,
						 width=5, fill='blue')
		canv.update()


# main body


if __name__ == "__main__":
	os.system('python3 auto_generator.py')
	s = Scene('scene.cfg')
	a = atan2(s.player.look.x, s.player.look.y)
	s.entities += [Entity(s.player.position + Vector2D(1, 1))]
	s.entities[len(s.entities) - 1].id = 0
	for ent in s.entities:
		ent.difference()
		ent.rotate()
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
			time.sleep(0.5)
		else:
			s.target_entities()
			s.display_cubes()
			player_move()

	root.mainloop()
