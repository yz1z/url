from tkinter import *
import tkinter as tk
import pyperclip
import requests

API_KEY = '4ca617a9857b423a110c4c7f9252857bd39e5'
BASE_URL = 'https://cutt.ly/api/api.php'

root = Tk()
root.title("Shorten URL Generator")
linkEntry = Entry(root, width=50)
linkEntry.pack()
linkEntry.insert(0, "Enter the link here")
contentEntry = Entry(root, width=50)
contentEntry.pack()
contentEntry.insert(0, "Enter the link content here")

status = {1: "the link has already been shortened",
          2: "the entered link is not a link",
          3: "the preferred link name/alias is already taken",
          4: "Invalid API key",
          5: "the link has not passed the validation. Includes invalid characters",
          6: "The link provided is from a blocked domain",
          7: "The link has been shortened"}

labelContents = [

    tk.StringVar(value=""),
    tk.StringVar(value=""),
    tk.StringVar(value=""),
    tk.StringVar(value=""),
    tk.StringVar(value=""),

]
labelList = [Label(root, textvariable=labelContents[0]),
             Label(root, textvariable=labelContents[1]),
             Label(root, textvariable=labelContents[2], font='Helvetica 18 bold underline'),
             Label(root, textvariable=labelContents[3]),
             Label(root, textvariable=labelContents[4], font='Helvetica 18 bold underline'),
             ]
for label in labelList:
    label.pack(anchor="w")


def shorten_link(full_link, link_name):
    global labelContents
    payload = {'key': API_KEY, 'short': full_link, 'name': link_name}
    request = requests.get(BASE_URL, params=payload)
    data = request.json()

    # print(data) #status 3 means title is taken

    # print('') exit
    for labelContent in labelContents:
        labelContent.set("")
    if data['url']['status'] == 7:
        title = data['url']['title']
        shortLink = data['url']['shortLink']
        fullLink = data["url"]['fullLink']

        labelContents[0].set(f"Title of the website: {title}")
        labelContents[1].set("Full Link of the website:")
        labelContents[2].set(fullLink)
        labelContents[3].set("Shorten link of the website(Copied to clipboard already):")
        labelContents[4].set(shortLink)
        pyperclip.copy(shortLink)

    else:
        labelContents[0].set(status[data['url']['status']])


def clicked():
    global linkEntry
    global contentEntry
    link = str(linkEntry.get())
    content = str(contentEntry.get())
    if not link.startswith("http"):
        link = "https://" + link
    shorten_link(link, content)


button = Button(root, text="Generate shorten link", command=clicked)
button.pack()
root.mainloop()
