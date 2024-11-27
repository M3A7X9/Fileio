from tkinter import *
import requests
from tkinter import filedialog as fd
from tkinter import ttk

def upload():
    filepath = fd.askopenfilename()
    if filepath:
        files = {'file': open(filepath, 'rb')}
        response = requests.post('https://file.io', files=files)
        if response.status_code == 200:
            download_link = response.json()['link']
            link_entry.insert(0, download_link)

window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry(“400x200”)

upload_button = ttk.Button(text="Загрузить файл", command=upload)
upload_button.pack()

entry = ttk.Entry()
entry.pack()

window.mainloop()
