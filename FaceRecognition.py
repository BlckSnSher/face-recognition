from tkinter import messagebox
import face_recognition
import cv2
import numpy as np


class FaceRecognition:
    def __init__(self, id):
        self.id = id

        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640)
        self.cam.set(4, 480)

        student_image = face_recognition.load_image_file(
            f"./data/{self.id}.jpg")
        student_face_encoding = face_recognition.face_encodings(student_image)[
            0]

        known_face_encodings = [
            student_face_encoding
        ]

        known_face_name = [
            self.id
        ]

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        while True:
            ret, frame = self.cam.read()

            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(
                    rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)

                face_names = []

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_face_name[best_match_index]
                        self.cam.release()
                        cv2.destroyAllWindows()
                    face_names.append(name)
                    print(face_names)
                    print("Success")
            process_this_frame = not process_this_frame
