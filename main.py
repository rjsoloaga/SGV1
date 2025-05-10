# main.py

import tkinter as tk
from ttkbootstrap import Window
from views.login import VentanaLogin


def main():
    root = Window(themename="superhero")  # ✅ Aquí usamos el tema oscuro
    root.withdraw()  # Ocultamos hasta abrir login

    VentanaLogin(root)

    root.mainloop()


if __name__ == "__main__":
    main()