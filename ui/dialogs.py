import tkinter as tk
import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk

# ======================================================
#   Mapa de Cores do Resultado
# ======================================================
RESULT_COLORS = {
    "Extremo": "#e025b7",
    "Bom":     "#fffd6d",
    "Normal":  "#ffffff",
    "Ruim":    "#60c075",
    "Péssimo": "#815100",
    "Desastre":"#8481ff",
}


# ======================================================
#   Base path (PyInstaller compatível)
# ======================================================
def _get_base_path():
    if getattr(sys, "frozen", False):  # rodando como exe
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


# ======================================================
#   Ícone
# ======================================================
def set_window_icon(win):
    try:
        path = os.path.join(_get_base_path(), "assets", "cthulhu.ico")
        if os.path.exists(path):
            win.iconbitmap(path)
    except:
        pass


# ======================================================
#   Fonte — SEMPRE carregada do assets
# ======================================================
def _load_font(fontsize):
    """
    Sempre usa MetalMania-Regular.ttf da pasta /assets no diretório raiz.
    """
    base = _get_base_path()

    # sobe um nível se estiver em ui/
    # quando rodando via PyInstaller, o _MEIPASS já contém assets
    if "ui" in os.path.basename(base).lower():
        base = os.path.dirname(base)  # sobe 1 nível

    font_path = os.path.join(base, "assets", "MetalMania-Regular.ttf")

    try:
        return ImageFont.truetype(font_path, fontsize)
    except Exception as e:
        print("Erro carregando fonte:", e)
        return ImageFont.load_default()

# ======================================================
#   Renderizar NÚMERO DO DADO (com contorno branco)
# ======================================================
def render_number_image(number, color, stroke=3, fontsize=72):

    fontsize = int(fontsize)
    stroke   = int(stroke)

    font = _load_font(fontsize)

    # Tamanho do texto
    try:
        bbox = font.getbbox(str(number), stroke_width=stroke)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except:
        w, h = font.getsize(str(number))

    img = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.text(
        (20, 20),
        str(number),
        font=font,
        fill=color
    )

    return ImageTk.PhotoImage(img)


# ======================================================
#   Renderizar RESULTADO (sem stroke, sem fundo)
# ======================================================
def render_result_banner(text, color, fontsize=72):
    font = _load_font(fontsize)

    try:
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except:
        w, h = font.getsize(text)

    pad = 20
    img = Image.new("RGBA", (w + pad, h + pad), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.text(
        (pad//2, pad//2),
        text,
        font=font,
        fill=color
    )

    return ImageTk.PhotoImage(img)


# ======================================================
#   POPUP VISUAL
# ======================================================
def show_visual_dice_popup(parent, title, dice_values, result_name, dice_type):

    win = tk.Toplevel(parent)
    win.title(title)
    win.resizable(False, False)
    set_window_icon(win)

    frame = tk.Frame(win, padx=20, pady=20, bg="#222")
    frame.pack()

    # ---------- D100 ----------
    if dice_type == "d100":
        value = dice_values[0] if dice_values else 0
        img = render_number_image(value, "#b30000", stroke=5, fontsize=120)
        lbl = tk.Label(frame, image=img, bg="#222")
        lbl.image = img
        lbl.pack(pady=15)

    # ---------- 2D12 ----------
    if dice_type == "2d12":
        d1 = dice_values[0] if dice_values else 0
        d2 = dice_values[1] if len(dice_values) > 1 else 0

        img1 = render_number_image(d1, "#b06cff", stroke=5, fontsize=100)
        img2 = render_number_image(d2, "#9d9d9d", stroke=5, fontsize=100)

        l1 = tk.Label(frame, image=img1, bg="#222")
        l2 = tk.Label(frame, image=img2, bg="#222")

        l1.image = img1
        l2.image = img2

        l1.pack(side="left", padx=20)
        l2.pack(side="left", padx=20)

    # ---------- RESULTADO ----------
    norm = result_name.strip().title()
    color = RESULT_COLORS.get(norm, "#ffffff")

    banner = render_result_banner(norm, color)
    lb = tk.Label(frame, image=banner, bg="#222")
    lb.image = banner
    lb.pack(pady=25)

    # ---------- OK ----------
    tk.Button(
        frame,
        text="OK",
        font=("Metal Mania", 20),
        command=win.destroy
    ).pack(pady=10)

    # ---------- Centralizar ----------
    def center():
        win.update_idletasks()
        w, h = win.winfo_width(), win.winfo_height()

        x = win.winfo_screenwidth() // 2 - w // 2
        y = win.winfo_screenheight() // 2 - h // 2

        win.geometry(f"{w}x{h}+{x}+{y}")
        win.focus_force()
        win.grab_set()

    win.after(10, center)
    win.transient(parent)
    win.wait_window()
