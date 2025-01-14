import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog


def convert_image_to_webp(folder_path):
    converted_image_names = []
    for root,_,files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png','.jpg','jpeg')):
                image_path = os.path.join(root, file)
                image_size = os.path.getsize(image_path) / 1024
                
                if image_size > 100:
                    webp_path = os.path.splitext(image_path)[0] + '.webp'
                    with Image.open(image_path) as img:
                        img.save(webp_path, 'WEBP', quality=75)
                    os.remove(image_path)
                    print(f"converted from "+image_path+" to "+webp_path)
                    converted_image_names.append((image_path, webp_path))
    return converted_image_names

def update_code_files(folder_path, converted_names):
    code_extensions = ('.dart','.java','.kt')
    for root,_,files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(code_extensions):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    line_ending = None
                    if '\r\n' in content:
                        line_ending = '\r\n'
                    elif '\n' in content:
                        line_ending = '\n'
                    elif '\r' in content:
                        line_ending = '\r'
                
                needs_update = False
                for original_path,webp_path in converted_names:
                    original = os.path.basename(original_path)
                    webp = os.path.basename(webp_path)
                    if original in content:
                        needs_update = True
                        content = content.replace(original, webp)
                if needs_update:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        if(line_ending):
                            content = content.replace('\r\n','\n').replace('\r','\n').replace('\n',line_ending)
                        f.write(content)
                    print(f"updated file: "+file_path)

# def select_folder(title="select a folder"):
#     root = tk.Tk()
#     root.withdraw()
#     folder_path = filedialog.askdirectory(title=title)
#     return folder_path

if __name__ == "__main__":
    image_folder = ""
    if not image_folder:
        exit()
    code_folder = ""
    if not code_folder:
        exit()
    converted_images = convert_image_to_webp(image_folder)
    update_code_files(code_folder, converted_images)