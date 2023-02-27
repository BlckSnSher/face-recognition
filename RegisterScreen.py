import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox

import mysql.connector as con

from logic import checkInputRegister

OUTPUT_PATH = Path(__file__).parent

ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame5")


def frame5(path: str) -> Path:
    return ASSETS_PATH / Path(path)


root = Tk()


class RegisterScreen:
    def __init__(self, master):
        self.master = master
        self.master.resizable(False, False)
        self.master.geometry("1280x832")
        self.master.title("Face Recognition Student Identifier")
        self.master.configure(bg="#fff")

        self.canvas = Canvas(
            master=self.master,
            bg="#FFFFFF",
            height=832,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            640.0,
            0.0,
            1280.0,
            832.0,
            fill="#FFFFFF",
            outline="")

        self.image_image_1 = PhotoImage(
            file=frame5("image_1.png"))
        self.image_1 = self.canvas.create_image(
            320.0,
            416.0,
            image=self.image_image_1
        )

        self.canvas.create_text(
            38.0,
            416.0,
            anchor="nw",
            text="Face Recognition Student Identifier",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 32 * -1)
        )

        self.image_image_2 = PhotoImage(
            file=frame5("image_2.png"))
        self.image_2 = self.canvas.create_image(
            959.0,
            296.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=frame5("image_3.png"))
        self.image_3 = self.canvas.create_image(
            959.0,
            405.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=frame5("image_4.png"))
        self.image_4 = self.canvas.create_image(
            959.0,
            514.0,
            image=self.image_image_4
        )

        self.entry_image_1 = PhotoImage(
            file=frame5("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            959.5,
            296.5,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            master=self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 18 * -1)
        )
        self.entry_1.place(
            x=779.0,
            y=275.0,
            width=361.0,
            height=41.0
        )

        self.entry_image_2 = PhotoImage(
            file=frame5("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            959.5,
            405.5,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            master=self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 18 * -1),
            show="•"
        )
        self.entry_2.place(
            x=779.0,
            y=384.0,
            width=361.0,
            height=41.0
        )

        self.entry_image_3 = PhotoImage(
            file=frame5("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(
            959.5,
            514.5,
            image=self.entry_image_3
        )
        self.entry_3 = Entry(
            master=self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 18 * -1),
            show="•"
        )
        self.entry_3.place(
            x=779.0,
            y=493.0,
            width=361.0,
            height=41.0
        )

        self.canvas.create_text(
            903.0,
            174.0,
            anchor="nw",
            text="Register",
            fill="#8E8E8E",
            font=("OpenSansRoman Regular", 30 * -1)
        )

        self.canvas.create_text(
            779.0,
            236.0,
            anchor="nw",
            text="Username",
            fill="#8E8E8E",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            779.0,
            345.0,
            anchor="nw",
            text="Password",
            fill="#8E8E8E",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            779.0,
            454.0,
            anchor="nw",
            text="Confirm Password",
            fill="#8E8E8E",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=frame5("button_1.png"))
        self.button_1 = Button(
            master=self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.register,
            relief="flat"
        )
        self.button_1.place(
            x=741.0,
            y=589.0,
            width=437.0,
            height=69.0
        )

        self.canvas.create_text(
            877.0,
            698.0,
            anchor="nw",
            text="Already have an account?",
            fill="#8E8E8E",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=frame5("button_2.png"))
        self.button_2 = Button(
            master=self.master,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.button_2.place(
            x=872.0,
            y=737.0,
            width=175.0,
            height=35.0
        )

    def register(self):
        username = self.entry_1.get()
        password = self.entry_2.get()
        confirm_password = self.entry_3.get()
        c = checkInputRegister(username, password, confirm_password)
        if c:
            conn = con.connect(
                host="localhost",
                user="root",
                password="root",
                database="mydb"
            )
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users "
                "(id INT AUTO_INCREMENT PRIMARY KEY, "
                "username VARCHAR(40), "
                "password VARCHAR(40))"
            )
            cursor.execute(
                f"SELECT * FROM users WHERE username='{username}'"
            )
            result = cursor.fetchone()
            if result is None:
                if password != confirm_password:
                    messagebox.showerror(
                        "Error", "Passwords do not match.")
                else:
                    cursor.execute(
                        f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
                    conn.commit()
                    messagebox.showinfo(
                        "Success", "Registration Successful")
                    self.master.destroy()
                    subprocess.run(["python", "./LoginScreen.py"])
            else:
                messagebox.showerror("Error", "Username already exists!")
        else:
            messagebox.showerror("Error", "Please fill all the fields.")

    def login(self):
        self.master.destroy()
        subprocess.run(["python", "./LoginScreen.py"])


app = RegisterScreen(root)
root.mainloop()
