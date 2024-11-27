import json
import os

history_file = "test_upload_history.json"

def save_history(file_path, link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    history.append({"file_path": os.path.basename(file_path), "download_link": link})
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)

def test_save_history():
    test_file_path = "test_file.txt"
    test_download_link = "https://file.io/example"

    # Вызов функции для тестирования
    save_history(test_file_path, test_download_link)

    # Проверка, что история была сохранена корректно
    with open("test_upload_history.json", "r") as file:
        history = json.load(file)
        assert len(history) == 1
        assert history[0]['file_path'] == test_file_path
        assert history[0]['download_link'] == test_download_link

    # Очистка тестовых данных
    os.remove("test_upload_history.json")

# Вызов функции тестирования
test_save_history()
