import tkinter as tk
from controller import SystemInfoController

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemInfoController(root)
    root.mainloop()