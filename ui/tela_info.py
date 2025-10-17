import ttkbootstrap as ttk
from ui.components import make_scrollable_text

class TelaInfo(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        painel = ttk.Panedwindow(self, orient="horizontal")
        painel.pack(fill="both", expand=True, padx=8, pady=8)

        app.vant_text = make_scrollable_text(painel, "Vantagens", 6)
        app.comp_text = make_scrollable_text(painel, "Complicações", 6)
        app.back_text = make_scrollable_text(painel, "Rosto do Personagem / Backstory", 6)

        painel.add(app.vant_text.master)
        painel.add(app.comp_text.master)
        painel.add(app.back_text.master)