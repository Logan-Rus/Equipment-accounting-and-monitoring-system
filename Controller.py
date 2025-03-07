from model import SystemInfoModel
from view import SystemInfoView
from openpyxl import Workbook

class SystemInfoController:
    def __init__(self, root):
        self.model = SystemInfoModel()
        self.view = SystemInfoView(root, self)

        # Автоматическое заполнение таблиц при запуске (локальная информация)
        local_info = self.model.get_system_info()
        self.view.display_info(local_info, tab_name="Локальный компьютер")

    def open_remote_settings(self):
        self.view.open_remote_settings_window()

    def display_remote_info(self, remote_ip, username, password):
        try:
            remote_info = self.model.get_remote_system_info(remote_ip, username, password)
            self.view.display_info(remote_info, tab_name=f"Удалённый: {remote_ip}")
        except Exception as e:
            self.view.show_error(str(e))

    def export_to_excel(self):
        # Создание Excel-файла
        wb = Workbook()
        ws_local = wb.active
        ws_local.title = "Локальный компьютер"

        # Получение данных о локальном компьютере
        local_info = self.model.get_system_info()
        self.write_info_to_sheet(ws_local, local_info)

        # Экспорт данных о удалённых компьютерах
        for tab in self.view.notebook.tabs():
            tab_name = self.view.notebook.tab(tab, "text")
            if tab_name.startswith("Удалённый:"):
                remote_ip = tab_name.replace("Удалённый:", "").strip()

                # Заменяем недопустимые символы в названии листа
                sheet_title = f"Удалённый {remote_ip}"
                sheet_title = sheet_title.replace(":", "-")  # Заменяем : на -

                ws_remote = wb.create_sheet(title=sheet_title)

                # Получение данных из Treeview
                frame = self.view.notebook.nametowidget(tab)
                tree = frame.winfo_children()[0]  # Получаем Treeview из вкладки
                remote_info = {}

                # Собираем данные из Treeview
                for child in tree.get_children():
                    values = tree.item(child, "values")
                    if len(values) == 2:
                        if values[1] == "":  # Это заголовок категории
                            current_category = values[0]
                            remote_info[current_category] = []
                        else:
                            remote_info[current_category].append(values)

                # Запись данных на лист
                self.write_info_to_sheet(ws_remote, remote_info)

        # Сохранение файла
        filename = "system_info.xlsx"
        wb.save(filename)
        self.view.show_info(f"Данные успешно экспортированы в файл {filename}")

    @staticmethod
    def write_info_to_sheet(ws, info):
        # Запись данных на лист Excel
        for category, data in info.items():
            ws.append([category])  # Заголовок категории
            for item in data:
                ws.append([item[0], item[1]])  # Параметр и значение
            ws.append([])  # Пустая строка между категориями