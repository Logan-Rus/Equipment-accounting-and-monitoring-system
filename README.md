
# model.py
import wmi
from datetime import datetime

class SystemInfoModel:
    def get_system_info(self):
        c = wmi.WMI()
        info = {}

        # Информация о системе
        system_info = []
        for os in c.Win32_OperatingSystem():
            system_info.append(("Операционная система", os.Caption))
            system_info.append(("Версия", os.Version))
            system_info.append(("Архитектура", os.OSArchitecture))
            system_info.append(("Производитель", os.Manufacturer))
            system_info.append(("Последняя загрузка", os.LastBootUpTime))
        info["Система"] = system_info

        # Информация о процессоре
        cpu_info = []
        for processor in c.Win32_Processor():
            cpu_info.append(("Процессор", processor.Name))
            cpu_info.append(("Количество ядер", processor.NumberOfCores))
            cpu_info.append(("Количество логических процессоров", processor.NumberOfLogicalProcessors))
            cpu_info.append(("Текущая частота", f"{processor.CurrentClockSpeed} МГц"))
            cpu_info.append(("Максимальная частота", f"{processor.MaxClockSpeed} МГц"))
        info["Процессор"] = cpu_info

        # Информация о памяти (RAM)
        memory_info = []
        for memory in c.Win32_PhysicalMemory():
            memory_info.append(("Объём памяти", f"{int(memory.Capacity) / (1024 ** 3):.2f} ГБ"))
            memory_info.append(("Производитель", memory.Manufacturer))
            memory_info.append(("Скорость", f"{memory.Speed} МГц"))
        info["Память"] = memory_info

        # Информация о дисках
        disk_info = []
        for disk in c.Win32_DiskDrive():
            disk_info.append(("Модель диска", disk.Model))
            disk_info.append(("Размер", f"{int(disk.Size) / (1024 ** 3):.2f} ГБ"))
            disk_info.append(("Интерфейс", disk.InterfaceType))
            disk_info.append(("ИД Диска", disk.SystemName))
        info["Диски"] = disk_info

        # Информация о видеокарте
        gpu_info = []
        for gpu in c.Win32_VideoController():
            gpu_info.append(("Видеокарта", gpu.Name))
            gpu_info.append(("Разрешение", f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}"))
            gpu_info.append(("Объём видеопамяти", f"{gpu.AdapterRAM / 1024 ** 3:.2f} ГБ"))
            if gpu.InstallDate:
                try:
                    installgpu_date = datetime.strptime(gpu.InstallDate.split(".")[0], '%Y%m%d%H%M%S')
                    gpu_info.append(("Дата установки", installgpu_date))
                except Exception as e:
                    gpu_info.append(("Ошибка при обработке даты", str(e)))
            else:
                gpu_info.append(("Дата установки", "Недоступна"))
        info["Видеокарта"] = gpu_info

        # Информация о сетевой карте
        network_info = []
        for NetworkAdapter in c.Win32_NetworkAdapter():
            network_info.append(("Сетевой адаптер", NetworkAdapter.Name))
        info["Сеть"] = network_info

        # Информация о материнской плате
        motherboard_info = []
        for MotherboardDevice in c.Win32_MotherboardDevice():
            motherboard_info.append(("Материнская плата", MotherboardDevice.Name))
            if MotherboardDevice.InstallDate:
                try:
                    install_date = datetime.strptime(MotherboardDevice.InstallDate.split(".")[0], '%Y%m%d%H%M%S')
                    motherboard_info.append(("Дата установки", install_date))
                except Exception as e:
                    motherboard_info.append(("Ошибка при обработке даты", str(e)))
            else:
                motherboard_info.append(("Дата установки", "Недоступна"))
        info["Материнская плата"] = motherboard_info

        return info


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


            # controller.py
from tkinter import messagebox
from openpyxl import Workbook

class SystemInfoController:
    def __init__(self, root):
        self.model = SystemInfoModel()
        self.view = SystemInfoView(root, self)
        self.refresh_data()

    def refresh_data(self):
        info = self.model.get_system_info()
        self.view.display_info(info)

    def export_to_excel(self):
        info = self.model.get_system_info()
        wb = Workbook()
        ws = wb.active
        ws.title = "Системная информация"

        for category, data in info.items():
            ws.append([category])  # Заголовок категории
            for item in data:
                ws.append([item[0], item[1]])  # Параметр и значение
            ws.append([])  # Пустая строка между категориями

        filename = "system_info.xlsx"
        wb.save(filename)
        messagebox.showinfo("Экспорт завершен", f"Данные успешно экспортированы в файл {filename}")


        # main.py
import tkinter as tk
from controller import SystemInfoController

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemInfoController(root)
    root.mainloop()
