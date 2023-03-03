from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame9")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("462x194")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=194,
    width=462,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=141.0,
    y=135.0,
    width=179.0,
    height=45.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    231.0,
    91.0,
    image=image_image_1
)

canvas.create_text(
    73.0,
    54.0,
    anchor="nw",
    text="Course Code",
    fill="#9F9F9F",
    font=("ArialMT", 14 * -1)
)

canvas.create_text(
    139.0,
    17.0,
    anchor="nw",
    text="Attendance Record",
    fill="#9F9F9F",
    font=("Arial BoldMT", 20 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    231.5,
    91.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=91.0,
    y=76.0,
    width=281.0,
    height=28.0
)
window.resizable(False, False)
window.mainloop()
