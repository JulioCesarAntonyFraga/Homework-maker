import urllib
import requests
from bs4 import BeautifulSoup
import re

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

from tkinter import *
from tkinter import filedialog

question_regex = r"(\s)*(\d)+(\s)*[(.)(\-)(\))]{1}(\s)*"

def UploadAction(event=None):
    filename = filedialog.askopenfilename()

    questions = open(f"{filename}", "r", encoding="utf-8").readlines()

    final_document = open("answers.txt", "w+", encoding="utf-8")

    for i in range(len(questions)):

        question = re.sub(question_regex, "", questions[i], 1)

        url = f"https://www.google.com/search?q={urllib.parse.quote(question)}"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, "html.parser")

        answer = str(soup.find(class_="BNeawe iBp4i AP7Wnd"))

        if answer == "None":

            answer = soup.find(class_="BNeawe s3v9rd AP7Wnd")

            final_document.write(f"{questions[i]}{answer.text}\n\n")

        else:

            answer = soup.find(class_="BNeawe iBp4i AP7Wnd")

            final_document.write(f"{questions[i]}{answer.text}\n\n")
    
    done = Label(text="Arquivo gerado!")
    done.pack()
    final_document.close()


root = Tk()


def make_label(parent, img):
    label = Label(parent, image=img)
    label.pack()


waring = Label(
    text="Cuidado, as respostas são retiradas do google, portanto NÃO são 100% precisas"
)
waring.pack()

frame = Frame(root, width=400, height=600, background="white")
frame.pack_propagate()
frame.pack()

img = PhotoImage(file="sample.png")
make_label(frame, img)

tuto = Label(
    text="Lembre-se, as perguntas tem que estar num documento .txt e organizadas como na imagem acima, ou o programa pode não funcionar corretamente!"
)
tuto.pack()

button = Button(root, text="Abrir arquivo", command=UploadAction)
button.pack()


root.mainloop()
