import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox

import mysql.connector as con

OUTPUT_PATH = Path(__file__).parent

ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")


def frame_0(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1280x832")
        self.master.title("Face Recognition Student Identifier - Log in")
        self.master.configure(bg="#fff")

        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=832,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        # logo
        self.image_image_1 = PhotoImage(
            file=frame_0("image_1.png"))
        self.image_1 = self.canvas.create_image(
            320.0,
            416.0,
            image=self.image_image_1
        )

        # app name
        self.canvas.create_text(
            38.0,
            416.0,
            anchor="nw",
            text="Face Recognition Student Identifier",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 32 * -1)
        )

        # rectangle for sign in
        self.canvas.create_rectangle(
            640.0,
            0.0,
            1280.0,
            832.0,
            outline="",
            fill="#FFFFFF"
        )

        # face recognition image
        self.image_image_2 = PhotoImage(
            file=frame_0("image_2.png"))
        self.image_2 = self.canvas.create_image(
            960.0,
            230.0,
            image=self.image_image_2
        )

        # username input bg
        self.image_image_3 = PhotoImage(
            file=frame_0("image_3.png"))
        self.image_3 = self.canvas.create_image(
            959.0,
            484.0,
            image=self.image_image_3
        )

        # password input bg
        self.image_image_4 = PhotoImage(
            file=frame_0("image_4.png"))
        self.image_4 = self.canvas.create_image(
            959.0,
            587.0,
            image=self.image_image_4
        )

        # login button bg
        self.button_image_1 = PhotoImage(
            file=frame_0("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.button_1.place(
            x=741.0,
            y=656.0,
            width=437.0,
            height=69.0
        )

        # username label
        self.canvas.create_text(
            774.0,
            423.0,
            anchor="nw",
            text="Username",
            fill="#8E8E8E",
            font=("OpenSansRoman Regular", 14 * -1)
        )
        # register label
        self.canvas.create_text(
            884.0,
            740.0,
            anchor="nw",
            text="Don’t have an account? ",
            fill="#8E8E8E",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        # password label
        self.canvas.create_text(
            774.0,
            526.0,
            anchor="nw",
            text="Password",
            fill="#8E8E8E",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        # username input bg
        self.entry_image_1 = PhotoImage(
            file=frame_0("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            959.5,
            484.5,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 18 * -1)
        )
        self.entry_1.place(
            x=779.0,
            y=463.0,
            width=361.0,
            height=41.0
        )

        # password input bg
        self.entry_image_2 = PhotoImage(
            file=frame_0("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            959.5,
            586.5,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 18 * -1),
            show="•"
        )
        self.entry_2.place(
            x=779.0,
            y=565.0,
            width=361.0,
            height=41.0
        )

        self.button_image_2 = PhotoImage(
            file=frame_0("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.register,
            relief="flat"
        )
        self.button_2.place(
            x=872.0,
            y=774.0,
            width=175.0,
            height=35.0
        )

    def register(self):
        self.master.destroy()
        subprocess.run(["python", "./RegisterScreen.py"])

    def login(self):
        username = self.entry_1.get()
        password = self.entry_2.get()

        if username != "" and password != "":
            db = con.connect(
                host="localhost",
                user="root",
                password="root",
            )

            cur = db.cursor()

            cur.execute("CREATE DATABASE IF NOT EXISTS mydb")
            cur.execute("USE mydb")

            cur.execute(
                f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")

            exists = cur.fetchone()
            if exists is None:
                messagebox.showerror("Error", "Wrong username or password!")
            else:
                messagebox.showinfo("Success", f"Welcome {username}")
                self.master.destroy()
                subprocess.run(["python", "./HomeScreen.py"])
        else:
            messagebox.showerror("Error", "Username and password are required to log in.")


root = Tk()
root.resizable(False, False)
app = LoginScreen(root)
root.mainloop()
