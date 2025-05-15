import tkinter as tk
from Controller import SystemInfoController

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemInfoController(root)
    root.mainloop()
