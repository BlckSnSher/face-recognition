import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, ttk, Frame, BOTH, Scrollbar, END, messagebox
from tkinter.ttk import Style

import mysql.connector as conn

print("connecting to database .....")
db = conn.connect(
    host='localhost',
    user='root',
    password='root',
    database='thesis'
)
cursor = db.cursor()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame6")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def on_close():
    response = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if response:
        window.destroy()
        subprocess.run(["python", "./home.py"])
    else:
        return


print("starting .....")


class DeleteStudent:
    def __init__(self, master):
        self.master = master
        self.master.geometry("462x602")
        self.master.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=602,
            width=462,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
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
            x=163.0,
            y=554.0,
            width=135.71435546875,
            height=35.6824951171875
        )

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            232.0,
            301.0,
            image=self.image_image_1
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            231.5,
            99.0,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("ArialMT", 14 * -1)
        )
        self.entry_1.place(
            x=87.0,
            y=82.0,
            width=289.0,
            height=32.0
        )

        self.canvas.create_text(
            155.0,
            23.0,
            anchor="nw",
            text="Delete Students",
            fill="#9F9F9F",
            font=("Arial BoldMT", 20 * -1)
        )

        self.canvas.create_text(
            69.0,
            59.0,
            anchor="nw",
            text="Search a student by name",
            fill="#9F9F9F",
            font=("ArialMT", 14 * -1)
        )

        self.frame = Frame(self.canvas, bg="#fff")
        self.frame.place(x=32, y=145, width=400, height=360)

        self.heading = ttk.Style()
        self.heading.configure(
            "Treeview.Heading",
            font=("OpenSansRoman Bold", 18 * -1),
        )
        self.tree_style = Style()
        self.tree_style.configure(
            "Custom.Treeview",
            font=("OpenSansRoman Bold", 14 * -1),
            rowheight=50,
        )

        self.table = ttk.Treeview(
            self.frame,
            columns=(
                "Student ID",
                "First Name",
                "Last Name",
                "Course",
                "Section",
                "Course Code",
                "Time", "Day",
                "Lab Room"
            ), show="headings",
            style="Custom.Treeview",
            cursor="hand2"
        )

        self.table.pack(fill=BOTH, expand=True)

        self.table.heading("Student ID", text="Student ID")
        self.table.heading("First Name", text="First Name")
        self.table.heading("Last Name", text="Last Name")
        self.table.heading("Course", text="Course")
        self.table.heading("Section", text="Section")
        self.table.heading("Course Code", text="Course Code")
        self.table.heading("Time", text="Time")
        self.table.heading("Day", text="Day")
        self.table.heading("Lab Room", text="Lab Room")

        self.scrollX = Scrollbar(self.table, orient="horizontal", command=self.table.xview)
        self.scrollX.pack(side="bottom", fill="x")

        self.scrollY = Scrollbar(self.table, orient="vertical", command=self.table.yview)
        self.scrollY.pack(side="right", fill="y")
        self.table.configure(xscrollcommand=self.scrollX.set, yscrollcommand=self.scrollY.set)

        # bind a command in table
        self.table.bind("<ButtonRelease-1>", self.selected_item)

        self.get_students()

    def get_students(self):
        print("fetching the info .....")
        get_students = """
            select student_id, firstname, lastname, course, section,
             course_code, time, day, lab_room from students
            """
        cursor.execute(get_students)
        rows = cursor.fetchall()
        for row in rows:
            data_list = list(row)
            self.table.insert("", END, values=data_list)

    def selected_item(self, event):
        get_item = self.table.focus()
        print(self.table.item(get_item))


window = Tk()
app = DeleteStudent(window)
window.protocol("WM_DELETE_WINDOW", on_close)
window.resizable(False, False)
window.mainloop()
