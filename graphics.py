import os
import sys
import time
import tkinter as tk
from PIL import ImageTk, Image
from math import *

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('1280x720')
canv = tk.Canvas(root, bg='grey')
canv.pack(fill=tk.BOTH, expand=1)


def return_dist(ent):  # Возвращает расстояние до объекта, используется для сортировки видимых объектов по расстоянию
    return ent.dist


def _from_rgb(rgb):  # возвращает HEX, нужный для tkinter из списка gb формата
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


class Vector2D:  # 2D вектора со сложением, вычитанием, делением на число, скалярным произведением, псевдовекторным произв и возвратом строки
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


# Операции на векторах:
# Квадрат
def v_abs2(x):
    return x * x


# Модуль
def v_abs(x):
    return sqrt(x * x)


# нормировка
def v_norm(x):
    return x / v_abs(x)


# поворот на 90гр
def v_rot(x):
    return Vector2D(-x.y, x.x)


# класс объекта в инвентаре
class inv():
    def __init__(self, idef):
        self.id = idef


# Класс pc
class Player:
    def __init__(self, look, position):
        self.look = look  # куда смотрит
        self.position = position  # координата
        self.forward = 0  # состояния движения
        self.right = 0
        self.rot = 0
        self.ammo = 100  # запас боеприпасов (не используется)
        self.hpoints = 50  # запас hp
        self.equip = []  # инвентарь
        self.killcount = 0

    def fire(self, targets):  # стрельба по противникам
        for tar in targets:  # список противников, которые умрут
            if tar.id != -1:    
                tar.death()
                self.killcount += 1

    def heal(self):  # приминение аптечки
        for loot in self.equip:
            if loot.id == 1:  # 1 - аптечка
                loot.id = -1
                self.hpoints = 100
                break


class Entity:  # Класс сущностей: аптечки, parent противников, etc
    def __init__(self, position=Vector2D(0, 0), idef=-1):
        self.position = position  # coordinates (assumed Vector2D)
        self.dist = 0.5  # distance to player
        self.height = 1
        self.width = 0.5
        self.id = idef
        self.color = [0, 100, 100]
        self.lh = 1  # height in pixels on screen, depends on relative position
        self.a = 0
        self.altitude = 0.5  # not used
        self.__name__ = 'Entity'  # name

    def rotate(self):  # oscillationc, visual effect
        if self.id == 1:
            if self.a < 36:
                self.a += 1
            else:
                self.a = 0
            self.width = 0.1 * cos(self.a / 36 * 2 * pi) + 0.4
            root.after(50, self.rotate)

    def difference(self):  # differentiate based on id
        if self.id == 1:  # first aid kit
            self.height = 0.3
            self.width = 0.3 * cos(self.a / 360 * 2 * pi)
            self.color = [200, 0, 0]
            self.altitude = 0.2

        if self.id == 2:  # supplementary
            self.height = 0.3
            self.width = 0.75 * cos(self.a / 360 * 2 * pi)
            self.color = [200, 200, 0]
            self.widespread = 0.6
            self.altitude = 0.2

        elif self.id == 3:  # supplementary
            self.height = 0.8
            self.width = 0.25 * cos(self.a / 360 * 2 * pi)
            self.color = [225, 155, 75]
            self.altitude = 0.4


class Target(Entity):  # Enemies
    def __init__(self, position=Vector2D(0, 0), idef=-1):
        super(Target, self).__init__(position, idef)
        self.__name__ = 'Target'
        self.breath = 10  # how fast they die

    def death(self):
        if self.breath > 0:
            self.breath -= 1
            self.height = 0.9 * self.height  # they shrink and disappear
            self.width = 0.9 * self.width
            for c in range(3):
                self.color[c] = self.color[c] * 0.9
            root.after(50, self.death)
        else:
            self.id = -1  # id = -1 to be ignored by the programm

    def attack(self, player):
        self.position -= ((self.position - player.position) * 0.01)  # they get closer and kill you
        if self.dist < 0.7:
            player.hpoints -= 1


class Scene:  # the game itself
    def __init__(self, filename=None):
        self.renderwidth = 40
        self.width = 1280  # x screen resolution
        self.height = 720  # y screen resolution
        self.camx = pi / 3  # horizontal FOW
        self.camy = self.camx * self.height / self.width  # vertical FOW
        self.entities = []  # scene contains all entities
        with open(filename, 'r') as file:
            s = file.read()  # reading scene.cfg containig map, entitties and targets
        self.fw, self.fh = [int(x) for x in s.split('\n')[0].split(' ')]  # map size x and y
        self.field = [[-1] * self.fh for x in range(self.fw)]  # sqared map, -1 = air, 0 = wall, 2 = portal
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
            if command == 'target':
                x, y, idef = [int(x) for x in args.split(' ')]
                self.entities += [Target(Vector2D(x, y), idef)]
        self.lines = 3  # nuber of horizontal lines making a wall
        self.color = [[] * self.lines for x in range(self.lines)]  # list of colors for each line
        self.edges = [0] * self.lines  # line edge positions (0 assumed)
        self.bc = [255, 255, 255]  # portal color
        self.entity_trace = [[Entity()] for x in range(self.width // self.renderwidth)]  # list of entities on each ray
        self.targets = []  # list of targets

    def target_entities(self):
        self.being_targeted = []  # list of targets that see you
        self.targets = []  # list of targets that you see
        self.entity_trace = [[Entity()] for x in
                             range(self.width // self.renderwidth)]  # list of entities on each ray casted
        for ent in self.entities:
            phi = atan2((ent.position.y - self.player.position.y), (ent.position.x - self.player.position.x)) - atan2(
                self.player.look.y, self.player.look.x)  # angle to entity
            if phi < self.camx / 2 and phi > - self.camx:  # if visible
                x_ = int((self.camx / 2 + phi) / self.camx * self.width) // self.renderwidth  # position on screen
                ent.dist = sqrt(
                    (ent.position.x - self.player.position.x) ** 2 + (ent.position.y - self.player.position.y) ** 2)
                ent.lh = int(ent.height / (ent.dist + 0.0001) / self.camy * self.height / 2)
                deltaphi = int((atan2(ent.width, ent.dist) / self.camx) * self.width / self.renderwidth) // 2
                for i in range(2 * deltaphi):
                    if (x_ - deltaphi + i) > -1 and (x_ - deltaphi + i) < (self.width // self.renderwidth):
                        self.entity_trace[x_ - deltaphi + i] += [ent]  # if visible - make all corresponding rays hit it
            if (ent.__name__ == 'Target') and (phi < pi / 32) and (phi > - pi / 32):
                self.targets += [ent]  # angles within wich targert will die
            if ent.__name__ == 'Entity' and ent.id == 1 and ent.dist < 0.3:
                self.player.equip += [inv(1)]
                ent.id = -1  # pick first aid kit up and make it disappear

    def get_lh(self, x_):  # get block height in pixels on screen (geometry inside(TM))
        player = self.player
        to = v_norm(
            v_rot(player.look) * sin(self.camx * x_ / self.width - 0.5) + player.look * cos(
                self.camx * x_ / self.width - 0.5))
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
            # wallX = wallX - int(wallX)
            # brightness = brightness * sqrt(abs(cos(x_ * self.renderwidth / (self.width / 2) + pi / 2)))

            return lh

    def display_cubes(self):  # not only cubes actually, also targets and entities
        canv.delete("all")

        canv.create_rectangle(0, self.height // 2, self.width, self.height, fill='black')  # floor

        self.edges = [0, 20, 80, 100]
        self.color[0] = [87, 31, 0]
        self.color[1] = [255, 255, 255]
        self.color[2] = [87, 31, 0]
        self.bc = [255, 0, 0]

        for x_ in range(int(self.width // self.renderwidth)):

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
                coss = abs(to.x if side == 0 else to.y)

                self.entity_trace[x_] += [
                    Entity(Vector2D(0, 0), 238)]  # flase entity, actually a wall (to sort wall with entities)
                self.entity_trace[x_][-1].dist = perpWallDist
                self.entity_trace[x_] = sorted(self.entity_trace[x_], key=return_dist,
                                               reverse=True)  # from closest to farthest
                walled = False  # havent found a wall yet

                for ent in self.entity_trace[x_]:
                    if ent.id != -1:
                        if ent.dist < 30:  # dont see farther
                            if ent.id == 238:  # if wall
                                if hit in [0, 1, 2]:  # a wall or id = 1 (not used (yet?))
                                    step = self.renderwidth / int(1 + 2 / (coss))  # render step
                                    # print(int(1 + 2 / (coss)))
                                    for n in range(int(1 + 2 / (coss))):  # for each step
                                        lh = self.get_lh(
                                            x_ * self.renderwidth - self.renderwidth / 2 + n * step)  # get height for each step

                                        for i in range(len(self.edges) - 1):
                                            canv.create_rectangle(
                                                x_ * self.renderwidth - self.renderwidth / 2 + n * step,
                                                self.height // 2 - lh + 2 * lh * (self.edges[i] / 100),
                                                x_ * self.renderwidth - self.renderwidth / 2 + (n + 1) * step,
                                                self.height / 2 - lh + 2 * lh * (self.edges[i + 1] / 100),
                                                fill=_from_rgb([int(self.color[i][0] * brightness),
                                                                int(self.color[i][1] * brightness),
                                                                int(self.color[i][2] * brightness)]),
                                                outline="")  # create part of a wall

                                '''if hit == 2:  # a portal
                                    canv.create_rectangle(x_ * self.renderwidth - self.renderwidth / 2,
                                                          self.height // 2 - lh / 2,
                                                          x_ * self.renderwidth + self.renderwidth / 2,
                                                          self.height / 2 + lh / 2, fill=_from_rgb(
                                            [int(self.bc[0] * brightness), int(self.bc[1] * brightness),
                                             int(self.bc[2] * brightness)]), outline="")'''
                                walled = True  # we have hitten a wall
                            else:
                                canv.create_rectangle(x_ * self.renderwidth - self.renderwidth // 2,
                                                      self.height // 2 - ent.lh // 2,
                                                      x_ * self.renderwidth + self.renderwidth // 2,
                                                      self.height // 2 + ent.lh // 2, fill=_from_rgb(
                                        [int(ent.color[0]), int(ent.color[1]), int(ent.color[2])]),
                                                      outline="")  # part of entity
                                if walled and ent not in self.being_targeted and ent.__name__ == 'Target':  # if we see it after after wall - they see us
                                    self.being_targeted += [ent]

        H.draw(self.player)  # draw hp bar
        canv.create_polygon(0.8 * self.width, self.height, 0.65 * self.width, 0.8 * self.height, 0.65 * self.width, 0.6 * self.height, self.width, 0.95 * self.height, self.width, self.height,  fill = 'red', outline = 'black')
        canv.create_polygon(self.width, 0.95 * self.height, 0.65 * self.width, 0.6 * self.height, 0.75 * self.width, 0.6 * self.height, self.width, 0.75 * self.height,  fill = 'red', outline = 'black')
        canv.create_polygon(0.8 * self.width, self.height, 0.75 * self.width, (1 - 0.2 / 3) * self.height, 0.72 * self.width, self.height, fill = 'grey', outline = 'black')


        canv.update()


# start moving
def move_detect(event):
    global player, show_minimap, hminus, hplus
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

    if event.char == '-':
        hminus -= 1

    if event.char == '=':
        hplus += 1


# stop moving
def move_undetect(event):
    global player, a, show_minimap, hminus, hplus

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

    if event.char == '-':
        hminus = 0

    if event.char == '=':
        hplus = 0

    if event.char == 'h':  # use first aid kit
        s.player.heal()


# move itself (separated for synchronisation of movement)
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


def shoot(event):  # shoot
    global s
    s.player.fire(s.targets)
    shoot_animation()
    
def shoot_animation():
    global s
    ray = canv.create_line(s.width / 2, s.height / 2, s.width * 0.65, s.height * 0.65, fill = 'green', width = 10)
    canv.update()
    root.after(100, shoot_unanimation)

def shoot_unanimation():
    global s
    try:
    	canv.delete(ray)
    	canv.update()
    except:
    	pass
    

def attack():  # make targets kill us
    global s
    for tar in s.being_targeted:
        tar.attack(s.player)


class minimap():  # minimap
    def __init__(self, scene, scenewidth=0, sceneheight=0):
        self.war_mist = 0
        self.scale = 1
        self.a = 500
        self.player = scene.player
        self.field = scene.field
        self.n = len(self.field)
        self.k = len(self.field[0])
        self.dx = self.a / self.n * self.scale
        self.dy = self.a / self.k * self.scale
        self.obzor = scene.camy
        self.const = 1150

    def draw(self):
        for i in range(self.n):
            for j in range(self.k):
                if self.war_mist:
                    if self.field[i][j] != -1 and self.field[i][j] != 0:
                        canv.create_rectangle(-380 + i * self.dx + self.const, j * self.dy, -380 + (i + 1) * self.dx + self.const,
                                              (j + 1) * self.dy, fill='#00acb4')
                    if self.field[i][j] == 2:
                        canv.create_rectangle(-380 + i * self.dx + self.const, j * self.dy, -380 + (i + 1) * self.dx + self.const,
                                              (j + 1) * self.dy, fill='red')
                else:
                    if self.field[i][j] != -1:
                        canv.create_rectangle(-380 + i * self.dx + self.const, j * self.dy, -380 + (i + 1) * self.dx + self.const,
                                              (j + 1) * self.dy, fill='#00acb4')
                    if self.field[i][j] == 2:
                        canv.create_rectangle(-380 + i * self.dx + self.const, j * self.dy, -380 + (i + 1) * self.dx + self.const,
                                              (j + 1) * self.dy, fill='red')

        canv.create_line(-380 + self.const + self.player.position.x * self.a * self.scale / self.n,
                         self.player.position.y * self.a * self.scale / self.k,
                         -380 + self.const + self.player.position.x * self.a * self.scale / self.n + self.player.look.x * 10 * self.scale,
                         self.player.position.y * self.a * self.scale / self.k + self.player.look.y * 10 * self.scale,
                         width=5, fill='red')
        canv.update()


class health():  # a health bar
    def __init__(self):
        self.hpoints = 50

    def draw(self, player):
        self.hpoints = player.hpoints
        canv.create_rectangle(x, y, x + 360, y + 90, fill='#00acb4')
        canv.create_rectangle(x + 30, y + 30, x + 330, y + 60, fill='#10455b')
        canv.create_rectangle(x + 30, y + 30, x + 30 + self.hpoints * 3, y + 60, fill='red')
        word = 0
        for i in player.equip:
            if i.id == 1:
                word += 1
        line = 'First aid: ' + str(word) + ' kills: ' + str(player.killcount)
        canv.create_text(x + 200, y + 15, text=line, font=('Courier', 18), fill='black')

    # canv.create_text(x + 90, y + 15, text='HEALTH', font=('Courier', 25), fill='black')
    def dead(self):
        if self.hpoints < 0:  # you died
            return True
        else:
            return False

        # main body


if __name__ == "__main__":
    s = Scene('scene.cfg')  # our scene
    a = atan2(s.player.look.x, s.player.look.y)  # player look angle
    # s.entities += [Entity(s.player.position + Vector2D(1, 1))]
    # s.entities[len(s.entities) - 1].id = 0
    for ent in s.entities:
        ent.difference()  # make em' different
        ent.rotate()  # begin Infinite Rotation (part 7 best)
    frame = 0
    begin = time.time()  # the beggining of time
    canv.bind("<space>", shoot)  # shoot on spacebar
    canv.bind("<KeyPress>", move_detect)  # walk, rotate, map, heal
    canv.bind("<KeyRelease>", move_undetect)  # unwalk, unrotate
    mnmp = minimap(s)  # our minimap
    show_minimap = 0  # do we see it
    mnmp.draw()
    time1 = -1  # last step time
    hplus, hminus, x, y = 0, 0, 0, 0
    H = health()  # our healthbar

    while True:  # Да, нормальные люди так не делают, знаю. Может позже исправлю это
        frame += 1
        if frame % 60 == 0:
            # print(60 / (time.time() - time1))
            time1 = time.time()

        if show_minimap:
            mnmp.draw()
            time.sleep(0.5)
        else:
            if hplus:
                H.hpoints += 1
            if hminus:
                H.hpoints -= 1
            s.target_entities()
            s.display_cubes()
            player_move()
            attack()

            if H.dead():
                break  # смерть

    im_10 = Image.open("images/you_died.png")
    image_10 = ImageTk.PhotoImage(im_10)
    canv.create_image(int(s.width / 2), int(s.height / 2),
                      image=image_10)  # Ученые узнали что люди видят после смерти...
    if sys.platform.startswith('linux'):
        os.system('firefox https://www.youtube.com/watch?v=dQw4w9WgXcQ^C')

    root.mainloop()
