# view.py
import tkinter as tk
from tkinter import ttk

class SystemInfoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Информация о системе")
        self.root.geometry("900x600")

        # Устанавливаем стиль
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#e0e0e0", padding=[10, 5], font=("Arial", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#ffffff")])

        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Кнопка для экспорта в Excel
        self.export_button = tk.Button(self.root, text="Экспорт в Excel", command=self.controller.export_to_excel, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
        self.export_button.pack(pady=10)

    def display_info(self, info):
        # Очистка всех вкладок перед обновлением
        for tab in self.notebook.tabs():
            for widget in self.notebook.nametowidget(tab).winfo_children():
                widget.destroy()

        # Заполнение вкладок данными
        for category, data in info.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=category)

            # Создание таблицы для каждой вкладки
            tree = ttk.Treeview(frame, columns=("Параметр", "Значение"), show="headings", selectmode="browse")
            tree.heading("Параметр", text="Параметр")
            tree.heading("Значение", text="Значение")
            tree.column("Параметр", width=200, anchor="w")
            tree.column("Значение", width=550, anchor="w")
            tree.pack(fill="both", expand=True, padx=10, pady=10)

            # Добавление данных в таблицу
            for item in data:
                tree.insert("", "end", values=item)

            # Добавление прокрутки
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")