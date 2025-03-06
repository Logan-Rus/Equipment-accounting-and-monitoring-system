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