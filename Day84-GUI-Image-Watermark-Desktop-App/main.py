from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

CLEAR = FALSE
IMAGE_CLEAR = FALSE

def copyright_text_apply(input_image_path, text):
    output_image_path = input_image_path.replace('in', 'out')

    photo = Image.open(input_image_path)

    # store image width and height
    w, h = photo.size

    # make the image editable
    drawing = ImageDraw.Draw(photo)
    font = ImageFont.truetype("Arial.ttf", int(float(w) / 10))

    # get text width and height
    text = "© " + text
    text_w, text_h = drawing.textsize(text, font)

    pos = (w - text_w) // 2, (h - text_h) // 2      # center
    # pos = w - text_w, (h - text_h) - 50       # left-bottom

    c_text = Image.new('RGB', (text_w, (text_h)), color='#000000')
    drawing = ImageDraw.Draw(c_text)

    drawing.text((0,0), text, fill='#ffffff', font=font)
    c_text.putalpha(100)

    photo.paste(c_text, pos, c_text)
    photo.save(output_image_path)

    show_result(output_image_path)


def copyright_logo_apply(input_image_path, logo_image_path):
    output_image_path = input_image_path.replace('in', 'out')

    photo = Image.open(input_image_path).convert('RGBA')
    wm_logo = Image.open(logo_image_path).convert('RGBA')

    # store image width and height
    w, h = photo.size
    lw, lh = wm_logo.size

    if lw * 2 <= w and lh * 2 <= h:
        new_w, new_h = int(lw * 2), int(lh * 2)
    elif lw * 1.5 <= w and lh * 1.5 <= h:
        new_w, new_h = int(lw * 1.5), int(lh * 1.5)
    else:
        new_w, new_h = lw, lh

    # print(f"new_w = {new_w}, new_h = {new_h}")

    width = (w - new_w) // 2
    height = (h - new_h) // 2

    wm_logo = wm_logo.resize((new_w, new_h), Image.ANTIALIAS)

    photo.paste(wm_logo, (width, height), wm_logo)

    photo = photo.convert('RGB')
    photo.save(output_image_path)

    show_result(output_image_path)


def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def optionTextLogo(x, selected_watermark, clear=False):
    global CLEAR
    CLEAR = True

    if clear:
        clearFrame(menu_frame)

    if selected_watermark == 'text':
        logo_label = Label(menu_frame, text="Watermark text :")
        logo_label.grid(row=2, column=2, sticky='nw', padx=30, pady=10)

        logo_entry = Entry(menu_frame, width=20)
        logo_entry.grid(row=2, column=3, sticky='nw', padx=10, pady=10)

        submit_button = Button(menu_frame, text="Generate Watermark",
                               command=lambda: copyright_text_apply(x, logo_entry.get()))
        submit_button.grid(row=2, column=4, columnspan=3, sticky='nw', padx=20, pady=10)

    elif selected_watermark == 'logo':
        selected_logo = StringVar()

        logo_types = (('Copyright', 'images/copyright.png'),
                      ('Sample', 'images/sample.png'),
                      ('Draft', 'images/draft.png'),
                      ('Example', 'images/example.png'))
        logo_label = Label(menu_frame, text="Select a Watermark logo :")
        logo_label.grid(row=2, column=2, columnspan=5, sticky='nw', padx=30, pady=30)

        col = 2

        for logo_key, logo_value in logo_types:
            logo_entry = Radiobutton(menu_frame, text=logo_key, value=logo_value, variable=selected_logo)
            logo_entry.grid(row=3, column=col, sticky='nw', padx=30, pady=30)
            col += 1

        submit_button = Button(menu_frame, text="Generate Watermark",
                               command=lambda: copyright_logo_apply(x, selected_logo.get()))
        submit_button.grid(row=4, column=2, columnspan=4, padx=30, pady=30)


def new_size(w, h):
    MAX_SIZE = 600

    if w <= MAX_SIZE and h <= MAX_SIZE:
        new_w, new_h = w, h
    elif w > h:
        new_w = MAX_SIZE
        new_h = int((h * MAX_SIZE) / w)
    elif w == h:
        new_w, new_h = MAX_SIZE, MAX_SIZE
    else:
        new_w = int((w * MAX_SIZE) / h)
        new_h = MAX_SIZE

    # print(f"new_w = {new_w}, new_h = {new_h}")
    return new_w, new_h


# Create a window
def open_img(clear=False):
    global IMAGE_CLEAR
    IMAGE_CLEAR = True

    if clear:
        clearFrame(image_frame)
        clearFrame(menu_frame)

    # Select the Image name from a folder
    x = openfilename()

    # opens the image
    img = Image.open(x)
    w, h = img.size

    new_w, new_h = new_size(w, h)

    # resize the image and apply a high-quality down sampling filter
    img = img.resize((new_w, new_h), Image.ANTIALIAS)

    # PhotoImage class is used to add image to widgets, icons etc.
    img = ImageTk.PhotoImage(img)

    panel = Label(image_frame, image=img)

    # set the image as img
    panel.image = img
    panel.grid(row=1, column=0)

    selected_watermark = StringVar()

    wm_types = (('Watermark Text', 'text'), ('Watermark Logo', 'logo'))
    wm_type_label = Label(text="Select a Watermark type :")
    wm_type_label.grid(row=0, column=1, columnspan=5, padx=30, sticky='w')

    col = 1

    for wm_key, wm_value in wm_types:
        wm_radiobutton = Radiobutton(text=wm_key, value=wm_value, variable=selected_watermark)
        wm_radiobutton.grid(row=1, column=col, padx=30, pady=10)

        col += 1

    wm_type_button = Button(text='Confirm', command=lambda:optionTextLogo(x, selected_watermark.get(), CLEAR))
    wm_type_button.grid(row=1, column=col, padx=30, pady=10)


def show_result(output_image_path):
    # Select the Image name from a folder
    img = Image.open(output_image_path)
    w, h = img.size

    new_w, new_h = new_size(w, h)

    # resize the image and apply a high-quality down sampling filter
    img = img.resize((new_w, new_h), Image.ANTIALIAS)

    # PhotoImage class is used to add image to widgets, icons etc.
    img = ImageTk.PhotoImage(img)

    panel = Label(image_frame, image=img)

    # set the image as img
    panel.image = img
    panel.grid(row=1, column=0)


def openfilename():
    # open file dialog box to select image
    # the dialogue box has a title 'Open'
    filename = filedialog.askopenfilename(title='open')
    return filename


window = Tk()
window.title("Watermark Creator")
window.geometry('1200x700')
window.config(padx=20, pady=20)
window.resizable(False, False)

image_frame = Frame(window)
image_frame.grid(row=2, column=0)

menu_frame = Frame(window)
menu_frame.grid(row=2, column=1, columnspan=5)

open_button = Button(text='Open Image', highlightthickness=1, command=lambda:open_img(IMAGE_CLEAR))
open_button.grid(row=0, column=0)

window.mainloop()







# def copyright_logo_apply(input_image_path, logo_image_path):
#     output_image_path = input_image_path.replace('in', 'out')
#
#     photo = Image.open(input_image_path).convert('RGBA')
#     wm_logo = Image.open(logo_image_path).convert('RGBA')
#
#     # store image width and height
#     w, h = photo.size
#     lw, lh = wm_logo.size
#
#     width = (w - lw) // 2
#     height = (h - lh) // 2
#
#     # final_img = Image.new('RGBA', (w, h))
#     # final_img = Image.alpha_composite(final_img, photo)
#     # final_img = Image.alpha_composite(final_img, wm_logo)
#
#     photo.paste(wm_logo, (width, height), wm_logo)
#     # blended = Image.blend(photo, wm_logo, alpha=0.5)
#
#     # photo = blended.convert('RGB')
#     # final_img = final_img.convert('RGB')
#     # final_img.save(output_image_path)
#
#     photo = photo.convert('RGB')
#     photo.save(output_image_path)
#
#     show_result(output_image_path)
