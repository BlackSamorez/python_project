from math import *
import time
from random import randrange as rnd, choice
import tkinter as tk

class entity():
    def __init__(self, position = [0, 0], idef = -1):
        self.position = position
        self.id = idef

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
                if field[i][j] != -1:
                    file.write('\n')
                    file.write('brick ')
                    file.write(str(i))
                    file.write(' ')
                    file.write(str(j))
                    file.write(' ')
                    file.write(str(field[i][j]))
        for ent in entities:
            file.write('\n')
            file.write('entity ')
            file.write(str(6 * ent.position[0] + 3))
            file.write(' ')
            file.write(str(6 * ent.position[1] + 3))
            file.write(' ')
            file.write(str(ent.id))


def import_rooms():
    room = [[[-1] * 13 for x in range(11)] for y in range(11)]
    for i in range(12):
        with open(('room' + str(i + 1) + '.cfg'), 'r') as file:
            s = file.read()

        for line in s.split('\n')[1:]:

            command, args = line.split(' ', 1)
            if command == 'brick':
                x, y, tid = [int(x) for x in args.split(' ')]
                room[x][y][i + 1] = tid

    return room


def create_floor():
    global field, name, n, k, player, dx, dy, percentage, boss_n, boss_k, subfield, p_n, p_k

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
                    luck = rnd(1, 100)
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

    room_counter = level_cut()

    field[6 * boss_n + 9][6 * boss_k + 9] = 2

    if room_counter < n * k * 0.3 or room_counter > n * k * 0.6:
        create_floor()


def level_cut():
    global field, name, n, k, player, dx, dy, percentage, subfield, boss_n, boss_k, p_n, p_k, cutting_edge, ent_chance, ent_types, entities
    reachable = []
    marked = []
    room_counter = 0
    for i in range(n):
        for j in range(k):
            if rnd(0, 100) < cutting_edge:
                field[6 * i + 3][6 * j] = 0
                field[6 * i][6 * j + 3] = 0

    reachable += [[boss_n, boss_k]]
    reachable += [[boss_n, boss_k + 1]]
    reachable += [[boss_n, boss_k + 2]]
    reachable += [[boss_n + 1, boss_k]]
    reachable += [[boss_n + 1, boss_k + 1]]
    reachable += [[boss_n + 1, boss_k + 2]]
    reachable += [[boss_n + 2, boss_k]]
    reachable += [[boss_n + 2, boss_k + 1]]
    reachable += [[boss_n + 2, boss_k + 1]]
    far_end = [0, 0]

    for room in reachable:

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
    p_k = 6 * far_end[1] + 3

    for i in range(n):
        for j in range(k):
            if ([i, j] not in reachable):
                for m in range(7):
                    for l in range(7):
                        field[6 * i + m][6 * j + l] = 0

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
                field[i][j] = -1

    if [0, 0] not in reachable:
        field[0][0] = -1
    if [0, k - 1] not in reachable:
        field[0][6 * k] = -1
    if [n - 1, 0] not in reachable:
        field[6 * n][0] = -1
    if [n - 1, k - 1] not in reachable:
        field[6 * n][6 * k] = -1

    for room in reachable:
        if loot_chance > rnd(1,100):
            rndid = rnd(1,4)
            entities += [entity(room, rndid)]
            field[6 * room[0] + 3][6 * room[1] + 3] = -1

    return room_counter

entities = []
name = 'scene.cfg'
percentage = 90
n = 8
k = 8
cutting_edge = 80
loot_chance = 60
ent_types = 4

create_floor()
exit()
