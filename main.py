import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from moviepy import AudioFileClip, VideoFileClip

selected_file = ""

def browse():
    global selected_file
    selected_file = filedialog.askopenfilename()
    if selected_file:
        file_label.config(text=os.path.basename(selected_file))

def convert():
    if not selected_file:
        messagebox.showerror("Error", "Select a file first")
        return

    target = format_var.get().lower()
    ext = os.path.splitext(selected_file)[1].lower()

    try:
        # image conversion
        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            formats = {
                "jpg": "JPEG",
                "jpeg": "JPEG",
                "png": "PNG",
                "webp": "WEBP"
            }

            if target not in formats:
                raise Exception("Invalid image format.")

            img = Image.open(selected_file)

            if target == "jpg" and img.mode == "RGBA":
                img = img.convert("RGB")

            out = os.path.splitext(selected_file)[0] + "." + target
            img.save(out, formats[target])

        # audio conversion
        elif ext in [".mp3", ".wav"]:
            out = os.path.splitext(selected_file)[0] + "." + target

            clip = AudioFileClip(selected_file)

            if target == "mp3":
                clip.write_audiofile(out)

            elif target == "wav":
                clip.write_audiofile(out, codec="pcm_s16le")

            else:
                raise Exception("Invalid audio format")

            clip.close()

        # video conversion handler
        elif ext == ".mp4":
            if target != "mp4":
                raise Exception("MP4 can only convert to MP4.")

            out = os.path.splitext(selected_file)[0] + "_copy.mp4"

            clip = VideoFileClip(selected_file)
            clip.write_videofile(out)
            clip.close()

        else:
            raise Exception("Unsupported file. Please check readme for supported types")

        messagebox.showinfo("Done", "Conversion complete!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# gui

root = tk.Tk()
root.title("Simple File Converter")
root.geometry("350x180")
root.resizable(False, False)

tk.Button(root, text="Browse File", command=browse).pack(pady=10)

file_label = tk.Label(root, text="No file selected")
file_label.pack()

format_var = tk.StringVar(value="png")

tk.Label(root, text="Output Format").pack(pady=(10, 0))

options = [
    "jpg",
    "png",
    "webp",
    "mp3",
    "wav",
    "mp4"
]

tk.OptionMenu(root, format_var, *options).pack()
tk.Button(root, text="Convert", command=convert).pack(pady=15)

root.mainloop()
