

from pathlib import Path
import subprocess
import time

import cv2

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, messagebox, ttk

import mysql.connector as con

from logic import checkInputAddStudent

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
    Path(r"./assets/frame7")


ASSETS_PATH_ADD_WINDOW = OUTPUT_PATH / Path(r"./assets/frame7")


def add_window_assets(path: str) -> Path:
    return ASSETS_PATH_ADD_WINDOW / Path(path)


def on_close():
    response = messagebox.askokcancel(
        "Close", "Are you sure you want to close the window?")
    if response:
        window.destroy()
        subprocess.run(["python", "./HomeScreen.py"])
    else:
        None


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
            file=add_window_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            329.0,
            153.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=add_window_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            329.0,
            242.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=add_window_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            329.0,
            331.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=add_window_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(
            329.0,
            420.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=add_window_assets("image_5.png"))
        self.image_5 = self.canvas.create_image(
            329.0,
            509.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=add_window_assets("image_6.png"))
        self.image_6 = self.canvas.create_image(
            329.0,
            637.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=add_window_assets("image_7.png"))
        self.image_7 = self.canvas.create_image(
            329.0,
            726.0,
            image=self.image_image_7
        )

        self.image_image_8 = PhotoImage(
            file=add_window_assets("image_8.png"))
        self.image_8 = self.canvas.create_image(
            329.0,
            815.0,
            image=self.image_image_8
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

        self.entry_image_1 = PhotoImage(
            file=add_window_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            329.5,
            153.0,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 16 * -1),
        )
        self.entry_1.place(
            x=128.0,
            y=138.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_2 = PhotoImage(
            file=add_window_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            329.5,
            242.0,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 16 * -1)
        )
        self.entry_2.place(
            x=128.0,
            y=227.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_3 = PhotoImage(
            file=add_window_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(
            329.5,
            331.0,
            image=self.entry_image_3
        )
        self.entry_3 = Entry(
            self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 16 * -1),
        )
        self.entry_3.place(
            x=128.0,
            y=316.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_4 = PhotoImage(
            file=add_window_assets("entry_4.png"))
        self.entry_bg_4 = self.canvas.create_image(
            329.5,
            420.0,
            image=self.entry_image_4
        )
        self.entry_4 = Entry(
            self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 16 * -1)
        )
        self.entry_4.place(
            x=128.0,
            y=405.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_5 = PhotoImage(
            file=add_window_assets("entry_5.png"))
        self.entry_bg_5 = self.canvas.create_image(
            329.5,
            509.0,
            image=self.entry_image_5
        )
        self.entry_5 = Entry(
            self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 16 * -1)
        )
        self.entry_5.place(
            x=128.0,
            y=494.0,
            width=403.0,
            height=28.0
        )

        self.entry_image_6 = PhotoImage(
            file=add_window_assets("entry_6.png"))
        self.entry_bg_6 = self.canvas.create_image(
            329.5,
            637.0,
            image=self.entry_image_6
        )
        self.entry_6 = Entry(
            self.master,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 16 * -1)
        )
        self.entry_6.place(
            x=128.0,
            y=622.0,
            width=403.0,
            height=28.0
        )

        # time entry
        self.entry_image_7 = PhotoImage(
            file=add_window_assets("entry_7.png"))
        self.entry_bg_7 = self.canvas.create_image(
            329.5,
            726.0,
            image=self.entry_image_7
        )
        self.entry_7 = Entry(
            self.master,
            bd=0,
            bg="#FFFFFF",
            fg="grey",
            highlightthickness=0,
            font=("OpenSansRoman Regular", 16 * -1)
        )
        self.entry_7.place(
            x=128.0,
            y=711.0,
            width=403.0,
            height=28.0
        )
        self.entry_7.insert(0, "9 am - 10:30 pm")
        self.entry_7.bind("<FocusIn>", self.entry_7_focus_in)
        self.entry_7.bind("<FocusOut>", self.entry_7_focus_out)

        # values of the day
        self.day = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]

        self.entry_image_8 = PhotoImage(
            file=add_window_assets("entry_8.png"))
        self.entry_bg_8 = self.canvas.create_image(
            329.5,
            815.0,
            image=self.entry_image_8
        )
        self.entry_8 = ttk.Combobox(
            self.master,
            background="#FFFFFF",
            foreground="#000716",
            state="readonly",
            takefocus=False,
            cursor="hand2",
            font=("OpenSansRoman Regular", 16 * -1),
            values=self.day,

        )
        self.entry_8.place(
            x=128.0,
            y=800.0,
            width=403.0,
            height=28.0
        )
        self.entry_8.current(0)
        self.entry_8.bind("<<ComboboxSelected>>", self.change_day)

        self.button_image_1 = PhotoImage(
            file=add_window_assets("button_1.png"))
        self.button_1 = Button(
            self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.Camera,
            relief="flat",
            cursor="hand2"
        )
        self.button_1.place(
            x=235.0,
            y=889.0,
            width=190.0,
            height=58.0
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

    def entry_7_focus_in(self, event):
        if self.entry_7.get() == "9 am - 10:30 pm":
            self.entry_7.delete(0, "end")
            self.entry_7.config(fg="#000716",)

    def entry_7_focus_out(self, event):
        if not self.entry_7.get():
            self.entry_7.insert(0, "9 am - 10:30 pm")
            self.entry_7.config(fg="grey")

    def change_day(self, event):
        selected_day = self.entry_8.get()
        print(selected_day)

    def submit_students(self):
        fname = self.entry_1.get()
        lname = self.entry_2.get()
        student_id = self.entry_3.get()
        course = self.entry_4.get()
        section = self.entry_5.get()
        course_code = self.entry_6.get()
        time = self.entry_7.get()
        day = self.entry_8.get()
        c = checkInputAddStudent(
            fname, lname, student_id, course, section, course_code, time, day)
        if c:
            conn = con.connect(
                host="localhost",
                user="root",
                password="root",
                database="mydb"
            )
            cursor = conn.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS students \
                (id INT AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(40), lastname VARCHAR(40), \
                student_id VARCHAR(10), course VARCHAR(100), section VARCHAR(30), \
                course_code VARCHAR(20), time VARCHAR(20), \
                day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))")

            cursor.execute(
                f"SELECT * FROM students WHERE student_id='{student_id}' AND course_code='{course_code}'")
            check = cursor.fetchone()
            if check is None:
                cursor.execute(
                    f"INSERT INTO students (firstname, lastname, student_id, course, section, course_code, time, day) VALUES ('{fname}', '{lname}', '{student_id}', '{course}', '{section}', '{course_code}', '{time}', '{day}')")
                conn.commit()
                cursor.execute("SELECT * FROM students")
                records = cursor.fetchall()
                for record in records:
                    print(record)
                print(cursor.rowcount, "records inserted")
            else:
                messagebox.showerror(
                    "Error", f"Student {student_id} already exists")
        else:
            messagebox.showerror("Error", "Please fill all the fields")

    def Camera(self):
        confirmation = messagebox.askyesno(
            "Confirm", "Please make sure the data is correct. Are you sure you want to continue?")
        if confirmation:
            student_id = self.entry_3.get()
            cam = cv2.VideoCapture(0)
            cam.set(3, 640)
            cam.set(4, 480)

            if not cam.isOpened():
                messagebox.showerror("Error", "Camera could not be opened")

            while True:
                ret, frame = cam.read()

                if ret:
                    cv2.imshow("Face Capture", frame)

                key = cv2.waitKey(1)

                if key == ord("q"):
                    response = messagebox.askyesno(
                        "Close the Camera", "Are you sure you want to close the camera?")
                    if response:
                        break
                    else:
                        None
                elif key == ord(" "):
                    captured = self.Capture(student_id, frame)
                    if captured:
                        cam.release()
                        cv2.destroyAllWindows()
                        response = messagebox.askyesno(
                            "Success",
                            f"Student {student_id} has been added successfully. Do you want to clear all the fields?")
                        if response:
                            self.master.destroy()
                            subprocess.run(
                                ["python", "./AddStudentsWindow.py"])
                        else:
                            return
                    else:
                        return
            cam.release()
            cv2.destroyAllWindows()
        else:
            return

    def Capture(self, sid, frame):

        # convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in grayscal frame
        face_cascade = cv2.CascadeClassifier(
            "./resources/haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

        # save if there is exactly one face detected
        if len(faces) == 1:
            self.submit_students()
            cv2.imwrite(f"./data/{sid}.jpg", frame)
            return True
        else:
            messagebox.showerror(
                "Error", "Could not detect your face. Please try again.")
            return False


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
app = AddStudentWindow(window)
window.resizable(False, False)
window.mainloop()
