# Day89-Professional Portfolio Project 9 : GUI - Disappearing Text Writing App

from tkinter import *
# from PIL import Image, ImageTk

startIndex = 1.0
readyText = "Start typing..."
write_on = False
wordsInput = 0
totalInput = 0


def ready():
    global write_on

    write_on = False
    text.configure(fg="#cccccc")
    text.insert(startIndex, readyText)
    text.mark_set("insert", startIndex)

def onKeyPress(event):
    global write_on, totalInput, wordsInput, last_input_time

    index = len(readyText)
    start = f"{startIndex} +0c"
    end = f"{startIndex} + {index}c"

    if not write_on:
        text.delete(start, end)
        text.config(fg="#111111")

    write_on = True

    if event.keysym == 'Return' or event.keysym == "space":
        wordsInput += 1

    totalInput += 1

    start_timer()
    # print(totalInput, wordsInput)


def noAction(event):
    global write_on

    if not write_on:
        text.mark_set("insert", startIndex)
    else:
        text.mark_set("insert", END)


def start_timer():
    if window.after_id is not None:
        window.after_cancel(window.after_id)
    count_down(12)


def count_down(count):
    if count > 0:
        window.after_id = window.after(600, count_down, count - 1)
    else:
        window.after_id = None

    if count > 0:
        change_color(count)
    if count == 0:
        text.delete(startIndex, END)
        screen_off()
        try_again()


def change_color(count):
    font_color = ["#FF8080", "#FF6666", "#FF4D4D", "#FF3333", "#FF1919", "#FF0000", "#DD0000", "#BB0000", "#9A0000", "#790001", "#5A0004", "#3A0002", "#111111"]
    border_color = ["#DD0000", "#FF0000", "#FF1919", "#FF3333","#FF4D4D", "#FF6666", "#FF8080", "#FF9999", "#FFB3B3", "#FFCCCC", "#FFE6E6", "white", "white"]

    text.config(fg=font_color[count])
    window.config(highlightbackground=border_color[count], highlightcolor=border_color[count])


def screen_off():
    window.config(bg="black", highlightbackground="black",highlightcolor="black")
    text.config(bg="black")


def screen_on():
    window.config(bg="white", highlightbackground="white", highlightcolor="white")
    text.config(bg="white")


def try_again():
    text.config(state="disabled", height=10)


def restart():
    screen_on()
    text.config(height=20, state="normal")
    ready()


window = Tk()
window.title("The Most Dangerous Writing App")
window.geometry('800x600')
window.config(padx=20, pady=20, bg="white")
window.config(bg="white", highlightthickness=20, highlightbackground="white", highlightcolor="white")

window.resizable(False, False)
window.after_id = None

# text frame
text_frame = Frame(window, padx=10, pady=10).pack()
text = Text(text_frame, padx=10, pady=10, height=20, width=45, highlightthickness=0,
            font=("Courier", 20), bd=3, insertbackground="red", spacing1=10, spacing2=10)
text.config(cursor="none")
text.focus()
text.pack()

# button frame (restart)
button_frame = Frame(window)
button_frame.pack(side="bottom")
button = Button(button_frame, text="Try Again?", command=restart, width=20, height=3,
                activeforeground="green", activebackground="orange")
button.pack()

ready()

text.bind("<KeyPress>", onKeyPress)
text.bind("<Button-1>", noAction)
text.bind("<Button-2>", noAction)
text.bind("<Button-3>", noAction)
text.bind("<B1-Motion>", noAction)
text.bind("<MouseWheel>", noAction)

window.mainloop()
