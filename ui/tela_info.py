import ttkbootstrap as ttk
from ui.components import make_scrollable_text

class TelaInfo(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        app.habilidades_text = make_scrollable_text(self, "Habilidades", 6)
        app.equip_text = make_scrollable_text(self, "Equipamento", 6)
        app.vant_text = make_scrollable_text(self, "Vantagens / Complicações", 6)
        app.back_text = make_scrollable_text(self, "Rosto do Personagem / Backstory", 10)