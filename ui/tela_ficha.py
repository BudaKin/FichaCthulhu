import tkinter as tk
import ttkbootstrap as ttk
from core.data import SKILLS, ATTRS

class TelaFicha(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # -------- Cabeçalho --------
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

        # -------- Atributos --------
        attr_frame = ttk.Labelframe(self, text="Atributos")
        attr_frame.pack(fill="x", padx=8, pady=6)
        for i, name in enumerate(ATTRS):
            lbl = ttk.Label(attr_frame, text=name)
            lbl.grid(row=i//6, column=(i%6)*2, sticky="w", padx=4, pady=2)
            lbl.bind("<Double-Button-1>", lambda ev, n=name: app._perform_roll(n, "2d12"))
            v = app.attr_vars.setdefault(name, tk.StringVar())
            ttk.Entry(attr_frame, textvariable=v, width=8).grid(row=i//6, column=(i%6)*2+1, sticky="w", padx=4, pady=2)

        # -------- Status --------
        stats_frame = ttk.Labelframe(self, text="Status")
        stats_frame.pack(fill="x", padx=8, pady=6)
        ttk.Label(stats_frame, text="Vida").grid(row=0, column=0, padx=4, sticky="w")
        ttk.Entry(stats_frame, textvariable=app.vida_var, width=10).grid(row=0, column=1, padx=4)
        ttk.Label(stats_frame, text="Sanidade").grid(row=0, column=2, padx=4, sticky="w")
        ttk.Entry(stats_frame, textvariable=app.san_var, width=10).grid(row=0, column=3, padx=4)
        ttk.Label(stats_frame, text="Ocultismo").grid(row=0, column=4, padx=4, sticky="w")
        ttk.Entry(stats_frame, textvariable=app.ocult_var, width=10).grid(row=0, column=5, padx=4)

        # -------- Perícias com Scroll --------
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

        # ---- Centralização das perícias ----
        self.center_frame = ttk.Frame(scrollable)
        self.center_frame.pack(anchor="center", pady=8)

        self.scrollable_skills = self.center_frame
        self._bind_mousewheel(canvas)

        # -------- Perícias Fixas --------
        for i, s in enumerate(SKILLS):
            row = i // 3
            col = (i % 3) * 2
            lbl = ttk.Label(self.center_frame, text=s)
            lbl.grid(row=row, column=col, sticky="w", padx=4, pady=2)
            lbl.bind("<Double-Button-1>", lambda ev, n=s: app._perform_roll(n, "2d12"))
            v = app.skill_vars.setdefault(s, tk.StringVar())
            ttk.Entry(self.center_frame, textvariable=v, width=8).grid(row=row, column=col+1, padx=4, pady=2)

        # -------- Botão Adicionar Perícia --------
        self.btn_add = ttk.Button(
            self.center_frame,
            text="+ Adicionar Perícia",
            bootstyle="info",
            command=lambda: self.add_language(app)
        )
        self._reposicionar_botao(app)

    # ===== Scroll com mouse =====
    def _bind_mousewheel(self, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # ===== Adicionar perícia extra =====
    def add_language(self, app, nome = "", val = ""):
        """Adiciona uma nova perícia extra e reposiciona o botão."""
        scrollable = self.scrollable_skills
        per_row = 3
        total = len(SKILLS) + len(app.extra_lang_vars)

        row = total // per_row
        col = (total % per_row) * 2

        linha = ttk.Frame(scrollable)
        linha.grid(row=row, column=col, columnspan=2, padx=4, pady=2, sticky="w")

        nome_var = tk.StringVar(value=nome)
        val_var = tk.StringVar(value=val)

        ttk.Entry(linha, textvariable=nome_var, width=20).pack(side="left", padx=4)
        ttk.Entry(linha, textvariable=val_var, width=8).pack(side="left", padx=4)

        btn_remove = ttk.Button(linha, text="✖", bootstyle="danger", width=2,
                                command=lambda l=linha: self.remover(app, l))
        btn_remove.pack(side="left", padx=2)

        def quick_roll(ev):
            nome = nome_var.get()
            app._perform_roll(nome, "2d12")
        linha.winfo_children()[0].bind("<Double-Button-1>", quick_roll)
        linha.winfo_children()[1].bind("<Double-Button-1>", quick_roll)

        app.extra_lang_vars.append((nome_var, val_var, linha))
        self._reorganizar_extras(app)

    # ===== Reorganizar matriz e reposicionar botão =====
    def _reorganizar_extras(self, app):
        per_row = 3
        vivos = [(n, v, l) for (n, v, l) in app.extra_lang_vars if l.winfo_exists()]

        for i, (_, _, linha) in enumerate(vivos):
            linha.grid_forget()
            row = (len(SKILLS) + i) // per_row
            col = (i % per_row) * 2
            linha.grid(row=row, column=col, columnspan=2, padx=4, pady=2, sticky="w")

        app.extra_lang_vars = vivos
        self._reposicionar_botao(app)

    # ===== Posiciona o botão sempre abaixo da última linha =====
    def _reposicionar_botao(self, app):
        per_row = 3
        total = len(SKILLS) + len(app.extra_lang_vars)
        row = total // per_row
        col = (total % per_row) * 2
        self.btn_add.grid_forget()
        self.btn_add.grid(row=row, column=col, columnspan=2, padx=4, pady=6, sticky="w")

    # ===== Remover perícia extra =====
    def remover(self, app, linha):
        app.extra_lang_vars = [(n, v, l) for (n, v, l) in app.extra_lang_vars if l != linha]
        linha.destroy()
        self._reorganizar_extras(app)
