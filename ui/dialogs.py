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
    "Péssimo": "#815100",
    "Desastre": "#8481ff",
}


# ======================================================
#   Caminho para assets (compatível com PyInstaller)
# ======================================================
def _get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


# ======================================================
#   Aplicar Ícone
# ======================================================
def set_window_icon(win):
    try:
        icon_path = os.path.join(_get_base_path(), "assets", "cthulhu.ico")
        if os.path.exists(icon_path):
            win.iconbitmap(icon_path)
    except:
        pass


# ======================================================
#   Função para carregar fonte com fallback universal
# ======================================================
def _load_font(fontsize):
    font_path = os.path.join(_get_base_path(), "assets", "MetalMania-Regular.ttf")

    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, fontsize)
        except:
            return ImageFont.load_default()
    else:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", fontsize)
        except:
            return ImageFont.load_default()


# ======================================================
#   Renderização de Número com Stroke
# ======================================================
def render_number_image(number, color, stroke=3, fontsize=72):
    font = _load_font(fontsize)

    # Corrige tamanho no Windows (aumenta ~40%)
    scale = 1.4 if sys.platform == "win32" else 1.0
    fontsize = int(fontsize * scale)
    stroke = int(stroke * scale)

    try:
        bbox = font.getbbox(str(number), stroke_width=stroke)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except:
        w, h = font.getsize(str(number))

    img = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # stroke real
    try:
        draw.text((10, 10), str(number),
                  font=font, fill=color,
                  stroke_width=stroke)
    except:
        # fallback manual
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1), (0, 1),
                   (1, -1), (1, 0), (1, 1)]
        for ox, oy in offsets:
            draw.text((10 + ox, 10 + oy), str(number),
                      font=font, fill="white")
        draw.text((10, 10), str(number),
                  font=font, fill=color)

    return ImageTk.PhotoImage(img)


# ======================================================
#   Renderização do Resultado como Imagem TRANSPARENTE
# ======================================================
def render_result_banner(text, color, fontsize=52):
    """
    Texto sem borda, fundo totalmente transparente.
    """

    font = _load_font(fontsize)

    try:
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except:
        w, h = font.getsize(text)

    padding = 20
    W = w + padding
    H = h + padding

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Texto puro, sem stroke
    draw.text(
        (padding // 2, padding // 2),
        text,
        font=font,
        fill=color
    )

    return ImageTk.PhotoImage(img)


# ======================================================
#   Popup Visual Final
# ======================================================
def show_visual_dice_popup(parent, title, dice_values, result_name, dice_type):

    win = tk.Toplevel(parent)
    win.title(title)
    win.resizable(False, False)
    set_window_icon(win)

    frame = tk.Frame(win, padx=20, pady=20, bg="#222")
    frame.pack()

    # -----------------------
    #   d100 → vermelho sangue
    # -----------------------
    if dice_type == "d100":
        val = dice_values[0] if dice_values else 0
        img = render_number_image(val, "#b30000", stroke=5, fontsize=110)
        lbl = tk.Label(frame, image=img, bg="#222")
        lbl.image = img
        lbl.pack(pady=10)

    # -----------------------
    # 2d12 → roxo + preto
    # -----------------------
    if dice_type == "2d12":
        d1 = dice_values[0] if dice_values else 0
        d2 = dice_values[1] if len(dice_values) > 1 else 0

        img1 = render_number_image(d1, "#b06cff", stroke=5, fontsize=90)
        img2 = render_number_image(d2, "#9d9d9d", stroke=5, fontsize=90)

        l1 = tk.Label(frame, image=img1, bg="#222")
        l1.image = img1
        l1.pack(side="left", padx=12)

        l2 = tk.Label(frame, image=img2, bg="#222")
        l2.image = img2
        l2.pack(side="left", padx=12)

    # -----------------------
    # Resultado como BANNER TRANSPARENTE
    # -----------------------
    normalized = result_name.strip().title()
    color = RESULT_COLORS.get(normalized, "#ffffff")

    banner = render_result_banner(normalized, color)
    lbl_banner = tk.Label(frame, image=banner, bg="#222")
    lbl_banner.image = banner
    lbl_banner.pack(pady=25)

    # -----------------------
    # Botão fechar
    # -----------------------
    tk.Button(frame, text="OK", command=win.destroy,
              font=("Metal Mania", 18)).pack(pady=10)

    # -----------------------
    # Centralização
    # -----------------------
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
