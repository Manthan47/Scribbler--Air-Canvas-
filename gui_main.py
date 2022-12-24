from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter.filedialog import askdirectory
import ppt
import whiteboard2
import quiz
import os

def ppt_main():
    ppt.ppt_main()


def whiteBoard():
    whiteboard2.whiteboard2_main()

def quiz_main():
    quiz.quiz_main()

scriptDir = os.getcwd()

OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"D:\SEM VII\CP III\Final project\assets\frame0")
print(OUTPUT_PATH)
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")



def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Scribbler")
window.geometry("900x480")
window.configure(bg = "#03045E")


canvas = Canvas(
    window,
    bg = "#03045E",
    height = 480,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets(r"image_1.png"))
image_1 = canvas.create_image(
    450.9999885559082,
    240.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets(r"image_2.png"))
image_2 = canvas.create_image(
    231.0,
    240.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file=relative_to_assets(r"button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=whiteBoard,
    relief="flat"
)
button_1.place(
    x=586.0,
    y=140.0,
    width=221.09521484375,
    height=44.90478515625
)

button_image_2 = PhotoImage(
    file=relative_to_assets(r"button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=ppt_main,
    relief="flat"
)
button_2.place(
    x=586.0,
    y=215.0,
    width=221.0,
    height=44.90478515625
)

button_image_3 = PhotoImage(
    file=relative_to_assets(r"button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=quiz_main,
    relief="flat"
)
button_3.place(
    x=586.0,
    y=290.0,
    width=221.0,
    height=44.90478515625
)
window.resizable(False, False)
window.mainloop()
