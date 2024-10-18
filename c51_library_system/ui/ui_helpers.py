import os
import tkinter as tk
from PIL import Image, ImageTk


BACKGROUND_PATH = os.path.join("D:\\CodeAcademy\\c51_library_system\\background", "background.png")

def set_background(root, canvas_width=1400, canvas_height=800):
    original_image = Image.open(BACKGROUND_PATH)
    resized_image = original_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(resized_image)
    
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")
    
    return canvas, background_photo