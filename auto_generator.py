import time
import tkinter as tk
from math import *
from random import randrange as rnd, choice


# названия коррелируют с graphics, сначала прочтите комментарии к нему

class entity():
    def __init__(self, position=[0, 0], idef=-1):
        self.position = position
        self.id = idef


def exit():  # записть в файл
    global field, name, n, k, p_n, p_k
    with open(name, 'w') as file:
        file.write(str(6 * n + 1))  # размеры карты
        file.write(' ')
        file.write(str(6 * k + 1))
        file.write('\n')
        file.write('player 1 1 ')  # layer and his look
        file.write(str(p_n))  # his coordinates
        file.write(' ')
        file.write(str(p_k))
        for i in range(6 * n + 1):
            for j in range(6 * k + 1):
                if field[i][j] != -1:  # for all map if not air
                    file.write('\n')
                    file.write('brick ')
                    file.write(str(i))
                    file.write(' ')
                    file.write(str(j))
                    file.write(' ')
                    file.write(str(field[i][j]))
        for ent in entities:  # for all targets and entities
            if ent.id != 238:  # id = 238 indicates a target
                file.write('\n')
                file.write('entity ')
                file.write(str(6 * ent.position[0] + 3))
                file.write(' ')
                file.write(str(6 * ent.position[1] + 3))
                file.write(' ')
                file.write(str(ent.id))
            else:  # else an entity
                file.write('\n')
                file.write('target ')
                file.write(str(ent.position[0]))
                file.write(' ')
                file.write(str(ent.position[1]))
                file.write(' ')
                file.write(str(2))


def import_rooms():  # read rooms from files
    room = [[[-1] * 13 for x in range(11)] for y in range(11)]
    for i in range(12):
        with open(('rooms/room' + str(i + 1) + '.cfg'), 'r') as file:
            s = file.read()

        for line in s.split('\n')[1:]:

            command, args = line.split(' ', 1)
            if command == 'brick':
                x, y, tid = [int(x) for x in args.split(' ')]
                room[x][y][i + 1] = tid

    return room


def create_floor():  # fill floor with rooms
    global field, name, n, k, player, dx, dy, percentage, boss_n, boss_k, subfield, p_n, p_k

    room = import_rooms()

    field = [[-1] * (6 * n + 1) for x in range(((k * 6) + 1))]
    subfield = [[-1] * n for x in range(k)]  # subfield comtaining room id for each 6x6 sqare

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

    for a in range(n):  # room boundaries
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

    for a in range(n):
        for b in range(k):
            if subfield[a][b] == -1:
                subfield[a][b] = rnd(1, 7)  # random 5x5 room
                if a != n - 1 and b != k - 1:
                    luck = rnd(1, 100)
                    if luck > percentage:
                        subfield[a][b] = rnd(1, 7)
                    else:
                        subfield[a][b] = rnd(8, 12)  # random generating bigger rooms

                if subfield[a][b] in [8, 9, 10, 11, 12]:  # if room is big
                    subfield[a + 1][b] = subfield[a][b]
                    subfield[a + 1][b + 1] = subfield[a][b]
                    subfield[a][b + 1] = subfield[a][b]

                    for l in range(11):  # writing a romm into field
                        for m in range(11):
                            field[(6 * a + 1) + l][(6 * b + 1) + m] = room[l][m][subfield[a][b]]

                if subfield[a][b] in [1, 2, 3, 4, 5, 6, 7]:  # writing a romm into field
                    for l in range(5):
                        for m in range(5):
                            z = room[l][m][subfield[a][b]]
                            field[(6 * a + 1) + l][(6 * b + 1) + m] = z

    boss_n = rnd(0, n - 3)  # random boss room coordinates
    boss_k = rnd(0, k - 3)
    for i in range(17):
        for j in range(17):
            field[6 * boss_n + i + 1][6 * boss_k + j + 1] = -1  # clearing boss room

    room_counter = level_cut()  # cutting the level

    field[6 * boss_n + 9][6 * boss_k + 9] = 2  # boss portal

    if room_counter < n * k * 0.3 or room_counter > n * k * 0.6:  # if cutting is bad start again
        create_floor()


def level_cut():  # cut a level
    global field, name, n, k, player, dx, dy, percentage, subfield, boss_n, boss_k, p_n, p_k, cutting_edge, ent_chance, ent_types, entities, tar_chance
    reachable = []  # list of reachable rooms
    room_counter = 0  # counting rooms
    for i in range(n):
        for j in range(k):
            if rnd(0, 100) < cutting_edge:
                field[6 * i + 3][6 * j] = 0
                field[6 * i][6 * j + 3] = 0  # placing walls in arcs

    reachable += [[boss_n, boss_k]]
    reachable += [[boss_n, boss_k + 1]]
    reachable += [[boss_n, boss_k + 2]]
    reachable += [[boss_n + 1, boss_k]]
    reachable += [[boss_n + 1, boss_k + 1]]
    reachable += [[boss_n + 1, boss_k + 2]]
    reachable += [[boss_n + 2, boss_k]]
    reachable += [[boss_n + 2, boss_k + 1]]
    reachable += [[boss_n + 2, boss_k + 1]]  # boss room is reachable
    far_end = [0, 0]  # where player is to be placed

    for room in reachable:  # if you can reach neighbor rooms they become reachable

        if not ((room[0] in [0, n - 1]) and (room[1] in [0, k - 1])):
            if room[0] != 0:
                if (field[6 * room[0]][6 * room[1] + 3] == -1 or field[6 * room[0]][6 * room[1] + 4] == -1) and (
                        [room[0] - 1, room[1]] not in reachable):
                    reachable += [[room[0] - 1, room[1]]]
                    far_end = [room[0] - 1, room[1]]
                    room_counter += 1

            if room[0] != n - 1:
                if (field[6 * room[0] + 6][6 * room[1] + 3] == -1 or field[6 * room[0] + 6][
                    6 * room[1] + 4] == -1) and ([room[0] + 1, room[1]] not in reachable):
                    reachable += [[room[0] + 1, room[1]]]
                    far_end = [room[0] + 1, room[1]]
                    room_counter += 1

            if room[1] != k - 1:
                if (field[6 * room[0] + 3][6 * room[1] + 6] == -1 or field[6 * room[0] + 4][
                    6 * room[1] + 6] == -1) and ([room[0], room[1] + 1] not in reachable):
                    reachable += [[room[0], room[1] + 1]]
                    far_end = [room[0], room[1] + 1]
                    room_counter += 1

            if room[1] != 0:
                if (field[6 * room[0] + 3][6 * room[1]] == -1 or field[6 * room[0] + 4][6 * room[1]] == -1) and (
                        [room[0], room[1] - 1] not in reachable):
                    reachable += [[room[0], room[1] - 1]]
                    far_end = [room[0], room[1] - 1]
                    room_counter += 1

    field[6 * far_end[0] + 3][6 * far_end[1] + 3] = -1
    p_n = 6 * far_end[0] + 3
    p_k = 6 * far_end[1] + 3  # clear space for the player and place him

    for i in range(n):
        for j in range(k):
            if ([i, j] not in reachable):
                for m in range(7):
                    for l in range(7):
                        field[6 * i + m][6 * j + l] = 0  # fill not reachable wit walls

    for i in range(6 * k - 1):
        if field[0][i] in [0, -2] and field[i + 2][0] in [0, -2] and field[1][i + 1] in [0, -2] and field[1][i] in [0,
                                                                                                                    -2] and \
                field[1][i + 2] in [0, -2]:
            field[0][i + 1] = -2

        if field[6 * k][i] in [0, -2] and field[6 * k][i + 2] in [0, -2] and field[6 * k - 1][i + 1] in [0, -2] and \
                field[6 * k - 1][i] in [0, -2] and field[6 * k - 1][i + 2] in [0, -2]:
            field[6 * k][i + 1] = -2

    for i in range(6 * n - 1):
        if field[i][0] in [0, -2] and field[i + 2][0] in [0, -2] and field[i + 1][1] in [0, -2] and field[i][1] in [0,
                                                                                                                    -2] and \
                field[i + 2][1] in [0, -2]:
            field[i + 1][0] = -2

        if field[i][6 * k] in [0, -2] and field[i + 2][6 * k] in [0, -2] and field[i + 1][6 * k - 1] in [0, -2] and \
                field[i][6 * k - 1] in [0, -2] and field[i + 2][6 * k - 1] in [0, -2]:
            field[i + 1][6 * k] = -2

    for i in range(1, 6 * n):
        for j in range(1, 6 * k):
            if field[i][j + 1] in [0, -2] and field[i + 1][j] in [0, -2] and field[i][j - 1] in [0, -2] and \
                    field[i - 1][j] in [0, -2] and field[i - 1][j - 1] in [0, -2] and field[i - 1][j + 1] in [0, -2] and \
                    field[i + 1][j - 1] in [0, -2] and field[i + 1][j + 1] in [0, -2]:
                field[i][j] = -2

    for i in range(6 * n + 1):
        for j in range(6 * k + 1):
            if field[i][j] == -2:
                field[i][j] = -1  # make walls with no air around air

    if [0, 0] not in reachable:
        field[0][0] = -1
    if [0, k - 1] not in reachable:
        field[0][6 * k] = -1
    if [n - 1, 0] not in reachable:
        field[6 * n][0] = -1
    if [n - 1, k - 1] not in reachable:
        field[6 * n][6 * k] = -1

    for room in reachable:
        if loot_chance > rnd(1, 100):  # loot chance - chance of entity spawning in the middle of a room
            rndid = 1
            entities += [entity(room, rndid)]
            field[6 * room[0] + 3][6 * room[1] + 3] = -1  # spawn entities

    for room in reachable:
        for l in range(6):
            for m in range(6):
                if field[6 * room[0] + l][6 * room[1] + m] == -1:
                    if tar_chance > rnd(0, 100):  # tar_chance - chance of target spawning in air in reachable room
                        entities += [entity([6 * room[0] + l, 6 * room[1] + m], 238)]  # spawn enemies

    return room_counter

def main():
    global entities, name, percentage, n, k, cutting_edge, loot_chance, tar_chance
    entities = []
    name = 'scene.cfg'
    percentage = 90
    n = 8  # rooms by x
    k = 8  # rooms by y
    cutting_edge = 80
    loot_chance = 10  # loot chance - chance of entity spawning in the middle of a room
    # ent_types = 4
    tar_chance = 3  # tar_chance - chance of target spawning in air in reachable room

    create_floor()
    exit()
