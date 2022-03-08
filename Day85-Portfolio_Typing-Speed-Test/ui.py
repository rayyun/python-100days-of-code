from tkinter import *
import csv
import random


THEME_COLOR = "#f5f3f2"
BACKGROUND = "#f5f3f2"
BG_COLOR = "#91C2AF"

FONT_NAME = "Courier"
WHITE = "#F5F5F5"
startIndex = 1.0
SHOW_WORD = 20
FONT_SIZE = 16

class TypingInterface:

    def __init__(self):
        self.words_data = []
        self.showed_words = []
        self.user_words = []
        self.display = ""
        self.word_length = 0
        self.user_input_length = 0
        # self.startIndex = 1.0
        self.previous_input = ""
        self.wpm_count = 0
        self.cpm_count = 0
        self.index = 0

        self.make_words()

        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.window.after_id = None

        word_card_img = PhotoImage(file="images/card.png")
        restart_btn_img = PhotoImage(file="images/reload.png")

        self.cpm_label = Label(text="Corrected CPM: ", font=("Arial", FONT_SIZE), bg=BACKGROUND)
        self.cpm_label.grid(row=1, column=1)
        self.cpm_value = Label(text="?", font=("Arial", FONT_SIZE), bg=WHITE)
        self.cpm_value.grid(row=1, column=2)

        self.wpm_label = Label(text="WPM: ", font=("Arial", FONT_SIZE), bg=BACKGROUND)
        self.wpm_label.grid(row=1, column=3)
        self.wpm_value = Label(text="?", font=("Arial", FONT_SIZE), bg=WHITE)
        self.wpm_value.grid(row=1, column=4)

        self.timer_label = Label(text="time left: ", font=("Arial", FONT_SIZE), bg=BACKGROUND)
        self.timer_label.grid(row=1, column=5)
        self.timer_text = Label(text="60", font=("Arial", FONT_SIZE), bg=BACKGROUND)
        self.timer_text.grid(row=1, column=6)

        # Creating UI
        self.canvas = Canvas(width=600, height=430, highlightthickness=0, bg=THEME_COLOR)

        self.canvas.create_image(300, 204, image=word_card_img)

        self.canvas.grid(row=2, column=1, columnspan=6)

        self.text = Text(self.canvas, padx=10, pady=10, height=10, width=25, highlightthickness=0, font=("Courier", 30), bg=BG_COLOR, fg="white")
        self.canvas.create_window((40, 40), window=self.text, anchor='nw', width=500, height=300)

        self.text.tag_configure('match', foreground='blue')
        self.text.tag_configure('un-match', foreground='red')


        self.sv = StringVar()
        self.window.bind("<BackSpace>", self.do_backspace)
        self.window.bind("<space>", self.user_type)
        self.sv.trace("w", lambda *args: self.callback(self.sv))
        self.entry_box = Entry(self.window, textvariable=self.sv)
        self.entry_box.focus()

        self.entry_box.grid(row=3, column=1, columnspan=6)


        self.restart_button = Button(image=restart_btn_img, bd=0, relief="flat",
                                     highlightthickness=0, bg=BACKGROUND, command=self.restart)
        self.restart_button.grid(row=4, column=1, columnspan=6, padx=20, pady=20)

        self.window.mainloop()


    def make_words(self):
        # Import words list
        with open("words.csv", encoding="utf-8-sig") as data_file:
            data = csv.reader(data_file)
            for row in data:
                self.words_data.append(''.join(row))


    def random_words(self):
        self.display = ""

        for i in range(SHOW_WORD):
            display_word = random.choice(self.words_data)
            self.showed_words.append(display_word)
            self.display += (display_word + ' ')

        print(len(self.display))
        self.text.insert(END, self.display)
        self.text.yview(END)


    def count_down(self, count):
        if count > 0:
            self.window.after_id = self.window.after(1000, self.count_down, count - 1)
        else:
            self.window.after_id = None
        if count < 10:
            count = f"0{count}"
        if count == "00":
            # self.compare()
            self.entry_box.delete(0, "end")
            self.entry_box.config(state="disabled")
            self.restart_button["state"] = "normal"
            self.window.bind("<Return>", self.start)
        self.timer_text.config(text=f"{count}")


    def start_timer(self):
        if self.window.after_id is not None:
            self.window.after_cancel(self.window.after_id)
        self.count_down(60)


    def callback(self, sv):
        # print(sv.get()[-1])

        if len(self.previous_input) < len(self.sv.get()):
            self.previous_input = self.sv.get()

            self.last_input = self.sv.get()[-1]
            self.index += 1

            print(self.last_input)
            self.check_match(self.last_input)


    def reset_data(self):
        self.showed_words = []
        self.user_words = []
        self.wpm_count = 0
        self.cpm_count = 0
        self.word_length = 0
        self.user_input_length = 0
        self.previous_input = ""
        self.index = 0
        self.entry_box.delete(0, "end")
        self.text.delete(startIndex, END)


    def restart(self):
        self.reset_data()
        self.wpm_value.config(text=self.wpm_count)
        self.cpm_value.config(text=self.cpm_count)
        self.entry_box.config(state="normal")
        self.start_timer()
        self.random_words()


    def start(self, event):
        self.reset_data()
        self.wpm_value.config(text=self.wpm_count)
        self.cpm_value.config(text=self.cpm_count)
        self.entry_box.config(state="normal")
        self.start_timer()
        self.random_words()
        self.window.unbind("<Return>")


    def check_match(self, letter):
        print(self.text.get(f"{startIndex} + {self.index - 1}c"))
        print(self.index)

        start, end = self.get_start_end(self.index)

        if letter == self.text.get(f"{startIndex} + {self.index - 1}c"):
            self.text.tag_add("match", start, end)
            if letter != " ":
                self.update_score("cpm", 1)
        else:
            self.text.tag_add("un-match", start, end)


    def get_start_end(self, index):
        start = f"{startIndex} + {index - 1}c"
        end = f"{startIndex} + {index}c"

        return start, end


    def do_backspace(self, event):
        print("do backspace!!!")

        start, end = self.get_start_end(self.index)

        self.text.tag_remove("un-match", start, end)
        self.text.tag_remove("match", start, end)

        if self.index > 0:
            self.index -= 1
            self.update_score("cpm", -1)

        self.previous_input = self.previous_input[:-1]

        print(f"backspace - {self.sv.get} / {self.index}")


    def user_type(self, event):
        self.user_words.append(self.entry_box.get().lower().strip())
        idx = len(self.user_words) - 1

        if self.showed_words[idx] == self.user_words[idx]:
            self.update_score("wpm", 1)

        self.entry_box.delete(0, "end")
        self.previous_input = ""

        if len(self.user_words) % SHOW_WORD == 0:
            self.random_words()


    def update_score(self, flag="cpm", update=1):
        if flag == "cpm":
            self.cpm_count += update
            self.cpm_value.config(text=self.cpm_count)
        elif flag == "wpm":
            self.wpm_count += update
            self.wpm_value.config(text=self.wpm_count)