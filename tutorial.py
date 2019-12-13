from tkinter import *


def clicked():
    exit()


window = Tk()
window.title("TUTORIAL")
window.geometry('530x350')

lbl1 = Label(window, text="Инструкция", font=("Arial Bold", 25), bg="#10455b", fg="#00acb4")
lbl1.grid(column=1, row=0)
lbl2 = Label(window, text="1. Перед началом игры не забудьте\n переключиться на английскую раскладку и нажать TAB\n"
             "2. Комбинации клавиш:", font=("Arial Bold", 15), fg="#10455b")
lbl2.grid(column=1, row=50)
lbl3 = Label(window, text="'A','S','W','D' - передвижение\n"
                          "'E','E' - поворот\n"
                          "enter - стрелять\n"
                          "H - использовать аптечку\n"
                          "'M' - показать карту",
                          font=("Arial Bold", 13), bg="#00acb4", fg="#10455b", justify=LEFT)
lbl3.grid(column=1, row=100)
btn = Button(window, text="Всё понятно", command=clicked, bg="#10455b", fg="#00acb4", font=("Arial Bold", 15))
btn.grid(column=1, row=200)
window.mainloop()
