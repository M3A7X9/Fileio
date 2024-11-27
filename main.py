from tkinter import *
import requests
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk

def upload():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()  # Проверка на ошибки HTTP
                download_link = response.json().get('link')
                if download_link:
                    entry.delete(0, END)
                    entry.insert(0, download_link)
                else:
                    raise ValueError("Не удалось получить ссылку для скачивания")
    except ValueError as ve:
        mb.showerror("Ошибка", f"Произошла ошибка: {ve}")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")


window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry("360x100")

upload_button = ttk.Button(text="Загрузить файл", command=upload)
upload_button.pack()

entry = ttk.Entry()
entry.pack()

window.mainloop()
