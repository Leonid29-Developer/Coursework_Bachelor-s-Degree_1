import tkinter as tk
from tkinter import ttk, filedialog


class CSV_App:
    filename = ""

    def __init__ (self, root):
        self.root = root
        self.root.title("CSV Manager - управление контентом")
        self.root.geometry("400x400")

        main_frame = tk.Frame(self.root)
        main_frame.place(relwidth = 1, relheight = 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = CSV_App(root)
    root.mainloop()
