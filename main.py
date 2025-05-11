# main.py

import tkinter as tk
from ttkbootstrap import Window
from views.login import VentanaLogin


def main():
    root = Window(themename="superhero")
    root.withdraw()

    VentanaLogin(root)

    root.mainloop()


if __name__ == "__main__":
    main()