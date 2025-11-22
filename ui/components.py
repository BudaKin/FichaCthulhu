# ui/components.py
import tkinter as tk
import ttkbootstrap as tb

def make_scrollable_text(parent, label, height):
    box = tb.Labelframe(parent, text=label)
    text = tk.Text(box, height=height, wrap="word")
    scroll = tb.Scrollbar(box, command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    text.pack(side="left", fill="both", expand=True, padx=4, pady=4)
    scroll.pack(side="right", fill="y")
    return text