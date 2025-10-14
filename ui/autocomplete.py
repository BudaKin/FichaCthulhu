# ui/autocomplete.py
import tkinter as tk
import ttkbootstrap as ttk

class AutocompleteEntry(ttk.Entry):
    def __init__(self, parent, autocomplete_list=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        if autocomplete_list is None:
            autocomplete_list = []
        self.autocomplete_list = sorted(autocomplete_list, key=str.lower)
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        try:
            self.var.trace_add("write", lambda *a: self.changed())
        except Exception:
            self.var.trace("w", self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Down>", self.move_down)
        self.bind("<Up>", self.move_up)
        self.listbox_up = False
        self.listbox = None

    def update_list(self, new_list):
        self.autocomplete_list = sorted(new_list, key=str.lower)
        if self.listbox_up:
            self.changed()

    def changed(self, *args):
        txt = self.var.get()
        if txt == "":
            self.close_listbox()
            return
        words = self.matches(txt)
        if words:
            if not self.listbox_up:
                self.open_listbox()
            self.listbox.delete(0, "end")
            for w in words:
                self.listbox.insert("end", w)
        else:
            self.close_listbox()

    def matches(self, text):
        text_l = text.lower()
        starts = [w for w in self.autocomplete_list if w.lower().startswith(text_l)]
        if starts:
            return starts[:50]
        contains = [w for w in self.autocomplete_list if text_l in w.lower()]
        return contains[:50]

    def selection(self, event):
        if self.listbox_up and self.listbox.curselection():
            self.var.set(self.listbox.get("active"))
            self.close_listbox()
            self.icursor("end")
        return "break"

    def move_up(self, event):
        if not self.listbox_up:
            return "break"
        cur = self.listbox.curselection()
        if not cur:
            idx = 0
        else:
            idx = cur[0]
        if idx > 0:
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(idx - 1)
            self.listbox.activate(idx - 1)
        return "break"

    def move_down(self, event):
        if not self.listbox_up:
            return "break"
        cur = self.listbox.curselection()
        if not cur:
            idx = -1
        else:
            idx = cur[0]
        if idx < self.listbox.size() - 1:
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(idx + 1)
            self.listbox.activate(idx + 1)
        return "break"

    def open_listbox(self):
        if self.listbox_up:
            return
        self.listbox = tk.Listbox(self.parent, height=6)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.listbox.bind("<Right>", self.selection)
        try:
            x = self.winfo_x()
            y = self.winfo_y() + self.winfo_height()
            w = self.winfo_width()
            self.listbox.place(x=x, y=y, width=w)
        except Exception:
            self.listbox.pack()
        self.listbox_up = True

    def close_listbox(self):
        if self.listbox_up and self.listbox:
            try:
                self.listbox.destroy()
            except Exception:
                pass
        self.listbox_up = False
        self.listbox = None

    def on_listbox_select(self, event):
        if self.listbox_up:
            sel = self.listbox.curselection()
            if sel:
                self.var.set(self.listbox.get(sel[0]))
            self.close_listbox()
            self.icursor("end")