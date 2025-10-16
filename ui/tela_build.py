import ttkbootstrap as ttk
from ui.components import make_scrollable_text

class TelaBuild(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        app.habilidades_text = make_scrollable_text(self, "Habilidades", 6)
        app.equip_text = make_scrollable_text(self, "Equipamento", 6)