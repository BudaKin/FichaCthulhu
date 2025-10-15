import tkinter as tk
import ttkbootstrap as ttk
from core.data import SKILLS, ATTRS

class TelaFicha(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Cabeçalho
        header = ttk.Labelframe(self, text="Identificação")
        header.pack(fill="x", padx=8, pady=6)
        labels = [
            ("Nome", "nome"), ("Arquétipo", "arquetipo"), ("NEX", "nex"),
            ("Ocupação", "ocupacao"), ("Dinheiro", "dinheiro"), ("Deslocamento", "deslocamento"),
            ("Estilo de Luta", "estilo_luta"), ("Soco", "soco"), ("Bônus de Dano", "bonus_dano")
        ]
        for i, (lab, key) in enumerate(labels):
            r = i // 3
            c = (i % 3) * 2
            ttk.Label(header, text=lab).grid(row=r, column=c, sticky="w", padx=4, pady=2)
            v = app.header_vars.setdefault(key, tk.StringVar())
            ttk.Entry(header, textvariable=v, width=22).grid(row=r, column=c+1, sticky="w", padx=4, pady=2)

        # Atributos
        attr_frame = ttk.Labelframe(self, text="Atributos")
        attr_frame.pack(fill="x", padx=8, pady=6)
        for i, name in enumerate(ATTRS):
            lbl = ttk.Label(attr_frame, text=name)
            lbl.grid(row=i//6, column=(i%6)*2, sticky="w", padx=4, pady=2)
            lbl.bind("<Double-Button-1>", lambda ev, n=name: app._perform_roll(n, "2d12"))
            v = app.attr_vars.setdefault(name, tk.StringVar())
            ttk.Entry(attr_frame, textvariable=v, width=8).grid(row=i//6, column=(i%6)*2+1, sticky="w", padx=4, pady=2)

        # Status
        stats_frame = ttk.Labelframe(self, text="Status")
        stats_frame.pack(fill="x", padx=8, pady=6)
        ttk.Label(stats_frame, text="Vida").grid(row=0, column=0, padx=4, sticky="w")
        ttk.Entry(stats_frame, textvariable=app.vida_var, width=10).grid(row=0, column=1, padx=4)
        ttk.Label(stats_frame, text="Sanidade").grid(row=0, column=2, padx=4, sticky="w")
        ttk.Entry(stats_frame, textvariable=app.san_var, width=10).grid(row=0, column=3, padx=4)
        ttk.Label(stats_frame, text="Ocultismo").grid(row=0, column=4, padx=4, sticky="w")
        ttk.Entry(stats_frame, textvariable=app.ocult_var, width=10).grid(row=0, column=5, padx=4)

        # Outras Perícias
        lang_frame = ttk.Labelframe(self, text="Outras Perícias")
        lang_frame.pack(fill="x", padx=8, pady=6)
        app.lang_container = ttk.Frame(lang_frame)
        app.lang_container.pack(fill="x", padx=4, pady=4)
        ttk.Button(lang_frame, text="+ Adicionar Perícia", bootstyle="info",
                   command=lambda: self.add_language(app)).pack(pady=2)

        # Perícias
        skills_frame = ttk.Labelframe(self, text="Perícias (valores)")
        skills_frame.pack(fill="both", expand=True, padx=8, pady=6)
        canvas = tk.Canvas(skills_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(skills_frame, orient="vertical", command=canvas.yview, bootstyle="round")
        scrollable = ttk.Frame(canvas)
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, s in enumerate(SKILLS):
            row = i // 3
            col = (i % 3) * 2
            lbl = ttk.Label(scrollable, text=s)
            lbl.grid(row=row, column=col, sticky="w", padx=4, pady=2)
            lbl.bind("<Double-Button-1>", lambda ev, n=s: app._perform_roll(n, "2d12"))
            v = app.skill_vars.setdefault(s, tk.StringVar())
            ttk.Entry(scrollable, textvariable=v, width=8).grid(row=row, column=col+1, padx=4, pady=2)

    # ===== Adicionar novas perícias (idiomas) com Quick Roll =====
    def add_language(self, app):
        linha = ttk.Frame(app.lang_container)
        linha.pack(fill="x", padx=4, pady=2)

        nome_var = tk.StringVar()
        val_var = tk.StringVar()
        nome_entry = ttk.Entry(linha, textvariable=nome_var, width=20)
        nome_entry.pack(side="left", padx=4)
        val_entry = ttk.Entry(linha, textvariable=val_var, width=8)
        val_entry.pack(side="left", padx=4)

        # Botão para remover a perícia
        remove_btn = ttk.Button(linha, text="✖", bootstyle="danger", width=2,
                                command=lambda: (linha.destroy(), app.extra_lang_vars.remove((nome_var, val_var, linha))))
        remove_btn.pack(side="left", padx=4)

        # Quick Roll: usa apenas o valor definido
        def quick_roll(ev):
            nome = nome_var.get()
            app._perform_roll(nome, "2d12")

        nome_entry.bind("<Double-Button-1>", quick_roll)
        val_entry.bind("<Double-Button-1>", quick_roll)

        app.extra_lang_vars.append((nome_var, val_var, linha))