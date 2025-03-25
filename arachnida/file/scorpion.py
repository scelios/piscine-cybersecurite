import os
import sys
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image, ExifTags, ImageTk
from PIL.ExifTags import TAGS
import time
import struct

def check_file(file):
    authorise = ["jpg", "jpeg", "png", "gif", "bmp"]
    if os.path.exists(file) and os.path.isfile(file) and os.path.getsize(file) > 0:
        if file.split(".")[-1].lower() in authorise:
            return True
    return False


def show_exif(file):
    image = Image.open(file)
    exif_data = image._getexif()
    if exif_data is not None:
        exif_text = ""
        filename = file.split("/")[-1]
        exif_text += f"File: {filename}\n"
        file_size = os.path.getsize(file)
        file_access_time = time.ctime(os.path.getatime(file))
        file_modify_date = time.ctime(os.path.getmtime(file))
        file_type = file.split(".")[-1].lower()
        file_permission = oct(os.stat(file).st_mode)[-3:]
        file_width, file_height = image.size
        file_endian = 'Little-endian' if struct.unpack('<H', b'\x01\x00')[0] == 1 else 'Big-endian'

        exif_text += f"File Size: {file_size} bytes\n"
        exif_text += f"File Access Time: {file_access_time}\n"
        exif_text += f"File Modify Date: {file_modify_date}\n"
        exif_text += f"File Type: {file_type}\n"
        exif_text += f"File Permissions: {file_permission}\n"
        exif_text += f"Image Width: {file_width} pixels\n"
        exif_text += f"Image Height: {file_height} pixels\n"
        exif_text += f"Image Endian: {file_endian}\n"
        for key, val in exif_data.items():
            if key in ExifTags.TAGS:
                exif_text += f"{ExifTags.TAGS[key]}: {val}\n"
            else:
                exif_text += f"'{key}' -> '{val}'\n"
        show_exif_gui_and_images(exif_text, file)
    else:
        file = file.split("/")[-1]
        # print(f"{file} No EXIF data found")

def show_exif_gui_and_images(exif_text, file):
    root = Tk()
    image = Image.open(file)
    file_name = file.split("/")[-1]
    root.title(file_name)
    root.geometry("800x300")

    img_width, img_height = image.size
    max_size = 300
    if img_width > max_size or img_height > max_size:
        scale = min(max_size / img_width, max_size / img_height)
        img_width = int(img_width * scale)
        img_height = int(img_height * scale)
    image = image.resize((img_width, img_height))

    img_label = Label(root)
    img_label.pack(side="left", padx=10, pady=10)
    img = ImageTk.PhotoImage(image)
    img_label.config(image=img)
    img_label.image = img

    exif_frame = Label(root, text=exif_text, justify="left", anchor="nw")
    exif_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    root.mainloop()

def main():
    args = sys.argv[1:]
    if not args:
        args = ["-h"]
    if args[0] == "-h":
        print("Usage: python scorpion.py [-h]  PATH ")
        print("Process some arguments.")
        print("Arguments:")
        print("  PATH          Path to your image file")
        sys.exit(0)
    try:
        for arg in args:
            if check_file(arg) is True:
                show_exif(arg)
            else:
                print(f"File {arg} not found or not supported")
                sys.exit(1)
    except KeyboardInterrupt:
        print("The program was interrupted by the user")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()