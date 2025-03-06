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