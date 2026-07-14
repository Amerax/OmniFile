import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def convert_image(input_path, target_format):
    target_format = target_format.strip().lower()
    format_mapping = {
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'png': 'PNG',
        'webp': 'WEBP'
    }
    
    if target_format not in format_mapping:
        print(f"Unsupported target format: {target_format}")
        return

    if not os.path.exists(input_path):
        print("Error: Input file does not exist.")
        return

    try:
        # try open img
        with Image.open(input_path) as img:
            if img.mode in ('RGBA', 'LA') and format_mapping[target_format] == 'JPEG':
                img = img.convert('RGB')
                
            # new file 
            base_path, _ = os.path.splitext(input_path)
            output_path = f"{base_path}.{target_format}"
            
            # Save 
            img.save(output_path, format_mapping[target_format])
            print(f"Success! Saved converted file to: {output_path}")
            
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

def main():
    print("=== Simple Image Converter ===")
    input_path = input("Enter the path to the image file (e.g., image.png): ").strip(' "')
    target_format = input("Enter target format (jpg, png, webp): ").strip()
    
    convert_image(input_path, target_format)
    input("\nPress Enter to exit...") # keeps the window open 

# simple gui interface 

root = tk.Tk()
root.title("Simple Image Converter")
root.geometry("420x180")
root.resizable(False, False)

tk.Label(root, text="Image File").pack(pady=(10, 0))

path_entry = tk.Entry(root, width=45)
path_entry.pack()

tk.Button(root, text="Browse", command=browse_file).pack(pady=5)
tk.Label(root, text="Convert To").pack()
format_var = tk.StringVar(value="png")
formats = ["jpg", "png", "webp"]
tk.OptionMenu(root, format_var, *formats).pack()

tk.Button(root, text="Convert", width=15, command=convert).pack(pady=15)

root.mainloop()

if __name__ == "__main__":
    main()
