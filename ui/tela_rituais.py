import ttkbootstrap as ttk
from ui.components import make_scrollable_text

class TelaRituais(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        painel = ttk.Panedwindow(self, orient="horizontal")
        painel.pack(fill="both", expand=True, padx=8, pady=8)

        app.rituals_text = make_scrollable_text(self, "Rituais", 12)
        app.rituals_text2 = make_scrollable_text(self, "Rituais", 12)

        painel.add(app.rituals_text.master)
        painel.add(app.rituals_text2.master)