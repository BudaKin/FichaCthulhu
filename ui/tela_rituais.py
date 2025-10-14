import ttkbootstrap as ttk
from ui.components import make_scrollable_text

class TelaRituais(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        app.rituals_text = make_scrollable_text(self, "Rituais", 12)