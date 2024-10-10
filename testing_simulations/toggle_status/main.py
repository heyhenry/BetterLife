import tkinter as tk
from PIL import Image, ImageTk

toggle = True

root = tk.Tk()

def toggle_status(mouse_event, text_widget, label_widget):
    global toggle
    if toggle:
        text_widget.config(text='Stay Logged Off: Off')
        label_widget.config(image=img_off)
        toggle = False
    else:
        text_widget.config(text='Stay Logged In: On')
        label_widget.config(image=img_on)
        toggle = True

max_size = (50, 50)

img_off = Image.open('img/switch-off.png')
img_off.thumbnail(max_size)
img_off = ImageTk.PhotoImage(img_off)

img_on = Image.open('img/switch-on.png')
img_on.thumbnail(max_size)
img_on = ImageTk.PhotoImage(img_on)

status_text = tk.Label(root, text='Stay Logged In')
status = tk.Label(root, image=img_on)

status_text.pack()
status.pack()

status.bind('<Button-1>', lambda mouse_event: toggle_status(mouse_event, status_text, status))


root.mainloop()