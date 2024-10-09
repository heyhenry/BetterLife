import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()

def open_image():
    file_path = filedialog.askopenfilename(title='Save Image File', filetypes=[('Image Files', '*.png *.jpeg *.jpg')])
    if file_path:
        save_image(file_path)

def save_image(file_path):
    image = Image.open(file_path)
    image.save('img/first.jpg')
    # photo = ImageTk.PhotoImage(image)

open_button = tk.Button(root, text='Open Image', command=open_image)
open_button.pack()

root.mainloop()