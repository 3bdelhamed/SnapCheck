import os.path
import datetime
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import numpy as np
import pickle
import mysql.connector
import util


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        screen_width = 1920
        screen_height = 1080
        window_width = 1200
        window_height = 520
        x_offset = (screen_width - window_width) // 4
        y_offset = (screen_height - window_height) // 4

        self.main_window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

        

        self.main_window.configure(bg='#614BC3')

        self.login_button_main_window = util.img_button(
            self.main_window, self.login,
            img_path="style/button_login.png",
            active_img_path="style/activebackground.png"
        )
        self.login_button_main_window.place(x=875, y=350)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        self.webcam_label.config(bg='#614BC0')

        self.add_webcam(self.webcam_label)



        self.log_path = './log.txt'

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="face_recognition_db",
        )

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        known_encodings, known_names = self.get_known_encodings_from_db()

        if not known_encodings:
            util.msg_box('Error', 'No registered users found in the database.')
            return

        face_encoding = util.get_face_encoding(self.most_recent_capture_arr)

        if face_encoding is None:
            util.msg_box('Error', 'No face detected. Please try again.')
            return

        matches = face_recognition.compare_faces(known_encodings, face_encoding)

        if True in matches:
            name = known_names[np.argmax(matches)]
            util.msg_box('Welcome back!', 'Welcome, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
        else:
            util.msg_box('Unknown User', 'Unknown user. Please register a new user or try again.')

    def get_known_encodings_from_db(self):
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute("SELECT name, encodings FROM employee_data")
            results = cursor.fetchall()

            known_encodings = []
            known_names = []

            for result in results:
                name = result['name']
                encodings_pickle = result['encodings']
                encodings = pickle.loads(encodings_pickle)

                known_names.append(name)
                known_encodings.append(encodings)

            cursor.close()
            return known_encodings, known_names

        except Exception as e:
            print(f"Error in get_known_encodings_from_db: {e}")
            return None, None

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(
            self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user
        )
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(
            self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user
        )
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(
            self.register_new_user_window, 'Please, \ninput username:'
        )
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()
        self.register_new_user()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        file_path = os.path.join(self.db_dir, '{}.pickle'.format(name))
        with open(file_path, 'wb') as file:
            pickle.dump(embeddings, file)

        util.msg_box('Success!', 'User was registered successfully!')

        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
