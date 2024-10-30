import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

# from plagreport import main

# Функция main для проверки решений
def main(archive_filename, min_size, min_percentage, report_filename):
    # Здесь разместите основную логику для анализа архивов
    # В данный момент функция просто выводит в терминал демонстрационные сообщения
    print(f"Проверка начата с параметрами:")
    print(f"Архив с решениями: {archive_filename}")
    print(f"Минимальный процент совпадения: {min_percentage}")
    print(f"Минимальная длина решения: {min_size}")
    print(f"Отчет будет сохранен в: {report_filename}")
    print("... Выполнение анализа ...")
    print("Проверка завершена.")

# Обработка нажатия кнопки "Выполнить проверку"
def run_check():
    # Получаем параметры из интерфейса
    archive_filename = archive_path.get()
    report_filename = report_path.get()
    min_percentage = min_percentage_scale.get()
    min_size = min_size_scale.get()
    
    # Проверка заполнения полей
    if not archive_filename:
        messagebox.showwarning("Ошибка", "Выберите архив с решениями.")
        return
    if not report_filename:
        messagebox.showwarning("Ошибка", "Выберите файл для сохранения отчета.")
        return
    
    # Очищаем терминал и перенаправляем вывод
    terminal_output.delete("1.0", tk.END)
    def write_to_terminal(text):
        terminal_output.insert(tk.END, text)
        terminal_output.see(tk.END)
    import sys
    sys.stdout.write = write_to_terminal

    # Вызываем функцию main с параметрами
    main(archive_filename, min_size, min_percentage, report_filename)

# Создание главного окна
root = tk.Tk()
root.title("Проверка решений на плагиат")
root.geometry("800x600")
root.resizable(False, False) 

tk.Label(root, text="Выберите архив с решениями студентов").pack(anchor="w", padx=10, pady=5)
archive_path = tk.StringVar()
tk.Entry(root, textvariable=archive_path, width=50).pack(padx=10, pady=5)
tk.Button(root, text="Выбрать файл", command=lambda: archive_path.set(filedialog.askopenfilename())).pack(pady=5)

yandex_contest = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Архив с решениями Яндекс Контест", variable=yandex_contest).pack(anchor="w", padx=10, pady=5)

tk.Label(root, text="Минимальный процент совпадения для отчета").pack(anchor="w", padx=10, pady=5)
min_percentage_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", length=400)
min_percentage_scale.set(90)
min_percentage_scale.pack(padx=10, pady=5)

tk.Label(root, text="Минимальная длина проверяемого решения").pack(anchor="w", padx=10, pady=5)
min_size_scale = tk.Scale(root, from_=0, to=1000, orient="horizontal", length=400)
min_size_scale.set(250)
min_size_scale.pack(padx=10, pady=5)

tk.Label(root, text="Место размещения и имя файла отчета (CSV)").pack(anchor="w", padx=10, pady=5)
report_path = tk.StringVar()
tk.Entry(root, textvariable=report_path, width=50).pack(padx=10, pady=5)
tk.Button(root, text="Выбрать место сохранения", command=lambda: report_path.set(filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")]))).pack(pady=5)

tk.Button(root, text="Выполнить проверку", command=run_check).pack(pady=10)

# tk.Label(root, text="Результаты выполнения:").pack(anchor="w", padx=10, pady=5)
# terminal_output = ScrolledText(root, height=10, wrap="word", state="normal")
# terminal_output.pack(padx=10, pady=5)

# Элементы интерфейса
tk.Label(root, text="Результаты выполнения:").pack(anchor="w", padx=10, pady=5)

# Терминал для вывода
terminal_output = ScrolledText(root, height=10, wrap="word", state="normal")
terminal_output.pack(side="bottom", fill="both", padx=10, pady=(10, 5))  # Установлен отступ 10 пикселей сверху



root.mainloop()
