

from pathlib import Path
import subprocess
import cv2
import mysql.connector as con
import time
import datetime
import face_recognition
import numpy as np
import os
import pandas as pd
from tkinter import Frame, Label, Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, Toplevel, ttk
import tkinter as tk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame9")
ASSETS_PATH_INFO = OUTPUT_PATH / Path(r"./assets/frame10")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def frame10(path: str) -> Path:
    return ASSETS_PATH_INFO / Path(path)


def on_close():
    response = messagebox.askyesno(
        "Close", "Are you sure you want to close the Attendance window?")
    if response:
        window.destroy()
        subprocess.run(["python", "./HomeScreen.py"])
    else:
        None


conn = con.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydb"
)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS attendance (att_id INT AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(40), lastname VARCHAR(40), student_id VARCHAR(10), course_code VARCHAR(40), time_in VARCHAR(40), time_out VARCHAR(40), date_attend VARCHAR(40), day_attend VARCHAR(40))")


class Attendance:
    def __init__(self, master):
        self.master = master
        self.master.geometry("611x390")
        self.master.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=390,
            width=611,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            305.0,
            180.0,
            image=self.image_image_1
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            305.5,
            122.5,
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
            x=125.0,
            y=101.0,
            width=361.0,
            height=41.0
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            305.5,
            238.5,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 16 * -1)
        )
        self.entry_2.place(
            x=125.0,
            y=217.0,
            width=361.0,
            height=41.0
        )

        self.canvas.create_text(
            116.0,
            59.0,
            anchor="nw",
            text="Enter the student id number",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            116.0,
            175.0,
            anchor="nw",
            text="Enter the course code",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.TimeInFunction,
            relief="flat"
        )
        self.button_1.place(
            x=89.0,
            y=313.0,
            width=160.0,
            height=47.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.TimeInFunction,
            relief="flat"
        )
        self.button_2.place(
            x=363.0,
            y=313.0,
            width=160.0,
            height=47.0
        )

    def TimeInFunction(self):
        student_id = self.entry_1.get()
        course_code = self.entry_2.get()

        exist = self.StudentExist()
        if exist:
            self.FaceRecognition()
        else:
            messagebox.showerror(
                "Error", f"Student {student_id} is not enrolled in course {course_code}.")

    def StudentExist(self):
        student_id = self.entry_1.get()
        course_code = self.entry_2.get()
        cursor.execute(
            f"SELECT * FROM students WHERE student_id = '{student_id}' AND course_code = '{course_code}'")
        exist = cursor.fetchone()
        if exist is None:
            return False
        else:
            return True

    def FaceRecognition(self):

        flag = False

        student_id = self.entry_1.get()

        video_capture = cv2.VideoCapture(0)

        # Load a sample picture and learn how to recognize it.
        student_image = face_recognition.load_image_file(
            f"./data/{student_id}.jpg")
        student_face_encoding = face_recognition.face_encodings(student_image)[
            0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            student_face_encoding,
        ]
        known_face_names = [
            student_id
        ]

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(
                    rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        not_time_in = self.checkAttendance()
                        if not_time_in:
                            self.time_in()
                            video_capture.release()
                            cv2.destroyAllWindows()
                        else:
                            self.time_out()
                            video_capture.release()
                            cv2.destroyAllWindows()
                        flag = True
                        break
                    face_names.append(name)
            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                student_face_encoding = []
                break
            elif cv2.waitKey(1) == ord('c') or cv2.waitKey(1) == ord(' '):
                student_face_encoding = []
                break
            elif flag:
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def time_in(self):
        student_id = self.entry_1.get()
        course_code = self.entry_2.get()

        time_in = time.strftime("%I:%M %p")
        time_out = ""

        curr_date = datetime.datetime.now().strftime("%B %d, %Y")
        curr_day = datetime.datetime.now().strftime("%A")

        cursor.execute(
            f"SELECT * FROM students WHERE student_id = '{student_id}' AND course_code = '{course_code}'")
        info = cursor.fetchone()
        fname = info[1]
        lname = info[2]
        std_id = info[3]
        course_code = info[5]

        not_timed_in = self.checkAttendance()

        if not_timed_in:
            cursor.execute(
                f"INSERT INTO attendance (firstname, lastname, student_id, course_code, time_in, time_out, date_attend, day_attend) VALUES ('{fname}', '{lname}', '{std_id}', '{course_code}', '{time_in}', '{time_out}', '{curr_date}', '{curr_day}')")
            conn.commit()
        else:
            messagebox.showerror(
                "Error", f"Student {student_id} is already present in course {course_code}.")

        newWindow = Toplevel(self.master)
        newWindow.title("Student Info")
        newWindow.resizable(False, False)
        self.app = StudentInfo(
            newWindow, student_id, course_code)

    def checkAttendance(self):
        std_id = self.entry_1.get()
        c_code = self.entry_2.get()

        cursor.execute(
            f"SELECT * FROM attendance WHERE student_id = '{std_id}' AND course_code = '{c_code}'")
        exist = cursor.fetchone()

        if exist is None:
            return True
        else:
            return False

    def time_out(self):
        student_id = self.entry_1.get()
        course_code = self.entry_2.get()

        time_out = time.strftime("%I:%M %p", time.localtime())

        not_timed_in = self.checkAttendance()

        if not_timed_in:
            messagebox.showerror(
                "Error", f"Student {student_id} is not timed in course {course_code}. Please time in first.")

        else:
            cursor.execute(
                f"UPDATE attendance SET time_out = '{time_out}' WHERE student_id = '{student_id}' AND course_code = '{course_code}'")
            conn.commit()

        newWindow = Toplevel(self.master)
        newWindow.title("Student Info")
        newWindow.resizable(False, False)
        self.app = StudentInfo(
            master=newWindow, std_id=student_id, c_code=course_code)


class StudentInfo:
    def __init__(self, master, std_id, c_code):
        self.master = master
        self.fname = tk.StringVar()
        self.lname = tk.StringVar()

        self.std_id = std_id
        self.course = tk.StringVar()
        self.sec = tk.StringVar()
        self.code = c_code
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

        self.info()
        self.scedule()

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
            text=self.course,
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
            text=f"{self.fname}, {self.lname}",
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
            text=self.code,
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 24 * -1)
        )

        self.canvas.create_text(
            281.0,
            290.0,
            anchor="nw",
            text=self.sec,
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
            "OpenSansRoman Bold", 21 * -1), background="#438FF4", foreground="#FFFFFF")

        self.time.place(x=145.0, y=567.0)
        self.canvas.create_text(
            1104.0,
            309.0,
            anchor="nw",
            text=self.time,
            fill="#FFFFFF",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.clock()

        self.frame = Frame(self.master, bg="#438FF4", relief="flat")

        self.style = ttk.Style()
        self.style.configure(
            "Custom.Treeview",
            rowheight=50,
            font=("OpenSansRoman Bold", 18 * -1),
        )
        self.frame.place(x=688, y=248, width=560, height=500)
        self.table = ttk.Treeview(
            self.frame, columns=("Course Code", "Time", "Day"), show="headings", style="Custom.Treeview", selectmode="none")

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

    def clock(self):
        self.curr_time = time.strftime("%I:%M:%S %p", time.localtime())
        self.time.config(text=self.curr_time)
        self.time.after(100, self.clock)

    def scedule(self):
        cursor.execute(
            f"SELECT course_code, time, day  FROM students WHERE student_id = '{self.std_id}' ORDER BY course_code")
        fetch_data = cursor.fetchall()
        for data in fetch_data:
            datalist = list(data)
            self.table.insert("", "end", values=datalist, tags=("disabled"))
            self.table.tag_bind(
                "disabled", "<<TreeviewSelect>>", lambda event: "break")

    def info(self):
        ids = self.std_id
        cd = self.code
        cursor.execute(
            f"SELECT firstname, lastname, course, section FROM students WHERE student_id = '{ids}' AND course_code = '{cd}'")
        data = cursor.fetchone()
        print(data)


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
app = Attendance(window)
window.resizable(False, False)
window.mainloop()
