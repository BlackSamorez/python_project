import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.geometry('880x720')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

pilImage = Image.open("images/text.png")
bg = ImageTk.PhotoImage(pilImage)
im_got = ImageTk.PhotoImage(file="images/got_it.png")
got_button = tk.Button(
    root, image=im_got,
    command=exit
)

canv.create_image(440, 360, image=bg)
got_button.place(x=600, y=320)

root.mainloop()
