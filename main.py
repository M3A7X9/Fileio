import json
import os
import requests
import pyperclip
from tkinter import filedialog, Toplevel, Listbox, Scrollbar, HORIZONTAL, VERTICAL
from tkinter import messagebox as mb
from tkinter import ttk
import tkinter as tk

history_file = "upload_history.json"


def save_history(file_path, download_link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)

    history.append({"file_path": os.path.basename(file_path), "download_link": download_link})

    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)


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
                    mb.showinfo("Ссылка скопирована", f"Ссылка успешно скопирована в буфер обмена")
                else:
                    raise ValueError("Не удалось получить ссылку для скачивания")
    except requests.RequestException as e:
        mb.showerror("Ошибка сети", f"Произошла ошибка сети: {e}")
    except ValueError as ve:
        mb.showerror("Ошибка", str(ve))
    except Exception as ex:
        mb.showerror("Ошибка", f"Произошла неизвестная ошибка: {ex}")


def show_history():
    if not os.path.exists(history_file):
        mb.showinfo("История", "История загрузок пуста")
        return

    history_window = Toplevel(window)
    history_window.title("История Загрузок")

    files_listbox = Listbox(history_window, width=50, height=20)
    files_listbox.grid(row=0, column=0, padx=(10,0), pady=10)

    links_listbox = Listbox(history_window, width=50, height=20)
    links_listbox.grid(row=0, column=1, padx=(0,10), pady=10)

    with open(history_file, "r") as f:
        history = json.load(f)
        for item in history:
            files_listbox.insert(END, item["file_path"])
            links_listbox.insert(END, item["download_link"])


window = tk.Tk()
window.title("TempFile Share")

upload_button = ttk.Button(text="Upload File", command=upload_file)
upload_button.pack()

link_entry = ttk.Entry(window)
link_entry.pack()

history_button = ttk.Button(text="Показать Историю", command=show_history)
history_button.pack()

window.mainloop()
