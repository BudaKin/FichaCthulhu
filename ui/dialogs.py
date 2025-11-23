# ui/dialogs.py
import tkinter as tk
import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk

# ======================================================
#   Mapa de Cores do Resultado
# ======================================================
RESULT_COLORS = {
    "Extremo": "#e025b7",
    "Bom": "#fffd6d",
    "Normal": "#ffffff",
    "Ruim": "#60c075",
    "Péssimo": "#9d9d9d",
    "Desastre": "#8481ff",
}

# ======================================================
#   Base path (PyInstaller compatível)
# ======================================================
def _get_base_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


# ======================================================
#   Ícone da Janela
# ======================================================
def set_window_icon(win):
    try:
        path = os.path.join(_get_base_path(), "assets", "cthulhu.ico")
        if os.path.exists(path):
            win.iconbitmap(path)
    except:
        pass


# ======================================================
#   Carregamento da Fonte — sempre do assets
# ======================================================
def _load_font(fontsize):
    """
    Sempre carrega MetalMania-Regular.ttf da pasta assets.
    Nunca usa fontes do sistema.
    """
    font_path = os.path.join(_get_base_path(), "assets", "MetalMania-Regular.ttf")

    try:
        return ImageFont.truetype(font_path, fontsize)
    except:
        # fallback raro
        return ImageFont.load_default()


# ======================================================
#   Renderização do número do dado
# ======================================================
def render_number_image(number, color, stroke=3, fontsize=72):

    # Ajuste real de escala por plataforma
    if sys.platform.startswith("win"):
        scale = 2.4      # Windows precisa maior
    elif sys.platform.startswith("linux"):
        scale = 1.0
    else:
        scale = 1.5

    fontsize = int(fontsize * scale)
    stroke = int(stroke * scale)

    font = _load_font(fontsize)

    # Calcula bounding-box
    try:
        bbox = font.getbbox(str(number), stroke_width=stroke)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except:
        w, h = font.getsize(str(number))

    img = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Stroke correto (com borda branca)
    draw.text(
        (20, 20),
        str(number),
        font=font,
        fill=color,
        stroke_width=stroke,
        stroke_fill="white"
    )

    return ImageTk.PhotoImage(img)


# ======================================================
#   Renderização do banner do resultado
# ======================================================
def render_result_banner(text, color, fontsize=52):

    if sys.platform.startswith("win"):
        scale = 1.6
    else:
        scale = 1.0

    fontsize = int(fontsize * scale)
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
        (pad // 2, pad // 2),
        text,
        font=font,
        fill=color
    )

    return ImageTk.PhotoImage(img)


# ======================================================
#   Popup visual final
# ======================================================
def show_visual_dice_popup(parent, title, dice_values, result_name, dice_type):

    win = tk.Toplevel(parent)
    win.title(title)
    win.resizable(False, False)
    set_window_icon(win)

    frame = tk.Frame(win, padx=20, pady=20, bg="#222")
    frame.pack()

    # ========== d100 (vermelho sangue) ==========
    if dice_type == "d100":
        val = dice_values[0] if dice_values else 0
        img = render_number_image(val, "#b30000", stroke=4, fontsize=120)
        lbl = tk.Label(frame, image=img, bg="#222")
        lbl.image = img
        lbl.pack(pady=15)

    # ========== 2d12 (roxo + cinza) ==========
    if dice_type == "2d12":
        d1 = dice_values[0] if dice_values else 0
        d2 = dice_values[1] if len(dice_values) > 1 else 0

        img1 = render_number_image(d1, "#b06cff", stroke=4, fontsize=100)
        img2 = render_number_image(d2, "#9d9d9d", stroke=4, fontsize=100)

        l1 = tk.Label(frame, image=img1, bg="#222")
        l2 = tk.Label(frame, image=img2, bg="#222")
        l1.image = img1
        l2.image = img2

        l1.pack(side="left", padx=22)
        l2.pack(side="left", padx=22)

    # ========== Resultado ==========
    normalized = result_name.strip().title()
    color = RESULT_COLORS.get(normalized, "#ffffff")

    banner = render_result_banner(normalized, color)
    lb = tk.Label(frame, image=banner, bg="#222")
    lb.image = banner
    lb.pack(pady=25)

    # Botão
    tk.Button(frame, text="OK", command=win.destroy,
              font=("Metal Mania", 20)).pack(pady=10)

    # Centralização
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
