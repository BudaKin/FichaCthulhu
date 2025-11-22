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
        icon_path = os.path.abspath(icon_path)
        if os.path.exists(icon_path):
            win.iconbitmap(icon_path)
    except Exception:
        pass


# =======================================================
#   NOVO POPUP VISUAL PARA ROLAGEM
# =======================================================
def show_visual_dice_popup(parent, title, dice_values, result_name, dice_type):
    """
    dice_values:
        d100 → [valor]
        2d12 → [d1, d2]
    result_name:
        "Bom", "Ruim", "Extremo", etc.
    dice_type:
        "d100" ou "2d12"
    """
    win = tk.Toplevel(parent)
    win.title(title)
    set_window_icon(win)
    win.resizable(False, False)

    frame = tk.Frame(win, padx=20, pady=20, bg="#222")
    frame.pack()

    # ================================
    #   DADO d100 (1 número roxo)
    # ================================
    if dice_type == "d100":
        val = dice_values[0]
        lbl = tk.Label(
            frame,
            text=str(val),
            fg="#b06cff",      # Roxo
            bg="#222",
            font=("Metal Mania", 48),
            bd=3,
            relief="solid"
        )
        lbl.pack(pady=10)

    # ================================
    #   DADOS 2d12 (roxo + preto)
    # ================================
    else:
        d1, d2 = dice_values

        lbl1 = tk.Label(
            frame,
            text=str(d1),
            fg="#b06cff",   # Roxo
            bg="#222",
            font=("Metal Mania", 42),
            bd=3,
            relief="solid"
        )
        lbl1.pack(side="left", padx=12)

        lbl2 = tk.Label(
            frame,
            text=str(d2),
            fg="black",
            bg="#222",
            font=("Metal Mania", 42),
            bd=3,
            relief="solid"
        )
        lbl2.pack(side="left", padx=12)

    # ================================
    #   RESULTADO (texto)
    # ================================
    lblr = tk.Label(
        frame,
        text=result_name,
        fg="white",
        bg="#222",
        font=("Metal Mania", 26)
    )
    lblr.pack(pady=(20, 5))

    # Botão ok
    tk.Button(
        frame,
        text="OK",
        command=win.destroy,
        font=("Metal Mania", 16)
    ).pack(pady=10)

    # Centralizar janela
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
