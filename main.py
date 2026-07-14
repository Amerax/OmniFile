import os
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

if __name__ == "__main__":
    main()
