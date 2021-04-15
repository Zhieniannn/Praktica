import csv
import smtplib
from time import sleep
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tkinter import *

with open("info.csv", "r", encoding="UTF-8") as file:
    reader = csv.DictReader(file, delimiter=",")
    data = [line for line in reader]

config = ConfigParser()
config.read("config.ini")

host = config.get("smtp", "server")
login = config.get("smtp", "user")
password = config.get("smtp", "password")
subject = "Hello, it`s a test"
timing = int(config.get("smtp", "timing"))

f = open("main.html", "r")
text = f.read()
print(text)

server = smtplib.SMTP(host)
server.ehlo()
server.starttls()
server.ehlo()
server.login(login, password)

for key in data:
    msg = MIMEMultipart()
    msg.attach(MIMEText(text, "html", "UTF-8"))
    msg["Subject"] = subject
    msg["From"] = login

    server.sendmail(login, key["email"], msg.as_string())
    sleep(timing)
server.quit()


def edit_cfg():
    num = txt.get()
    print(num)
    config.set("smtp", "timing", (num))
    with open("config.ini", "w") as f:
        config.write(f)


def add_user():
    a = first.get()
    b = second.get()
    with open("info.csv", "a", encoding="UTF-8") as file:
        file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
        file_writer.writerow([a, b])


# Визуал программы

window = Tk()
window.geometry("300x200")
window.title("Настройка")
window.resizable(False, False)

lbl = Label(window, text="Ввод числа задержки:", font=("Corbel"))
lbl.grid(column=0, row=0)

txt = Entry(window, width=25)
txt.grid(column=0, row=1)

btn = Button(
    window, text="Изменить", bg="white", fg="black", relief="raised", command=edit_cfg
)
btn.grid(column=1, row=1)

lbl = Label(window, text="Добавить людей в рассылку:", font=("Corbel"))
lbl.grid(column=0, row=2)

lbl = Label(window, text="Введите имя :", font=("Corbel"))
lbl.grid(column=0, row=3)

first = Entry(window, width=25)
first.grid(column=0, row=4)

lbl = Label(window, text="Введите email :", font=("Corbel"))
lbl.grid(column=0, row=5)

second = Entry(window, width=25)
second.grid(column=0, row=6)

btn = Button(
    window,
    text="Добавить",
    bg="white",
    fg="black",
    relief="groove",
    height="2",
    command=add_user,
)
btn.grid(column=1, row=5)

window.mainloop()
