import tkinter as tk
import boto3
from tkinter.filedialog import askopenfile
import fitz
import os
import sys
from tempfile import gettempdir
from contextlib import closing


window = tk.Tk()
window.geometry("400x400")
window.title("Convert PDF to Audiobook")
textExample = tk.Text(window, height=10)
textExample.pack()

text_to_read = ""


def read_text():
    global text_to_read
    aws_mag_con = boto3.session.Session(profile_name="PDFPolly")
    client = aws_mag_con.client(service_name="polly", region_name="eu-central-1")
    response = client.synthesize_speech(Text=text_to_read, Engine="neural", OutputFormat="mp3", VoiceId="Joanna")
    print(response)
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "speech.mp3")
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)

    else:
        print("Not find the stream!")
        sys.exit(-1)

    if sys.platform == "win32":
        os.startfile(output)


def open_pdf():
    global text_to_read
    file = askopenfile(mode="r", filetypes=[("PDF Files", "*.pdf")])
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text()
    textExample.insert("1.0", text)
    text_to_read = text


btn = tk.Button(window, height=1, width=10, text="Read", command=read_text)
btn.pack()
btn2 = tk.Button(window, height=1, width=10, text="Open PDF", command=open_pdf)
btn2.pack()

window.mainloop()