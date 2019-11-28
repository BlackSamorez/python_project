from math import sqrt

class Vector2D:
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

def v_abs2(x):
	return x * x
def v_abs(x):
	return sqrt(x * x)
def v_norm(x):
	return x / v_abs(x)
def v_rot(x):
	return Vector2D(-x.y, x.x)

class Player:
	def __init__(self, look, position, health):
		self.look = look
		self.position = position
		self.health = health
		self.forward = 0
		self.right = 0
		self.rot = 0

PLAYER_HEALTH_DEFAULT = 100

