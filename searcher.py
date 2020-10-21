import re
import urllib
import lxml
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from tkinter import *
from tkinter import filedialog

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

session = HTMLSession()

question_number_regex = r"(\s)*(\d)+(\s)*[(.)(\-)(\))]{1}(\s)*"


def UploadAction(event=None):
    filename = filedialog.askopenfilename()

    questions = open(f"{filename}", "r", encoding="utf-8").readlines()

    output = {"question": [], "answer": []}

    for question in questions:

        question_without_number = re.sub(
            question_number_regex, "", question.replace("\n", ""), 1
        )

        output["question"].append(question_without_number)

        url = f"https://www.google.com/search?q={urllib.parse.quote(question_without_number)}"
        req = session.get(url, headers=headers)

        # For Javascript render
        # req.html.render()

        soup = BeautifulSoup(req.html.html, "lxml")

        answer = soup.find(class_="QIclbb XpoqFe")

        if answer is None:
            answer = soup.find("span", class_="aCOpRe").span

        output["answer"].append(answer.text)

    df = pd.DataFrame(output)

    df.to_json("answers.json", orient="index", indent=2, force_ascii=False)

    done = Label(text="Arquivo gerado!")
    done.pack()


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
    text="Lembre-se, as perguntas tem que estar num documento .txt separadas por linha. Como no exemplo acima."
)
tuto.pack()

button = Button(root, text="Abrir arquivo", command=UploadAction)
button.pack()

if __name__ == "__main__":
    root.mainloop()
