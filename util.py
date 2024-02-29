import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
import face_recognition



def img_button(window, command, img_path, active_img_path=None):
    img = PhotoImage(file=img_path)
    active_img = PhotoImage(file=active_img_path) if active_img_path else None

    button = tk.Label(
        window,
        image=img,
        bd=0,  
        highlightthickness=0,  
        bg=window.cget("bg")
    )
    button.img = img  

    def on_click(event):
        command()

    def on_enter(event):
        if active_img:
            button.config(image=active_img)

    def on_leave(event):
        button.config(image=img)

    button.bind("<Button-1>", on_click)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return button

def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground="#15F5BA",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=10,
        font=('Helvetica bold', 20)
    )

    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title, description)


def get_face_encoding(image):
    try:
        face_encoding = face_recognition.face_encodings(image)
        return face_encoding[0] if face_encoding else None
    except Exception as e:
        print(f"Error in get_face_encoding: {e}")
        return None
