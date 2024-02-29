import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import face_recognition
import mysql.connector
import pickle

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        foreground_color = 'blue'
        button_foreground_color = 'white'
        button_background_color = 'green'

        self.name_label = tk.Label(root, text="Name:", foreground=foreground_color)
        self.name_entry = tk.Entry(root, background='lightyellow')

        self.dep_label = tk.Label(root, text="Department:", foreground=foreground_color)
        self.dep_var = tk.StringVar()
        self.dep_var.set("AI")
        self.dep_radios = [
            ttk.Radiobutton(root, text="AI", variable=self.dep_var, value="AI", style="TRadiobutton", command=self.radio_command),
            ttk.Radiobutton(root, text="Bio", variable=self.dep_var, value="Bio", style="TRadiobutton", command=self.radio_command),
            ttk.Radiobutton(root, text="SW", variable=self.dep_var, value="SW", style="TRadiobutton", command=self.radio_command),
        ]

        self.image_label = tk.Label(root, text="Image:", foreground=foreground_color)
        self.image_path = ""
        self.image_label_display = tk.Label(root)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_image, foreground=button_foreground_color, background=button_background_color)

        self.save_button = tk.Button(root, text="Save", command=self.save_data, foreground=button_foreground_color, background=button_background_color)

        # Grid layout
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.dep_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        for i, radio in enumerate(self.dep_radios):
            radio.grid(row=1, column=i + 1, padx=10, pady=10, sticky="w")

        self.image_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.image_label_display.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.browse_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.save_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Radiobutton style configuration
        self.root.style = ttk.Style()
        self.root.style.configure("TRadiobutton", foreground=foreground_color)

    def browse_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            image = Image.open(self.image_path)
            image.thumbnail((150, 150))
            photo = ImageTk.PhotoImage(image)
            self.image_label_display.config(image=photo)
            self.image_label_display.image = photo

    def save_data(self):
        name = self.name_entry.get()
        department = self.dep_var.get()

        if name and department and self.image_path:
            encodings = self.get_face_encodings(self.image_path)

            if encodings:
                if len(encodings) > 1:
                    print("Warning: Multiple faces detected. Saving the first encoding.")
                
                self.save_to_database(name, department, self.image_path, encodings[0])
                print("Data saved successfully!")
            else:
                print("Error: Unable to extract face encodings from the image.")
        else:
            print("Error: Please provide all required information.")

    def get_face_encodings(self, image_path):
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            return encodings if encodings else []  
        except Exception as e:
            print(f"Error in get_face_encodings: {e}")
            return []

    def save_to_database(self, name, department, image_path, encodings):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognition_db",
            )

            encodings_pickle = pickle.dumps(encodings)

            cursor = connection.cursor()

            insert_query = "INSERT INTO employee_data (name, department, image_path, encodings) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, department, image_path, encodings_pickle))

            connection.commit()
            cursor.close()
            connection.close()

        except Exception as e:
            print(f"Error in save_to_database: {e}")

    def radio_command(self):
        print(f"Selected Department: {self.dep_var.get()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
