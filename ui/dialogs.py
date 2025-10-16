# ui/dialogs.py
import tkinter as tk
import sys
import os

def _get_base_path():
    """Retorna o caminho absoluto do recurso, compatível com PyInstaller"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def set_window_icon(win):
    """Aplica o ícone ao window, compatível com PyInstaller"""
    try:
        icon_path = os.path.join(_get_base_path(), "assets", "cthulhu.ico")
        icon_path = os.path.abspath(icon_path)  # garante caminho absoluto
        if os.path.exists(icon_path):
            win.iconbitmap(icon_path)
    except Exception:
        pass

def show_quick_roll_popup(parent, title, text):
    win = tk.Toplevel(parent)
    win.title(title)
    set_window_icon(win)
    win.resizable(False, False)

    frame = tk.Frame(win, padx=10, pady=10)
    frame.pack(fill="both", expand=True)

    lbl = tk.Label(frame, text=text, justify="left", wraplength=400)
    lbl.pack(padx=5, pady=5)

    btn = tk.Button(frame, text="OK", command=win.destroy)
    btn.pack(pady=(5,0))

    def centralizar():
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (w // 2)
        y = (win.winfo_screenheight() // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")
        win.lift()
        win.focus_force()
        win.grab_set()

    win.after(10, centralizar)
    win.transient(parent)
    win.wait_window()
