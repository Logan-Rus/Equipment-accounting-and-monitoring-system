import tkinter as tk
from tkinter import ttk, messagebox

class SystemInfoView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
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

        # Кнопка для открытия настроек удалённого компьютера
        self.remote_settings_button = tk.Button(self.root, text="Настройки удалённого компьютера", command=self.controller.open_remote_settings, font=("Arial", 10, "bold"), bg="#2196F3", fg="white")
        self.remote_settings_button.pack(pady=10)

        # Кнопка для экспорта в Excel
        self.export_button = tk.Button(self.root, text="Экспорт в Excel", command=self.controller.export_to_excel, font=("Arial", 10, "bold"), bg="dark Green", fg="white")
        self.export_button.pack(pady=10)

    def display_info(self, info, tab_name):
        # Создаем новую вкладку для отображения информации
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=tab_name)

        # Создание таблицы для вкладки
        tree = ttk.Treeview(frame, columns=("Параметр", "Значение"), show="headings", selectmode="browse")
        tree.heading("Параметр", text="Параметр")
        tree.heading("Значение", text="Значение")
        tree.column("Параметр", width=200, anchor="w")
        tree.column("Значение", width=550, anchor="w")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Добавление данных в таблицу
        for category, data in info.items():
            tree.insert("", "end", values=[category, ""])  # Заголовок категории
            for item in data:
                tree.insert("", "end", values=item)

        # Добавление прокрутки
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def open_remote_settings_window(self):
        # Создаем новое окно для ввода данных удалённого компьютера
        remote_window = tk.Toplevel(self.root)
        remote_window.title("Настройки удалённого компьютера")
        remote_window.geometry("300x300")

        # Поля для ввода данных удалённого компьютера
        remote_ip_label = tk.Label(remote_window, text="IP удалённого компьютера:")
        remote_ip_label.pack(pady=5)
        remote_ip_entry = tk.Entry(remote_window)
        remote_ip_entry.pack(pady=5)

        username_label = tk.Label(remote_window, text="Имя пользователя:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(remote_window)
        username_entry.pack(pady=5)

        password_label = tk.Label(remote_window, text="Пароль:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(remote_window, show="*")
        password_entry.pack(pady=5)

        # Кнопка для подтверждения ввода
        confirm_button = tk.Button(remote_window, text="Подтвердить", command=lambda: self.controller.display_remote_info(remote_ip_entry.get(), username_entry.get(), password_entry.get()), font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
        confirm_button.pack(pady=10)

    def show_error(self, message):
        messagebox.showerror("Ошибка", message)

    def show_info(self, message):
        messagebox.showinfo("Информация", message)