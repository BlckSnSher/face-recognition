import csv
import os
import subprocess
from pathlib import Path
from tkinter import END, Tk, Canvas, Entry, Button, PhotoImage, messagebox, ttk

import cv2
import joblib
import mysql.connector
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydb"
)

cur = db.cursor()

query_create_database = """
CREATE TABLE IF NOT EXISTS students (
id INT PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(30),
lastname VARCHAR(30),
student_id VARCHAR(30),
course VARCHAR(30),
section VARCHAR(30),
course_code VARCHAR(20),
time VARCHAR(20),
day VARCHAR(20)
)
"""
cur.execute(query_create_database)


def on_close():
    response = messagebox.askyesno(
        "Close", "Are you sure you want to close the window?")
    if response:
        window.destroy()
        subprocess.run(["python", "./HomeScreen.py"])
    else:
        return


face_detector = cv2.CascadeClassifier(
    "./resources/haarcascade_frontalface_default.xml")


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


def face_recognition():
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


def check_student(sid, crs_cd):
    cur.execute(
        "SELECT student_id FROM students "
        f"WHERE student_id = '{sid}' AND course_code = '{crs_cd}'")
    result = cur.fetchone()
    if result is None:
        print(f"Student {sid} is not registered, Available!")
        return False
    else:
        return True


class AddStudentWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("659x967")
        self.master.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=967,
            width=659,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            329.0,
            484.0,
            image=self.image_image_1
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.submit,
            relief="flat",
            cursor="hand2"
        )
        self.button_1.place(
            x=235.0,
            y=889.0,
            width=190.0,
            height=58.0
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            329.5,
            153.0,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSans Bold", 16 * - 1),
        )
        self.entry_1.place(
            x=128.0,
            y=138.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            329.5,
            242.0,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSans Bold", 16 * - 1),
        )
        self.entry_2.place(
            x=128.0,
            y=227.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(
            329.5,
            331.0,
            image=self.entry_image_3
        )
        self.entry_3 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSans Bold", 16 * - 1),
        )
        self.entry_3.place(
            x=128.0,
            y=316.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        self.entry_bg_4 = self.canvas.create_image(
            329.5,
            420.0,
            image=self.entry_image_4
        )
        self.entry_4 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSans Bold", 16 * - 1),
        )
        self.entry_4.place(
            x=128.0,
            y=405.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_5 = PhotoImage(
            file=relative_to_assets("entry_5.png"))
        self.entry_bg_5 = self.canvas.create_image(
            329.5,
            509.0,
            image=self.entry_image_5
        )
        self.entry_5 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSans Bold", 16 * - 1),
        )
        self.entry_5.place(
            x=128.0,
            y=494.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_6 = PhotoImage(
            file=relative_to_assets("entry_6.png"))
        self.entry_bg_6 = self.canvas.create_image(
            329.5,
            637.0,
            image=self.entry_image_6
        )
        self.entry_6 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSans Bold", 16 * - 1),
        )
        self.entry_6.place(
            x=128.0,
            y=622.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_7 = PhotoImage(
            file=relative_to_assets("entry_7.png"))
        self.entry_bg_7 = self.canvas.create_image(
            329.5,
            726.0,
            image=self.entry_image_7
        )
        self.entry_7 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="grey",
            highlightthickness=0,
            font=("OpenSans Bold", 16 * - 1)
        )
        self.entry_7.place(
            x=128.0,
            y=711.0,
            width=403.0,
            height=28.0
        )

        self.entry_7.insert(0, "09:00 AM - 10:30 AM")
        self.entry_7.bind("<FocusIn>", self.on_focus_in)
        self.entry_7.bind("<FocusOut>", self.on_focus_out)

        self.entry_image_8 = PhotoImage(
            file=relative_to_assets("entry_8.png"))
        self.entry_bg_8 = self.canvas.create_image(
            329.5,
            815.0,
            image=self.entry_image_8
        )
        self.day = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]
        self.entry_8 = ttk.Combobox(
            background="#FFFFFF",
            foreground="#000716",
            font=("OpenSans Bold", 16 * - 1),
            state="readonly",
            values=self.day
        )
        self.entry_8.current(0)
        self.entry_8.bind("<FocusIn>", self.change_day)

        self.entry_8.place(
            x=128.0,
            y=800.0,
            width=403.0,
            height=28.0
        )

        self.canvas.create_text(
            102.0,
            99.0,
            anchor="nw",
            text="Firstname",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            102.0,
            188.0,
            anchor="nw",
            text="Lastname",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            102.0,
            277.0,
            anchor="nw",
            text="Student ID Number",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            102.0,
            366.0,
            anchor="nw",
            text="Course",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            102.0,
            455.0,
            anchor="nw",
            text="Section",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            102.0,
            583.0,
            anchor="nw",
            text="Course Code",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            102.0,
            672.0,
            anchor="nw",
            text="Time",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            102.0,
            761.0,
            anchor="nw",
            text="Day",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            263.0,
            40.0,
            anchor="nw",
            text="Add Students",
            fill="#9F9F9F",
            font=("OpenSansRoman Bold", 20 * -1)
        )

        self.canvas.create_text(
            289.0,
            77.0,
            anchor="nw",
            text="Student Info",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

        self.canvas.create_text(
            291.0,
            554.0,
            anchor="nw",
            text="Subject Info",
            fill="#9F9F9F",
            font=("OpenSansRoman Regular", 14 * -1)
        )

    def on_focus_in(self, event):
        if self.entry_7.get() == "09:00 AM - 10:30 AM":
            self.entry_7.delete(0, "end")
            self.entry_7.config(fg="#000716", )

    def on_focus_out(self, event):
        if not self.entry_7.get():
            self.entry_7.insert(0, "09:00 AM - 10:30 AM")
            self.entry_7.config(fg="grey")

    def change_day(self, event):
        selected_day = self.entry_8.get()
        print(selected_day)

    def submit(self):
        first_name = self.entry_1.get().capitalize()
        last_name = self.entry_2.get().capitalize()

        # format the student_id into XXXX-XXXXX
        student_id = self.entry_3.get()
        formatted_id = f'{student_id[:4]}-{student_id[5:]}'

        course = self.entry_4.get().upper()
        section = self.entry_5.get().upper()
        course_code = self.entry_6.get().upper()

        # formatted time into hh:mm or AM/PM
        time_schedule = self.entry_7.get().upper()
        formatted_time_am_am = (
            f'{time_schedule[:2]}:{time_schedule[3:5]} AM - '
            f'{time_schedule[11:13]}:{time_schedule[14:16]} AM'
        )

        formatted_time_am_pm = (
            f'{time_schedule[:2]}:{time_schedule[3:5]} AM - '
            f'{time_schedule[11:13]}:{time_schedule[14:16]} PM'
        )

        formatted_time_pm_am = (
            f'{time_schedule[:2]}:{time_schedule[3:5]} PM - '
            f'{time_schedule[11:13]}:{time_schedule[14:16]} AM'
        )

        formatted_time_pm_pm = (
            f'{time_schedule[:2]}:{time_schedule[3:5]} PM - '
            f'{time_schedule[11:13]}:{time_schedule[14:16]} PM'
        )

        day_schedule = self.entry_8.get().capitalize()

        if (
                first_name == "" or last_name == "" or
                student_id == "" or course == "" or
                section == "" or course_code == ""
        ):
            messagebox.showerror(
                "Error", "Please don't leave any empty fields."
            )

        elif (
                time_schedule != formatted_time_am_am and
                time_schedule != formatted_time_am_pm and
                time_schedule != formatted_time_pm_am and
                time_schedule != formatted_time_pm_pm
        ):

            messagebox.showerror(
                "Error", "Please enter valid time. It must be in the format 'hh:mm' AM/PM - 'hh:mm' AM/PM."
            )

        elif student_id != formatted_id:

            messagebox.showerror(
                "Error", "Invalid Student ID. It must be in the format of XXXX-XXXXX.")

        else:
            exists = check_student(student_id, course_code)
            if exists:
                messagebox.showerror(
                    "Error",
                    f"Student {student_id} is already registered in course {course_code}."
                )
            else:
                self.push_to_database(
                    first_name, last_name,
                    student_id, course,
                    section, course_code,
                    time_schedule, day_schedule
                )

    def push_to_database(self, fn, ln, sid, crs, sc, crs_cd, ts, ds):

        query_insert = """
        INSERT INTO students (
        firstname, lastname,
        student_id, course,
        section, course_code,
        time, day
        )
        """
        values = f"""
        VALUES (
        '{fn}', '{ln}', '{sid}', 
        '{crs}', '{sc}', '{crs_cd}',
        '{ts}', '{ds}'
        )
        """
        cur.execute(query_insert + values)
        db.commit()

        cur.execute(
            "SELECT * FROM students"
        )
        for x in cur:
            print(x)
        print(cur.rowcount, " students added")

        # create dir if no exist
        if not os.path.isdir('Attendance'):
            os.makedirs('Attendance')
        if not os.path.isdir('static/faces'):
            os.makedirs('static/faces')
        if f'Students-{crs_cd}.csv' not in os.listdir('Attendance'):
            with open(f'./Attendance/Student-{crs_cd}.csv', 'w') as f:
                f.write(
                    'Student Id,First name,Last name,Course,Section,Course Code,Time,Day')

        # push to csv file
        with open(f'./Attendance/Students-{crs_cd}.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([sid, fn, ln, crs, sc, crs_cd, ts, ds])
        self.add()

    def clear_fields(self):
        self.entry_1.delete("0", END)
        self.entry_2.delete("0", END)
        self.entry_3.delete("0", END)
        self.entry_4.delete("0", END)
        self.entry_5.delete("0", END)
        self.entry_6.delete("0", END)

    def add(self):
        student_id = self.entry_3.get()
        course_code = self.entry_6.get().upper()

        user_image_folder = f"./static/faces/{student_id}_{course_code}"

        if not os.path.isdir(user_image_folder):
            os.makedirs(user_image_folder)
        cam = cv2.VideoCapture(0)
        i, j = 0, 0
        while True:
            _, frame = cam.read()
            faces = extract_face(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
                cv2.putText(frame, f'Images Captured: {i}/50', (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
                if j % 10 == 0:
                    name = f"{student_id}_{course_code}_{i}.jpg"
                    cv2.imwrite(f"{user_image_folder}/{name}",
                                frame[y:y + h, x:x + w])
                    i += 1
                j += 1
            if j == 500:
                break
            cv2.imshow("Adding new user", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                r = messagebox.askyesno(
                    "Exit",
                    "Are you sure you want to exit?"
                )
                if r:
                    break
                else:
                    continue
            if cv2.waitKey(1) & 0xFF == ord(' '):
                r = messagebox.askyesno(
                    "Exit",
                    "Are you sure you want to exit?"
                )
                if r:
                    break
                else:
                    continue

        cam.release()
        cv2.destroyAllWindows()
        print("Training Models")
        train_model()

        response = messagebox.askyesno(
            "Success",
            f"Student {student_id} has been registered in course {course_code}."
            f"Do you want to clear all fields?"
        )
        if response:
            self.clear_fields()
        else:
            return

    # component testing function
    def test_submit(self):
        first_name = self.entry_1.get()
        last_name = self.entry_2.get()
        student_id = self.entry_3.get()
        course = self.entry_4.get()
        section = self.entry_5.get()
        course_code = self.entry_6.get()

        print(
            first_name, last_name, student_id,
            course, section, course_code
        )


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
app = AddStudentWindow(window)
window.resizable(False, False)
window.mainloop()
