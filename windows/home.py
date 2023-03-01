import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox

import cv2
import joblib
import mysql.connector as connector
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# database
db = connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='thesis'
)
cursor = db.cursor()

create_table_attendance = """
CREATE TABLE IF NOT EXISTS attendance 
(att_id INT AUTO_INCREMENT PRIMARY KEY, 
firstname VARCHAR(40), 
lastname VARCHAR(40), 
student_id VARCHAR(10), 
course_code VARCHAR(40), 
time_in VARCHAR(40), 
time_out VARCHAR(40), 
date_attend VARCHAR(40), 
day_attend VARCHAR(40))
"""

create_table_student = """
CREATE TABLE IF NOT EXISTS students (
id INT PRIMARY KEY AUTO_INCREMENT, 
firstname VARCHAR(40), lastname VARCHAR(40), 
course VARCHAR(50), section VARCHAR(40), 
student_id VARCHAR(10), course_code VARCHAR(40), 
time VARCHAR(40), day VARCHAR(40), 
lab_room VARCHAR(40) 
)
"""

cursor.execute(create_table_student)
cursor.execute(create_table_attendance)

# global variables
global identified_person
current_time = time.strftime("%I:%M %p", time.localtime())
current_date = datetime.now().strftime("%B %d, %Y")
current_day = datetime.now().strftime("%A")

# face detector variable using haar cascade
face_detector = cv2.CascadeClassifier(
    "./resources/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def extract_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    return face_points


def identify_face(face_array):
    model = joblib.load('./static/face_recognition_model.pkl')
    return model.predict(face_array)


def train_model():
    faces = []
    labels = []
    user_list = os.listdir('./static/faces')
    for user in user_list:
        for image_name in os.listdir(f'./static/faces/{user}'):
            img = cv2.imread(f'./static/faces/{user}/{image_name}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)

    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, './static/face_recognition_model.pkl')


def time_in_function():
    student = face_recognition()
    student_id = student.split('_')[0]
    course_code = student.split('_')[0]

    get_student = ("""
    SELECT firstname, lastname FROM students 
    WHERE student_id = '{student_id}' AND 
    course_code = '{course_code}'
    """).format(student_id=student_id, course_code=course_code)
    cursor.execute(get_student)
    data = cursor.fetchone()
    firstname = data[0]
    lastname = data[1]

    exists = fetch_data(student_id, course_code)
    if len(exists) > 0:
        update_attendance = (f"""
        UPDATE attendance SET time_in = '{current_time}' 
        WHERE student_id = '{student_id}' AND 
        course_code = '{course_code}' AND 
        date_attend = '{current_date}'
        """)
        cursor.execute(update_attendance)
        db.commit()

    else:
        attendance_time_in = (f"""
            INSERT INTO attendance 
            (firstname, lastname, 
            student_id, course_code, 
            time_in, date_attend, 
            day_attend) VALUES 
            ('{firstname}', '{lastname}', 
            '{student_id}', '{course_code}', 
            '{current_time}',
            '{current_date}', '{current_day}')
            """)
        cursor.execute(attendance_time_in)
        db.commit()


def time_out_function():
    student = face_recognition()
    student_id = student.split('_')[0]
    course_code = student.split('_')[0]

    get_student = ("""
        SELECT firstname, lastname FROM students 
        WHERE student_id = '{student_id}' AND 
        course_code = '{course_code}'
        """).format(student_id=student_id, course_code=course_code)
    cursor.execute(get_student)
    data = cursor.fetchone()
    firstname = data[0]
    lastname = data[1]

    exists = fetch_data(student_id, course_code)
    if len(exists) > 0:
        update_attendance = (f"""
            UPDATE attendance SET time_out = '{current_time}' 
            WHERE student_id = '{student_id}' AND 
            course_code = '{course_code}' AND 
            date_attend = '{current_date}'
            """)
        cursor.execute(update_attendance)
        db.commit()
    else:
        attendance_time_in = (f"""
                INSERT INTO attendance 
                (firstname, lastname, 
                student_id, course_code, 
                time_out, date_attend, 
                day_attend) VALUES 
                ('{firstname}', '{lastname}', 
                '{student_id}', '{course_code}', 
                '{current_time}',
                '{current_date}', '{current_day}')
                """)
        cursor.execute(attendance_time_in)
        db.commit()


def fetch_data(student_id, course_code):
    get_attendance = (f"""
    SELECT * FROM attendance WHERE 
    student_id = '{student_id}' AND 
    course_code = '{course_code}' AND 
    date_attend = '{current_date}'
    """)
    cursor.execute(get_attendance)
    return cursor.fetchall()


def face_recognition():
    train_model()
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
        elif cv2.waitKey(1) & 0xFF == ord(' '):
            break
    cam.release()
    cv2.destroyAllWindows()
    return identified_person


class HomeWindow:
    def __init__(self, master):
        self.master = master

        self.master.geometry("1000x600")
        self.master.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            window,
            bg="#FFFFFF",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            500.0,
            300.0,
            image=self.image_image_1
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_student,
            relief="flat"
        )
        self.button_1.place(
            x=522.0,
            y=106.0,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=522.0,
            y=181.2080535888672,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(
            x=522.0,
            y=256.4161071777344,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_4.place(
            x=522.0,
            y=331.6241455078125,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        self.button_5.place(
            x=524.0,
            y=407.0,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        self.button_6 = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.time_in,
            relief="flat"
        )
        self.button_6.place(
            x=22.0,
            y=332.0,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_7 = PhotoImage(
            file=relative_to_assets("button_7.png"))
        self.button_7 = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.time_out,
            relief="flat"
        )
        self.button_7.place(
            x=22.0,
            y=407.0,
            width=417.091064453125,
            height=54.95973205566406
        )

        self.button_image_8 = PhotoImage(
            file=relative_to_assets("button_8.png"))
        self.button_8 = Button(
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        self.button_8.place(
            x=879.0,
            y=543.0,
            width=102.0,
            height=36.0
        )

    def add_student(self):
        self.master.destroy()
        subprocess.run(['python', './addstudent.py'])

    def update_student(self):
        self.master.destroy()
        subprocess.run(['python', './updatestudent.py'])

    def delete_student(self):
        self.master.destroy()
        subprocess.run(['python', './deletestudent.py'])

    def list_student(self):
        self.master.destroy()
        subprocess.run(['python', ''])

    def record_student(self):
        self.master.destroy()
        subprocess.run(['python', 'add_student.py'])

    def logout_function(self):
        self.master.destroy()
        subprocess.run(['python', 'add_student.py'])

    def time_in(self):
        time_in_function()
        messagebox.showinfo('Time In', 'Time In Successfully')

    def time_out(self):
        time_out_function()
        messagebox.showinfo('Time Out', 'Time Out Successfully')


window = Tk()
app = HomeWindow(window)
window.resizable(False, False)
window.mainloop()
