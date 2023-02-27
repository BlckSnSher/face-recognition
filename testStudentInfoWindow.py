import datetime
import subprocess
import time
from pathlib import Path
from tkinter import (
    Frame,
    Label,
    Tk,
    Canvas,
    PhotoImage,
    messagebox,
    ttk,
)

import mysql.connector as con

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame9")
ASSETS_PATH_INFO = OUTPUT_PATH / Path(r"./assets/frame10")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def frame10(path: str) -> Path:
    return ASSETS_PATH_INFO / Path(path)


def on_close():
    response = messagebox.askyesno(
        "Close", "Are you sure you want to close the Attendance window?"
    )
    if response:
        window.destroy()
        subprocess.run(["python", "./HomeScreen.py"])
    else:
        return


conn = con.connect(
    host="localhost", user="root", password="root", database="mydb"
)
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS attendance "
    "(att_id INT AUTO_INCREMENT PRIMARY KEY, "
    "firstname VARCHAR(40), "
    "lastname VARCHAR(40), "
    "student_id VARCHAR(10), "
    "course_code VARCHAR(40), "
    "time_in VARCHAR(40), "
    "time_out VARCHAR(40), "
    "date_attend VARCHAR(40), "
    "day_attend VARCHAR(40))"
)


class StudentInfo:
    def __init__(self, master):
        self.master = master
        self.first_name = "John Lee"
        self.last_name = "Smith"

        self.curr_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.curr_day = datetime.datetime.now().strftime("%A")
        self.code = "CS202"
        self.sec = "CS3"
        self.std_id = "2020-20209"
        self.master.geometry("1280x832")

        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=832,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(file=frame10("image_1.png"))
        self.image_1 = self.canvas.create_image(
            640.0, 391.0, image=self.image_image_1
        )

        self.canvas.create_text(
            281.0,
            263.0,
            anchor="nw",
            text="BSCS",
            fill="#000000",
            font=("OpenSansRoman Regular", 20 * -1),
        )

        self.canvas.create_text(
            404.0,
            34.0,
            anchor="nw",
            text="Student Information",
            fill="#FFFFFF",
            font=("Inter Bold", 48 * -1),
        )

        self.canvas.create_text(
            281.0,
            224.0,
            anchor="nw",
            text=f"{self.first_name}, {self.last_name}",
            fill="#000000",
            font=("Inter Bold", 32 * -1),
        )

        self.canvas.create_text(
            55.0,
            653.0,
            anchor="nw",
            text="Time in:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            55.0,
            709.0,
            anchor="nw",
            text="Time out:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            55.0,
            498.0,
            anchor="nw",
            text="Date:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            148.0,
            498.0,
            anchor="nw",
            text=self.curr_date,
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            54.0,
            436.0,
            anchor="nw",
            text="Course Code:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            238.0,
            436.0,
            anchor="nw",
            text=self.code,
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            281.0,
            290.0,
            anchor="nw",
            text=self.sec,
            fill="#000000",
            font=("OpenSansRoman Regular", 20 * -1),
        )

        self.canvas.create_text(
            281.0,
            317.0,
            anchor="nw",
            text=self.std_id,
            fill="#000000",
            font=("OpenSansRoman Regular", 20 * -1),
        )

        self.canvas.create_text(
            906.0,
            184.0,
            anchor="nw",
            text="Schedule",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 30 * -1),
        )

        self.canvas.create_text(
            54.0,
            567.0,
            anchor="nw",
            text="Time:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            54.0,
            531.0,
            anchor="nw",
            text="Day:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            147.0,
            531.0,
            anchor="nw",
            text=self.curr_day,
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            147.0,
            567.0,
            anchor="nw",
            text="09:30:23",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            184.0,
            653.0,
            anchor="nw",
            text="09:30:23",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            184.0,
            709.0,
            anchor="nw",
            text="09:30:23",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1),
        )

        self.canvas.create_text(
            717.0,
            309.0,
            anchor="nw",
            text="CS 301",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 20 * -1),
        )

        self.canvas.create_text(
            910.0,
            309.0,
            anchor="nw",
            text="9AM - 10AM",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 20 * -1),
        )

        self.time = Label(
            self.master,
            font=("OpenSansRoman Bold", 21 * -1),
            background="#438FF4",
            foreground="#FFFFFF",
        )

        self.time.place(x=145.0, y=567.0)
        self.canvas.create_text(
            1104.0,
            309.0,
            anchor="nw",
            text=f"{self.time}",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 20 * -1),
        )

        self.frame = Frame(self.master, bg="#438FF4", relief="flat")

        self.style = ttk.Style()
        self.style.configure(
            "Custom.Treeview",
            rowheight=50,
            font=("OpenSansRoman Bold", 18 * -1),
        )
        self.frame.place(x=688, y=248, width=560, height=500)
        self.table = ttk.Treeview(
            self.frame,
            columns=("Course Code", "Time", "Day"),
            show="headings",
            style="Custom.Treeview",
            selectmode="none",
        )

        self.heading_style = ttk.Style()
        self.heading_style.configure(
            "Treeview.Heading",
            font=("OpenSansRoman Bold", 18 * -1),
            height=50,
            background="#438FF4",
        )
        self.table.pack(fill="both", expand=True)
        self.table.heading("Course Code", text="Course Code")
        self.table.heading("Time", text="Time")
        self.table.heading("Day", text="Day")

        self.clock()
        self.schedule()

    def clock(self):
        curr_time = time.strftime("%I:%M:%S %p", time.localtime())
        self.time.config(text=curr_time)
        self.time.after(100, self.clock)

    def schedule(self):
        cursor.execute(
            f"SELECT course_code, time, day  FROM students WHERE student_id = '{self.std_id}' ORDER BY course_code"
        )
        fetch_data = cursor.fetchall()
        for data in fetch_data:
            data_lists = list(data)
            self.table.insert("", "end", values=data_lists, tags="disabled")
            self.table.tag_bind(
                "disabled", "<<TreeviewSelect>>", lambda event: "break"
            )


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
app = StudentInfo(window)
window.resizable(False, False)
window.mainloop()
