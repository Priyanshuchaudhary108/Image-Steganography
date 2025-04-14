from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import itertools
import tkinter

def encode_message(image, message):

    binary_data = [format(ord(i), '08b') for i in message]
    binary_data.append('00000000')

    width, height = image.size
    pixels = image.load()
    data_index = 0
    bit_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            
            for i in range(3):

                if data_index < len(binary_data):
                    pixel[i] = pixel[i] & ~1 | int(binary_data[data_index][bit_index])
                    bit_index += 1
                
                    if bit_index == 8:
                        data_index += 1
                        bit_index = 0
            
            pixels[x, y] = tuple(pixel)
            if data_index == len(binary_data):
                return image

def decode_message(image):
    
    width, height = image.size
    pixels = image.load()
    binary_data = ""
    
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i : i + 8]
        if byte == '00000000':  
            return message
        message += chr(int(byte, 2))

def select_image(label, mode):
    
    global file_path
    image_extensions = ["avif", "jpg", "jpeg", "png", "svg"]
    image_extensions_cases = []
    
    for extension in image_extensions:
        chars = ((char.lower(), char.upper()) for char in extension)
        for letters in itertools.product(*chars):
            image_extensions_cases.append('*.' + ''.join(letters))
    
    file_types = [('test files', image_extensions_cases), ('All files', '*'),]
    file_path = filedialog.askopenfilename(title = f"Select image to {mode}", filetypes = file_types)
    
    if file_path:
        label.config(text = file_path.split("/")[-1])

def encode_input():

    encode_input_window = tkinter.Toplevel()
    encode_input_window.title("Encode")
    encode_input_window.geometry("+440+125")
    encode_input_window.resizable("False", "False")
    encode_input_window.tk.call("wm", "iconphoto", encode_input_window._w, icon_image)

    message_label = ttk.Label(encode_input_window, text = "Secret Message", font = ("Times New Roman", 16))
    message_entry = ttk.Entry(encode_input_window, width = 25, font = ("Times New Roman", 16))
    source_label = ttk.Label(encode_input_window, text = "Select Image", font = ("Times New Roman", 16))
    source_name_label = ttk.Label(encode_input_window, text = "No Image Selected", font = ("Times New Roman", 16))
    select_image_button = ttk.Button(encode_input_window, image = select_pic, command = lambda: select_image(source_name_label, "encode"))
    encode_button = ttk.Button(encode_input_window, text = "Encode", command = lambda: encode_action(message_entry.get(), encode_input_window), style = "my.TButton")

    message_label.grid(row = 0, column = 0)
    message_entry.grid(row = 0, column = 1, padx = 5, pady = 5, columnspan = 2)
    source_label.grid(row = 1, column = 0, pady = 5)
    source_name_label.grid(row = 1, column = 1, pady = 5)
    select_image_button.grid(row = 1, column = 2, pady = 5)
    encode_button.grid(row = 2, column = 1, pady = 5)

    encode_input_window.mainloop()

def encode_action(message, encode_input_window):
    
    if not file_path:
        return
    
    image = Image.open(file_path).convert('RGB')
    encoded_image = encode_message(image, message)
    
    save_image_window = tkinter.Toplevel()
    save_image_window.title("Save Encoded Image")
    save_image_window.geometry("+490+175")
    save_image_window.resizable("False", "False")
    save_image_window.tk.call("wm", "iconphoto", save_image_window._w, icon_image)

    def save_image():
        file = filedialog.asksaveasfilename(defaultextension = ".png", filetypes = [('PNG Image', '*.png')])
        if file:
            encoded_image.save(file)
        save_image_window.destroy()

    info_label = ttk.Label(save_image_window, text = "Message successfully encoded", font = ("Times New Roman", 16))
    save_button = ttk.Button(save_image_window, text = "Save Image", command = save_image, style = "my.TButton")

    info_label.pack(padx = 10, pady = 10)
    save_button.pack(pady = 10)

    encode_input_window.destroy()
    save_image_window.mainloop()

def decode_input():

    decode_input_window = tkinter.Toplevel()
    decode_input_window.title("Decode")
    decode_input_window.geometry("+580+125")
    decode_input_window.resizable("False", "False")
    decode_input_window.tk.call("wm", "iconphoto", decode_input_window._w, icon_image)

    source_label = ttk.Label(decode_input_window, text = "Select Image", font = ("Times New Roman", 18))
    source_name_label = ttk.Label(decode_input_window, text = "No Image Selected", font = ("Times New Roman", 18))
    select_image_button = ttk.Button(decode_input_window, image = select_pic, command = lambda: select_image(source_name_label, "decode"))
    decode_button = ttk.Button(decode_input_window, text = "Decode", command = lambda: decode_action(decode_input_window), style = "my.TButton")

    source_label.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    source_name_label.grid(row = 1, column = 0, padx = 5)
    select_image_button.grid(row = 1, column = 1, padx = 5)
    decode_button.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5)

    decode_input_window.mainloop()

def decode_action(decode_input_window):
    
    if not file_path:
        return
    
    image = Image.open(file_path)
    secret_message = decode_message(image)
    decode_input_window.destroy()
    
    message_window = tkinter.Toplevel()
    message_window.title("Message")
    message_window.geometry("+580+125")
    message_window.tk.call("wm", "iconphoto", message_window._w, icon_image)
    
    message_label = ttk.Label(message_window, text = "The Secret Message is", font = ("Times New Roman", 18))
    secret_message_label = ttk.Label(message_window, text = secret_message, font = ("Times New Roman", 18))

    message_label.pack(pady = 5)
    secret_message_label.pack(pady = 5)

    message_window.mainloop()

def my_info():
    
    info_window = tkinter.Toplevel()
    info_window.geometry("+240+370")
    info_window.title("Credit")
    info_window.resizable("False", "False")
    info_window.tk.call("wm", "iconphoto", info_window._w, icon_image)

    ttk.Label(info_window, text = "SUNNY KUMAR", font = ("Times New Roman", 22)).pack(padx = 10)
    ttk.Label(info_window, text = "B Tech in CSE", font = ("Times New Roman", 20)).pack(padx = 10)
    ttk.Label(info_window, text = "Chandigarh University", font = ("Times New Roman", 18)).pack(padx = 10)
    ttk.Label(info_window, text = "2021-2025", font = ("Times New Roman", 16)).pack(padx = 10)

    info_window.mainloop()

window = tkinter.Tk()

icon_image = tkinter.PhotoImage(file = "Icon.png")
select_pic = tkinter.PhotoImage(file = "Add Image.png")
style = ttk.Style()
style.configure("my.TButton", font = ("Times New Roman", 18))

window.title("Image Steganography")
window.resizable("False", "False")
window.geometry("+530+360")
window.call("wm", "iconphoto", window._w, icon_image)

my_info_button = ttk.Button(window, text = "Credit", command = my_info, style = "my.TButton")
encode_button = ttk.Button(window, command = encode_input, style = "my.TButton")
decode_button = ttk.Button(window, command = decode_input, style = "my.TButton")
exit_button = ttk.Button(window, text = "Exit", command = window.destroy, style = "my.TButton")

encode_button["text"] = "Encode  message  into  image"
decode_button["text"] = "Decode  message  from  image"

my_info_button.pack(padx = 5)
encode_button.pack(padx = 5)
decode_button.pack(padx = 5)
exit_button.pack(padx = 5)

window.mainloop()