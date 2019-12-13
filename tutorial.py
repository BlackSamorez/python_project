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
lbl3 = Label(window, text="'a','s','w','d' - передвижение\n"
                          "'q','e' - поворот\n"
                          "enter - стрелять\n"
                          "'m' - показать карту",
                          font=("Arial Bold", 13), bg="#00acb4", fg="#10455b", justify=LEFT)
lbl3.grid(column=1, row=100)
lbl4 = Label(window, text="ЧИТЫ:\n '+' - добавить hp\n '-' - убавить hp", font=("Arial Bold", 15), bg="red", justify=LEFT)
lbl4.grid(column=1, row=150)
btn = Button(window, text="Всё понятно", command=clicked, bg="#10455b", fg="#00acb4", font=("Arial Bold", 15))
btn.grid(column=1, row=200)
window.mainloop()
