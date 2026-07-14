import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from moviepy import AudioFileClip, VideoFileClip
import pandas as pd

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
    out = os.path.splitext(selected_file)[0] + "." + target

    try:
        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            formats = {"jpg":"JPEG","jpeg":"JPEG","png":"PNG","webp":"WEBP"}

            if target not in formats:
                raise Exception("Invalid image format.")

            img = Image.open(selected_file)

            if target == "jpg" and img.mode == "RGBA":
                img = img.convert("RGB")

            img.save(out, formats[target])

        elif ext in [".mp3", ".wav"]:
            clip = AudioFileClip(selected_file)

            if target == "mp3":
                clip.write_audiofile(out)
            elif target == "wav":
                clip.write_audiofile(out, codec="pcm_s16le")
            else:
                raise Exception("Invalid audio formae.")

            clip.close()

        elif ext == ".mp4":
            clip = VideoFileClip(selected_file)

            if target == "mp4":
                clip.write_videofile(out)
            elif target == "mp3":
                clip.audio.write_audiofile(out)
            elif target == "wav":
                clip.audio.write_audiofile(out, codec="pcm_s16le")
            else:
                clip.close()
                raise Exception("Invalid vido format")

            clip.close()

        elif ext == ".csv":
            df = pd.read_csv(selected_file)

            if target == "xlsx":
                df.to_excel(out, index=False)
            elif target == "json":
                df.to_json(out, orient="records", indent=4)
            else:
                raise Exception("CSV can only convert to XLSX or JSON, read redme to double check what you can convert to.")

        elif ext == ".xlsx":
            df = pd.read_excel(selected_file)

            if target == "csv":
                df.to_csv(out, index=False)
            elif target == "json":
                df.to_json(out, orient="records", indent=4)
            else:
                raise Exception("Excel can only convert to csv or json.")

        elif ext == ".json":
            df = pd.read_json(selected_file)

            if target == "csv":
                df.to_csv(out, index=False)
            elif target == "xlsx":
                df.to_excel(out, index=False)
            else:
                raise Exception("JSON can only convert to CSV or XLSX.")

        else:
            raise Exception("Unsupported file type sorry.")

        messagebox.showinfo(
    "Done",
    f"Conversion complete!\n\nSaved to:\n{out}"
)

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Simple File Converter")
root.geometry("350x180")
root.resizable(False, False)

tk.Button(root, text="Browse File", command=browse).pack(pady=10)

file_label = tk.Label(root, text="No file selected")
file_label.pack()
format_var = tk.StringVar(value="png")

tk.Label(root, text="Output Format").pack(pady=(10,0))

options = [
    "jpg","png","webp",
    "mp3","wav","mp4",
    "csv","xlsx","json"
]

tk.OptionMenu(root, format_var, *options).pack()
tk.Button(root, text="Convert", command=convert).pack(pady=15)

root.mainloop()
