import datetime
import subprocess
import time
from pathlib import Path
from tkinter import END, Frame, Label, StringVar, Tk, Canvas, Button, PhotoImage, Toplevel, messagebox, ttk

import cv2
import joblib
import mysql.connector as connector

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
              Path(r"./assets/frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH9 = OUTPUT_PATH / Path(r"./assets/frame9")
ASSETS_PATH_INFO = OUTPUT_PATH / Path(r"./assets/frame10")


def relative_to_assets9(path: str) -> Path:
    return ASSETS_PATH9 / Path(path)


def frame10(path: str) -> Path:
    return ASSETS_PATH_INFO / Path(path)


def on_close():
    response = messagebox.askokcancel(
        "Close", "Are you sure you want to close the window?")
    if response:
        window.destroy()
    else:
        return


global identified_person

face_detector = cv2.CascadeClassifier(
    "./resources/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

db = connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mydb'
)

cursor = db.cursor()


def list_of_students_function():
    messagebox.showinfo("Success", "List of Students")


def attendance_record_function():
    messagebox.showinfo("Success", "Attendance Record")


def extract_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    return face_points


def identify_face(face_array):
    model = joblib.load('./static/face_recognition_model.pkl')
    return model.predict(face_array)


class HomeScreen:

    def __init__(self, master):
        self.master = master
        self.master.geometry("1280x832")
        self.master.title("Face Recognition Student Identifier - Home Screen")
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
        self.canvas.create_rectangle(
            640.0,
            0.0,
            1280.0,
            832.0,
            fill="#FFFFFF",
            outline="")

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
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

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_student_function,
            relief="flat",
            cursor="hand2"
        )
        self.button_1.place(
            x=740.0,
            y=62.0,
            width=437.0,
            height=76.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.update_student_function,
            relief="flat",
            cursor="hand2"
        )
        self.button_2.place(
            x=740.0,
            y=166.0,
            width=437.0,
            height=76.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_student_function,
            relief="flat",
            cursor="hand2"
        )
        self.button_3.place(
            x=740.0,
            y=270.0,
            width=437.0,
            height=76.0
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=list_of_students_function,
            relief="flat",
            cursor="hand2"
        )
        self.button_4.place(
            x=740.0,
            y=374.0,
            width=437.0,
            height=76.0
        )

        self.button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.attendance_function,
            relief="flat",
            cursor="hand2"
        )
        self.button_5.place(
            x=740.0,
            y=478.0,
            width=437.0,
            height=76.0
        )

        self.button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        self.button_6 = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=attendance_record_function,
            relief="flat",
            cursor="hand2"
        )
        self.button_6.place(
            x=742.0,
            y=582.0,
            width=437.0,
            height=76.0
        )

        self.button_image_7 = PhotoImage(
            file=relative_to_assets("button_7.png"))
        self.button_7 = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.logout_function,
            relief="flat",
            cursor="hand2"
        )
        self.button_7.place(
            x=1163.0,
            y=781.0,
            width=102.0,
            height=36.0
        )

    def add_student_function(self):
        self.master.destroy()
        subprocess.run(["python", "./addstudent.py"])

    def update_student_function(self):
        self.master.destroy()
        subprocess.run(["python", "./UpdateStudentWindow.py"])

    def delete_student_function(self):
        self.master.destroy()
        subprocess.run(["python", "./DeleteStudentWindow.py"])

    def attendance_function(self):
        self.face_recognition()

    def logout_function(self):
        response = messagebox.askyesno(
            "Log Out", "Are you sure you want to log out?")
        if response:
            self.master.destroy()
            subprocess.run(["python", "./LoginScreen.py"])
        else:
            return

    # face recognition

    def face_recognition(self):
        global identified_person
        cam = cv2.VideoCapture(0)
        ret = True
        while ret:
            ret, frame = cam.read()

            if len(extract_face(frame)) > 0:
                (x, y, w, h) = extract_face(frame)[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
                face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
                identified_person = identify_face(face.reshape(1, -1))[0]
                cv2.putText(frame, identified_person,
                            (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()
        self.openStudentInfo(identified_person)
        print(identified_person)

    def openStudentInfo(self, sid_cd):
        
        new_window = Toplevel(self.master)
        new_window.title("Face Recognition Student Identifier")
        StudentInfo(new_window, sid_cd)


def update_info():
    cursor.execute(f"SELECT ")


class StudentInfo:
    def __init__(self, master, sid_cd):
        self.master = master
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.crs = StringVar()
        self.std_id = sid_cd.split("_")[0]
        self.day = StringVar()

        self.code = sid_cd.split("_")[1]
        self.sec = StringVar()

        # time in and time out
        self.ti = StringVar()
        self.to = StringVar()

        # date and day
        self.curr_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.curr_day = datetime.datetime.now().strftime("%A")

        self.master.geometry("1280x832")
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
        self.image_image_1 = PhotoImage(
            file=frame10("image_1.png"))
        self.image_1 = self.canvas.create_image(
            640.0,
            391.0,
            image=self.image_image_1
        )

        self.canvas.create_text(
            281.0,
            263.0,
            anchor="nw",
            text=f"{self.crs}",
            fill="#000000",
            font=("OpenSansRoman Regular", 20 * -1)
        )

        self.canvas.create_text(
            404.0,
            34.0,
            anchor="nw",
            text="Student Information",
            fill="#FFFFFF",
            font=("Inter Bold", 48 * -1)
        )

        self.canvas.create_text(
            281.0,
            224.0,
            anchor="nw",
            text=f"{self.first_name}, {self.last_name}",
            fill="#000000",
            font=("Inter Bold", 32 * -1)
        )

        self.canvas.create_text(
            55.0,
            653.0,
            anchor="nw",
            text="Time in:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            55.0,
            709.0,
            anchor="nw",
            text="Time out:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            55.0,
            498.0,
            anchor="nw",
            text="Date:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            148.0,
            498.0,
            anchor="nw",
            text=self.curr_date,
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            54.0,
            436.0,
            anchor="nw",
            text="Course Code:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            238.0,
            436.0,
            anchor="nw",
            text=f"{self.code}",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            281.0,
            290.0,
            anchor="nw",
            text=f"{self.sec}",
            fill="#000000",
            font=("OpenSansRoman Regular", 20 * -1)
        )

        self.canvas.create_text(
            281.0,
            317.0,
            anchor="nw",
            text=self.std_id,
            fill="#000000",
            font=("OpenSansRoman Regular", 20 * -1)
        )

        self.canvas.create_text(
            906.0,
            184.0,
            anchor="nw",
            text="Schedule",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 30 * -1)
        )

        self.canvas.create_text(
            54.0,
            567.0,
            anchor="nw",
            text="Time:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            54.0,
            531.0,
            anchor="nw",
            text="Day:",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            147.0,
            531.0,
            anchor="nw",
            text=self.curr_day,
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            147.0,
            567.0,
            anchor="nw",
            text="09:30:23",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            184.0,
            653.0,
            anchor="nw",
            text="09:30:23",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            184.0,
            709.0,
            anchor="nw",
            text="09:30:23",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            717.0,
            309.0,
            anchor="nw",
            text="CS 301",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.canvas.create_text(
            910.0,
            309.0,
            anchor="nw",
            text="9AM - 10AM",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.time = Label(self.master, font=(
            "OpenSansRoman Bold", 22 * -1), background="#438FF4", foreground="#FFFFFF")

        self.time.place(x=145.0, y=567.0)
        self.canvas.create_text(
            1104.0,
            309.0,
            anchor="nw",
            text=f"{self.time}",
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 20 * -1)
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
            self.frame, columns=("Course Code", "Time", "Day"), show="headings", style="Custom.Treeview",
            selectmode="none")

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
        self.fetch_data()

    def clock(self):
        curr_time = time.strftime("%I:%M:%S %p", time.localtime())
        self.time.config(text=curr_time)
        self.time.after(100, self.clock)

    def schedule(self):
        cursor.execute(
            f"SELECT course_code, time, day  FROM students WHERE student_id = '{self.std_id}' ORDER BY course_code")
        fetch_data = cursor.fetchall()
        for data in fetch_data:
            data_lists = list(data)
            self.table.insert("", END, values=data_lists, tags="disabled")
            self.table.tag_bind(
                "disabled", "<<TreeviewSelect>>", lambda event: "break")

    # get the data in database where student id and course code is related
    def fetch_data(self):
        sid = self.std_id
        code = self.code
        print(sid, code)
        select = f"""
        SELECT firstname,
        lastname,
        course,
        section
        FROM students WHERE
        student_id = {sid} AND course_code = '{code}'
        """

        cursor.execute(select)
        data = cursor.fetchone()
        if data is None:
            messagebox.showerror("Error", "Data not found")
        else:
            for x in data:
                print(x)
                self.first_name.set(x[0])
                self.last_name.set(x[1])
                self.crs.set(x[2])
                self.sec.set(x[3])


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
app = HomeScreen(window)
window.resizable(False, False)
window.mainloop()
