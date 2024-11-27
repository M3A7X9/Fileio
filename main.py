import json
import os
import requests
import pyperclip
from tkinter import filedialog, messagebox, Toplevel, Listbox, Scrollbar, HORIZONTAL, VERTICAL
from tkinter import ttk
import tkinter as tk

history_file = "upload_history.json"


def save_history(file_path, download_link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            history = json.load(file)

    history.append({"file_path": os.path.basename(file_path), "download_link": download_link})

    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)


def upload_file():
    try:
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()
                download_link = response.json().get('link')
                if download_link:
                    link_entry.delete(0, tk.END)
                    link_entry.insert(0, download_link)
                    pyperclip.copy(download_link)
                    save_history(filepath, download_link)
                    messagebox.showinfo("Ссылка скопирована", "Ссылка успешно скопирована в буфер обмена")
                else:
                    raise ValueError("Не удалось получить ссылку для скачивания")
    except requests.RequestException as e:
        messagebox.showerror("Ошибка сети", f"Произошла ошибка сети: {e}")
    except ValueError as ve:
        messagebox.showerror("Ошибка", str(ve))
    except Exception as ex:
        messagebox.showerror("Ошибка", f"Произошла неизвестная ошибка: {ex}")


app = tk.Tk()
app.title("TempFile Share")

upload_button = ttk.Button(app, text="Upload File", command=upload_file)
upload_button.pack()

link_entry = ttk.Entry(app)
link_entry.pack()

app.mainloop()
