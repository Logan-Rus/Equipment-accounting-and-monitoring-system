import wmi
from datetime import datetime
import GPUtil

class SystemInfoModel:
    @staticmethod
    def get_system_info():
        c = wmi.WMI()
        info = {}

        # Информация о системе
        system_info = []
        for os in c.Win32_OperatingSystem():
            system_info.append(("Операционная система", os.Caption))
            system_info.append(("Версия", os.Version))
            system_info.append(("Архитектура", os.OSArchitecture))
            system_info.append(("Производитель", os.Manufacturer))
            last_boot_time = os.LastBootUpTime
            last_boot_time = datetime.strptime(last_boot_time.split(".")[0], '%Y%m%d%H%M%S')
            system_info.append(("Последняя загрузка", last_boot_time.strftime('%d-%m-%Y %H:%M:%S')))
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
        total_memory = 0
        memory_speed = None
        memory_manufacturer = None

        for memory in c.Win32_PhysicalMemory():
            total_memory += int(memory.Capacity)
            if memory_speed is None:
                memory_speed = memory.Speed
            if memory_manufacturer is None:
                memory_manufacturer = memory.Manufacturer

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
        info["Диски"] = disk_info

        # Информация о видеокарте
        gpu_info = []
        gpus = GPUtil.getGPUs()  # Получаем информацию о GPU через GPUtil
        for gpu in gpus:
            gpu_info.append(("Видеокарта", gpu.name))
            gpu_info.append(("Объём видеопамяти", f"{gpu.memoryTotal} MB"))
        for gpu in c.Win32_VideoController():
            gpu_info.append(("Разрешение", f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}"))
        info["Видеокарта"] = gpu_info

        # Информация о сетевой карте
        network_info = []
        for NetworkAdapter in c.Win32_NetworkAdapter():
            network_info.append(("Сетевой адаптер", NetworkAdapter.Name))
        info["Сеть"] = network_info

        # Информация о материнской плате
        motherboard_info = []
        for board in c.Win32_BaseBoard():
            motherboard_info.append(("Производитель", board.Manufacturer))
            motherboard_info.append(("Модель", board.Product))
            motherboard_info.append(("Серийный номер", board.SerialNumber))
        info["Материнская плата"] = motherboard_info

        return info

    @staticmethod
    def get_remote_system_info(remote_ip, username, password):
        try:
            # Подключаемся к удалённому компьютеру
            remote_connection = wmi.WMI(computer=remote_ip, user=username, password=password)
            info = {}

            # Информация о системе
            system_info = []
            for os in remote_connection.Win32_OperatingSystem():
                system_info.append(("Операционная система", os.Caption))
                system_info.append(("Версия", os.Version))
                system_info.append(("Архитектура", os.OSArchitecture))
                system_info.append(("Производитель", os.Manufacturer))
                last_boot_time = os.LastBootUpTime
                last_boot_time = datetime.strptime(last_boot_time.split(".")[0], '%Y%m%d%H%M%S')
                system_info.append(("Последняя загрузка", last_boot_time.strftime('%d-%m-%Y %H:%M:%S')))
            info["Система"] = system_info

            # Информация о процессоре
            cpu_info = []
            for processor in remote_connection.Win32_Processor():
                cpu_info.append(("Процессор", processor.Name))
                cpu_info.append(("Количество ядер", processor.NumberOfCores))
                cpu_info.append(("Количество логических процессоров", processor.NumberOfLogicalProcessors))
                cpu_info.append(("Текущая частота", f"{processor.CurrentClockSpeed} МГц"))
                cpu_info.append(("Максимальная частота", f"{processor.MaxClockSpeed} МГц"))
            info["Процессор"] = cpu_info

            # Информация о памяти (RAM)
            memory_info = []

            for memory in remote_connection.Win32_PhysicalMemory():
                memory_info.append(("Объём памяти", f"{int(memory.Capacity) / (1024 ** 3):.2f} ГБ"))
                memory_info.append(("Производитель", memory.Manufacturer))
                memory_info.append(("Скорость", f"{memory.Speed} МГц"))
            info["Память"] = memory_info

            # Информация о дисках
            disk_info = []
            for disk in remote_connection.Win32_DiskDrive():
                disk_info.append(("Модель диска", disk.Model))
                disk_info.append(("Размер", f"{int(disk.Size) / (1024 ** 3):.2f} ГБ"))
                disk_info.append(("Интерфейс", disk.InterfaceType))
            info["Диски"] = disk_info

            # Информация о видеокарте
            gpu_info = []
            for gpu in remote_connection.Win32_VideoController():
                gpu_info.append(("Видеокарта", gpu.Name))
                gpu_info.append(("Разрешение", f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}"))
            info["Видеокарта"] = gpu_info

            # Информация о сетевой карте
            network_info = []
            for NetworkAdapter in remote_connection.Win32_NetworkAdapter():
                network_info.append(("Сетевой адаптер", NetworkAdapter.Name))
            info["Сеть"] = network_info

            # Информация о материнской плате
            motherboard_info = []
            for board in remote_connection.Win32_BaseBoard():
                motherboard_info.append(("Производитель", board.Manufacturer))
                motherboard_info.append(("Модель", board.Product))
                motherboard_info.append(("Серийный номер", board.SerialNumber))
            info["Материнская плата"] = motherboard_info

            return info

        except wmi.x_wmi as e:
            raise Exception(f"Ошибка подключения к удалённому компьютеру {remote_ip}: {e}")