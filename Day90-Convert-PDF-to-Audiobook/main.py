from tkinter import *
from tkinter import filedialog
import pdftotext
from google.cloud import texttospeech
import os
from playsound import playsound
import pygame

startIndex = 1.0

def textFromPDF(filename):
    global text, play_button
    text.delete(startIndex, END)

    f = open(filename, 'rb')
    audio_file_name = f"audio/{os.path.basename(f.name).replace('.pdf', '')}.mp3"
    print(audio_file_name)

    pdf = pdftotext.PDF(f)

    f.close()

    # Iterate over all the pages
    for idx, page in enumerate(pdf):
        print(idx)
        text.insert(END, page)
        text.yview(END)
        google_text_to_speech(idx, page, audio_file_name)

    play_button.config(state="active", command=lambda:play_audio_file(audio_file_name))


def google_text_to_speech(idx, page, audio_file_name):

    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "path-of-your-credendtial-jason-file"

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=page)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-GB-Standard-A", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    if idx == 0:
        option = "wb"
    else:
        option = "ab"

    with open(audio_file_name, option) as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file {audio_file_name}')


# problem : while playing audio files, mouse doesn't move.
# def play_audio_file(filename):
#     playsound(filename)



def play_audio_file(filename):
    pygame.mixer.init()  # initialise the pygame
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(loops=0)


def openfile():
    global play_button

    filename = filedialog.askopenfilename(title='open')
    print(filename)
    play_button.config(state='disabled')

    textFromPDF(filename)

    return filename


window = Tk()
window.title("Covert PDF to Audio Book")
window.geometry('1200x700')
window.config(padx=20, pady=20)
window.resizable(False, False)

open_button = Button(text='Open File', highlightthickness=1, command=openfile, width=20, height=2,
                activeforeground="green", activebackground="orange")
open_button.pack()

text = Text(window, padx=20, pady=20, height=15, width=80, highlightthickness=0, font=("Courier", 18),
                 bg="#F8EDE3", fg="#191919", spacing1=10)
text.pack()

play_button = Button(text='Play', state="disabled", highlightthickness=1, width=20, height=2,
                activeforeground="green", activebackground="orange")
play_button.pack()


window.mainloop()