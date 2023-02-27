
from pathlib import Path
import subprocess

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
    Path(r"./assets/frame8")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def on_close():
    response = messagebox.askokcancel("Quit", "Do you want to quit?")
    if response:
        window.destroy()
        subprocess.run(["python", "./HomeScreen.py"])
    else:
        None


class DeleteStudentsWindow:

    def __init__(self, master):
        self.master = master
        self.master.geometry("659x864")
        self.master.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=864,
            width=659,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            250.0,
            40.0,
            anchor="nw",
            text="Delete Students",
            fill="#9F9F9F",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(
            x=235.0,
            y=776.0,
            width=190.0,
            height=58.0
        )

        self.canvas.create_text(
            102.0,
            97.0,
            anchor="nw",
            text="Search a student by name",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            329.5,
            152.0,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 15 * -1)
        )
        self.entry_1.place(
            x=128.0,
            y=132.0,
            width=403.0,
            height=38.0
        )

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            330.0,
            435.0,
            image=self.image_image_1
        )


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
app = DeleteStudentsWindow(window)
window.resizable(False, False)
window.mainloop()
