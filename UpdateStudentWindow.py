import subprocess
from pathlib import Path
from tkinter import END, Frame, Tk, Canvas, Entry, Button, PhotoImage, messagebox, ttk

import mysql.connector

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
              Path(r"./assets/frame6")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def on_close():
    response = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if response:
        window.destroy()
        subprocess.run(["python", "./HomeScreen.py"])
    else:
        return


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydb"
)

cursor = conn.cursor()

query = """
SELECT student_id, 
firstname, 
lastname, 
course, 
section, 
course_code, 
time,
day
FROM students ORDER BY student_id
"""


class UpdateStudentWindow:
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
            246.0,
            40.0,
            anchor="nw",
            text="Update Students",
            fill="#9F9F9F",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            # command=self.search,
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
            font=("OpenSansRoman Regular", 16 * -1)
        )
        self.entry_1.place(
            x=128.0,
            y=132.0,
            width=403.0,
            height=38.0
        )
        self.entry_1.bind("<KeyPressed>", self.update_table)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            330.0,
            435.0,
            image=self.image_image_1
        )

        self.frame = Frame(self.canvas, bg="#fff")
        self.frame.place(x=55, y=220, width=550, height=510)

        self.style = ttk.Style()
        self.style.configure(
            "Custom.Treeview",
            font=("OpenSansRoman Bold", 14 * -1),
            rowheight=50,
        )

        self.heading = ttk.Style()
        self.heading.configure(
            "Treeview.Heading",
            font=("OpenSansRoman Bold", 18 * -1),
        )
        self.table = ttk.Treeview(
            self.frame,
            columns=(
                "First Name",
                "Last Name",
                "Student ID",
                "Course",
                "Section",
                "Course Code",
                "Time",
                "Day"
            ),
            show="headings",
            style="Custom.Treeview",
            cursor='hand2'
        )

        self.table.pack(fill="both", expand=True)

        self.table.heading("First Name", text="First Name")
        self.table.heading("Last Name", text="Last Name")
        self.table.heading("Student ID", text="Student ID")
        self.table.heading("Course", text="Course")
        self.table.heading("Section", text="Section")
        self.table.heading("Course Code", text="Course Code")
        self.table.heading("Time", text="Time")
        self.table.heading("Day", text="Day")

        self.update_table(self.entry_1.get())

    def get_students(self):
        cursor.execute(query)
        fetch_data = cursor.fetchall()
        for data in fetch_data:
            data_lists = list(data)
            self.table.insert("", END, values=data_lists)

    def update_table(self, search_value):

        for row in self.table.get_children():
            self.table.delete(row)

        if search_value is not "":
            cursor.execute(
                "SELECT student_id, "
                "firstname, "
                "lastname, "
                "course, "
                "section, "
                "course_code, "
                "time, "
                "day FROM students WHERE firstname LIKE ?",
                f'%{search_value}%'
            )
        else:
            cursor.execute(query)

        rows = cursor.fetchall()

        for row in rows:
            data_lists = list(row)
            self.table.insert('', END, values=data_lists)
        self.entry_1.get()
        self.entry_1.after(100, self.update_table)


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
app = UpdateStudentWindow(window)
window.resizable(False, False)
window.mainloop()
