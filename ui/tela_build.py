import ttkbootstrap as ttk
from ui.components import make_scrollable_text

class TelaBuild(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        painel = ttk.Panedwindow(self, orient="horizontal")
        painel.pack(fill="both", expand=True, padx=8, pady=8)

        app.habilidades_text = make_scrollable_text(self, "Habilidades", 6)
        app.equip_text = make_scrollable_text(self, "Equipamento", 6)

        painel.add(app.habilidades_text.master)
        painel.add(app.equip_text.master)