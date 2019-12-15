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
x = 1280
y = 720


a = canv.create_polygon(0.8 * x, y, 0.65 * x, 0.8 * y, 0.65 * x, 0.6 * y, x, 0.95 * y, x, y,  fill = 'red', outline = 'black')
b = canv.create_polygon(x, 0.95 * y, 0.65 * x, 0.6 * y, 0.75 * x, 0.6 * y, x, 0.75 * y,  fill = 'red', outline = 'black')
c = canv.create_polygon(0.8 * x, y, 0.75 * x, (1 - 0.2 / 3) * y, 0.72 * x, y,fill = 'black', outline = 'black')
d = canv.create_line(x / 2, y / 2, x * 0.65, y * 0.65, fill = 'green', width = 10)


canv.update()
root.mainloop()