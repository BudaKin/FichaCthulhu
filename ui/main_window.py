# ui/main_window.py
import os
import sys
import json
import datetime
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

from core.data import SKILLS, ATTRS
from core.dice import eval_dice_expression
from core import storage
from ui.autocomplete import AutocompleteEntry
from ui import dialogs
from ui.components import make_scrollable_text

class PerditioGUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="vapor")
        self.title("Editor de Ficha (Lixo's Enterprise)")
        self._set_icon()
        self.geometry("1100x800")
        self.minsize(900,600)

        my_style = ttk.Style()
        self.default_font = ("Metal Mania", 11)
        self.option_add("*Font", self.default_font)
        my_style.configure(".", font=self.default_font)

        self._roll_window = None
        self.roll_history = []
        self._active_scroll_widget = None
        self.bind_all("<MouseWheel>", self._on_global_mousewheel)

        # garante que a pasta "fichas" exista
        self.fichas_dir = os.path.join(os.getcwd(), "fichas")
        os.makedirs(self.fichas_dir, exist_ok=True)

        self.selected_path = os.path.join(self.fichas_dir, "selected.json")

        # storage
        self.extra_lang_vars = []  # list of tuples (name_var, value_var, name_entry_widget)

        self.create_widgets()

        # Tenta carregar selected.json ao iniciar (se existir)
        try:
            with open(self.selected_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._apply_data(data)
        except FileNotFoundError:
            pass
        except Exception as e:
            try:
                messagebox.showwarning("Aviso", f"Erro ao abrir selected.json:\n{e}")
            except Exception:
                pass

        # centraliza janela principal
        self.after(10, self._centralize_main_window)

    def _set_icon(self):
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, "..", "assets", "cthulhu.ico")
            icon_path = os.path.normpath(icon_path)
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass

    def _centralize_main_window(self):
        try:
            self.update_idletasks()
            w = self.winfo_width()
            h = self.winfo_height()
            x = (self.winfo_screenwidth() // 2) - (w // 2)
            y = (self.winfo_screenheight() // 2) - (h // 2)
            self.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

    def show_quick_roll_popup(self, title, text):
        dialogs.show_quick_roll_popup(self, title, text)

    def _set_active_scroll(self, widget):
        self._active_scroll_widget = widget

    def _on_global_mousewheel(self, event):
        w = getattr(self, "_active_scroll_widget", None)
        if not w:
            return
        try:
            w.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Botões principais (topo)
        btn_frame = ttk.Frame(main_frame, height=40)
        btn_frame.pack(side="top", fill="x")
        btn_frame.pack_propagate(False)  # impede que o frame encolha
        ttk.Button(btn_frame, text="Salvar (JSON)", command=self.save_json, bootstyle="success").pack(side="left", padx=6, pady=4)
        ttk.Button(btn_frame, text="Carregar (JSON)", command=self.load_json, bootstyle="info").pack(side="left", padx=6, pady=4)
        ttk.Button(btn_frame, text="Exportar Texto", command=self.export_text, bootstyle="secondary").pack(side="left", padx=6, pady=4)
        ttk.Button(btn_frame, text="Rolar Dados", command=self.open_roll_window, bootstyle="primary").pack(side="left", padx=6, pady=4)
        ttk.Button(btn_frame, text="Limpar", command=self.clear_all, bootstyle="danger").pack(side="right", padx=6, pady=4)

        paned = ttk.PanedWindow(main_frame, orient="horizontal")
        paned.pack(fill="both", expand=True)

        left_frame = ttk.Frame(paned, width=520)
        right_frame = ttk.Frame(paned, width=520)
        paned.add(left_frame, weight=1)
        paned.add(right_frame, weight=1)

        # Cabeçalho
        header = ttk.Labelframe(left_frame, text="Identificação")
        header.pack(fill="x", padx=8, pady=6)
        labels = [
            ("Nome", "nome"), ("Arquétipo", "arquetipo"), ("NEX", "nex"),
            ("Ocupação", "ocupacao"), ("Dinheiro", "dinheiro"), ("Deslocamento", "deslocamento"),
            ("Estilo de Luta", "estilo_luta"), ("Soco", "soco"), ("Bônus de Dano", "bonus_dano")
        ]
        self.header_vars = {}
        for i, (lab, key) in enumerate(labels):
            r = i // 3
            c = (i % 3) * 2
            ttk.Label(header, text=lab).grid(row=r, column=c, sticky="w", padx=4, pady=2)
            v = tk.StringVar()
            self.header_vars[key] = v
            ttk.Entry(header, textvariable=v, width=22).grid(row=r, column=c+1, sticky="w", padx=4, pady=2)

        # Atributos
        attr_frame = ttk.Labelframe(left_frame, text="Atributos")
        attr_frame.pack(fill="x", padx=8, pady=6)
        self.attr_vars = {}
        for i, name in enumerate(ATTRS):
            lbl = ttk.Label(attr_frame, text=name)
            lbl.grid(row=i//6, column=(i%6)*2, sticky="w", padx=4, pady=2)
            v = tk.StringVar()
            self.attr_vars[name] = v
            e = ttk.Entry(attr_frame, textvariable=v, width=8)
            e.grid(row=i//6, column=(i%6)*2+1, sticky="w", padx=4, pady=2)
            lbl.bind("<Double-Button-1>", lambda ev, n=name: self.quick_roll(n, force_2d12=True))

        # Status
        stats_frame = ttk.Labelframe(left_frame, text="Status")
        stats_frame.pack(fill="x", padx=8, pady=6)
        ttk.Label(stats_frame, text="Vida").grid(row=0, column=0, padx=4, sticky="w")
        self.vida_var = tk.StringVar()
        ttk.Entry(stats_frame, textvariable=self.vida_var, width=10).grid(row=0, column=1, padx=4)
        ttk.Label(stats_frame, text="Sanidade").grid(row=0, column=2, padx=4, sticky="w")
        self.san_var = tk.StringVar()
        ttk.Entry(stats_frame, textvariable=self.san_var, width=10).grid(row=0, column=3, padx=4)
        ttk.Label(stats_frame, text="Ocultismo").grid(row=0, column=4, padx=4, sticky="w")
        self.ocult_var = tk.StringVar()
        ttk.Entry(stats_frame, textvariable=self.ocult_var, width=10).grid(row=0, column=5, padx=4)

        # Outras Perícia
        lang_frame = ttk.Labelframe(left_frame, text="Outras Perícias")
        lang_frame.pack(fill="x", padx=8, pady=6)
        self.lang_container = ttk.Frame(lang_frame)
        self.lang_container.pack(fill="x", padx=4, pady=4)
        ttk.Button(lang_frame, text="+ Adicionar Perícia", bootstyle="info", command=self.add_language).pack(pady=2)

        # Perícias
        skills_frame = ttk.Labelframe(left_frame, text="Perícias (valores)")
        skills_frame.pack(fill="both", expand=True, padx=8, pady=6)
        canvas = tk.Canvas(skills_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(skills_frame, orient="vertical", command=canvas.yview, bootstyle="round")
        scrollable = ttk.Frame(canvas)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e, w=canvas: self._set_active_scroll(w))
        canvas.bind("<Leave>", lambda e: self._set_active_scroll(None))

        self.skill_vars = {}
        N_COLS = 3
        for i, s in enumerate(SKILLS):
            row = i // N_COLS
            col = (i % N_COLS) * 2
            lbl = ttk.Label(scrollable, text=s)
            lbl.grid(row=row, column=col, sticky="w", padx=4, pady=2)
            v = tk.StringVar()
            self.skill_vars[s] = v
            e = ttk.Entry(scrollable, textvariable=v, width=8)
            e.grid(row=row, column=col+1, padx=4, pady=2)
            lbl.bind("<Double-Button-1>", lambda ev, n=s: self.quick_roll(n, force_2d12=True))

        # Blocos de texto (direita)
        self.habilidades_text = make_scrollable_text(right_frame, "Habilidades", 6)
        self.equip_text = make_scrollable_text(right_frame, "Equipamento", 6)
        self.rituals_text = make_scrollable_text(right_frame, "Rituais", 10)
        self.vant_text = make_scrollable_text(right_frame, "Vantagens / Complicações", 6)
        self.back_text = make_scrollable_text(right_frame, "Rosto do Personagem / Backstory", 10)

    # ---------------- Ações rápidas ----------------
    def quick_roll(self, name, force_2d12=False):
        bonus = 0
        if name in self.attr_vars:
            try: bonus = int(self.attr_vars[name].get())
            except: pass
        elif name in self.skill_vars:
            try: bonus = int(self.skill_vars[name].get())
            except: pass
        else:
            for name_var, val_var, _ in self.extra_lang_vars:
                if name_var.get().strip() == name:
                    try: bonus = int(val_var.get())
                    except: pass
                    break

        expr = '2d12' if force_2d12 else '1d20'
        val, details = eval_dice_expression(expr)
        total = val + bonus
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        out = f'[{timestamp}] {expr} + {name}({bonus}) => {total}\nDetalhes: {details}\n\n'
        self.roll_history.append(out)

        if hasattr(self, 'history_box') and self._roll_window and tk.Toplevel.winfo_exists(self._roll_window):
            self._set_window_icon(self._roll_window)
            self.history_box.insert('end', out)
            self.history_box.see('end')
        else:
            self.show_quick_roll_popup("Quick Roll", out)

    def add_language(self, name="", value=""):
        f = ttk.Frame(self.lang_container)
        f.pack(fill="x", pady=2)
        v1 = tk.StringVar(value=name)
        v2 = tk.StringVar(value=value)
        name_entry = ttk.Entry(f, textvariable=v1, width=20)
        name_entry.pack(side="left", padx=4)
        val_entry = ttk.Entry(f, textvariable=v2, width=8)
        val_entry.pack(side="left", padx=4)
        ttk.Button(f, text="X", bootstyle="danger", command=lambda: (f.destroy(), self._remove_lang_vars(v1, v2))).pack(side="left", padx=4)
        name_entry.bind("<Double-Button-1>", lambda ev, nvar=v1: self.quick_roll(nvar.get(), force_2d12=True))
        try:
            v1.trace_add("write", lambda *a: self._update_autocomplete_sources())
        except Exception:
            v1.trace("w", lambda *a: self._update_autocomplete_sources())
        self.extra_lang_vars.append((v1, v2, name_entry))
        self._update_autocomplete_sources()

    def _remove_lang_vars(self, v1, v2):
        for t in list(self.extra_lang_vars):
            if t[0] is v1 and t[1] is v2:
                try:
                    self.extra_lang_vars.remove(t)
                except ValueError:
                    pass
        self._update_autocomplete_sources()

    def _get_all_roll_keys(self):
        keys = list(self.attr_vars.keys()) + list(self.skill_vars.keys())
        for v1, v2, _ in self.extra_lang_vars:
            n = v1.get().strip()
            if n:
                keys.append(n)
        return sorted(set(keys), key=str.lower)

    def _update_autocomplete_sources(self):
        if hasattr(self, 'roll_attr_entry') and isinstance(self.roll_attr_entry, AutocompleteEntry):
            self.roll_attr_entry.update_list(self._get_all_roll_keys())

    # ---------------- Dados e Exportações ----------------
    def gather_data(self):
        langs = []
        for v1, v2, _ in self.extra_lang_vars:
            if v1.get().strip() or v2.get().strip():
                langs.append({"nome": v1.get().strip(), "valor": v2.get().strip()})
        return {
            "header": {k: v.get() for k, v in self.header_vars.items()},
            "attributes": {k: v.get() for k, v in self.attr_vars.items()},
            "status": {"vida": self.vida_var.get(), "sanidade": self.san_var.get(), "ocultismo": self.ocult_var.get()},
            "skills": {k: v.get() for k, v in self.skill_vars.items()},
            "languages": langs,
            "habilidades": self.habilidades_text.get("1.0", "end").strip(),
            "rituals": self.rituals_text.get("1.0", "end").strip(),
            "equipment": self.equip_text.get("1.0", "end").strip(),
            "advantages": self.vant_text.get("1.0", "end").strip(),
            "backstory": self.back_text.get("1.0", "end").strip()
        }

    def save_json(self):
        data = self.gather_data()
        fpath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
        if not fpath: return
        storage.save_json_to_path(data, fpath)
        messagebox.showinfo("Salvo", f"Ficha salva em:\n{fpath}")

    def load_json(self):
        fpath = filedialog.askopenfilename(
            filetypes=[("JSON files","*.json")],
            initialdir=self.fichas_dir  # abre direto na pasta "fichas"
        )
        if not fpath: return
        data = storage.load_json_from_path(fpath)
        self._apply_data(data)

        # sobrescreve sempre o fichas/selected.json
        try:
            storage.save_json_to_path(data, self.selected_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar selected.json:\n{e}")

        messagebox.showinfo("Carregado", f"Ficha carregada de:\n{fpath}\n(selected.json atualizado)")

    def _apply_data(self, data):
        for k, v in data.get("header", {}).items():
            if k in self.header_vars: self.header_vars[k].set(v)
        for k, v in data.get("attributes", {}).items():
            if k in self.attr_vars: self.attr_vars[k].set(v)
        st = data.get("status", {})
        self.vida_var.set(st.get("vida", ""))
        self.san_var.set(st.get("sanidade", ""))
        self.ocult_var.set(st.get("ocultismo", ""))
        for k, v in data.get("skills", {}).items():
            if k in self.skill_vars: self.skill_vars[k].set(v)
        # línguas extras: limpar e recriar
        for child in self.lang_container.winfo_children():
            child.destroy()
        self.extra_lang_vars.clear()
        for lang in data.get("languages", []):
            self.add_language(lang.get("nome", ""), lang.get("valor", ""))
        # textos
        self.habilidades_text.delete("1.0", "end"); self.habilidades_text.insert("1.0", data.get("habilidades", ""))
        self.rituals_text.delete("1.0", "end"); self.rituals_text.insert("1.0", data.get("rituals", ""))
        self.equip_text.delete("1.0", "end"); self.equip_text.insert("1.0", data.get("equipment", ""))
        self.vant_text.delete("1.0", "end"); self.vant_text.insert("1.0", data.get("advantages", ""))
        self.back_text.delete("1.0", "end"); self.back_text.insert("1.0", data.get("backstory", ""))
        self._update_autocomplete_sources()

    def export_text(self):
        data = self.gather_data()
        fpath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if not fpath: return
        storage.export_text_to_path(data, fpath)
        messagebox.showinfo("Exportado", f"Ficha exportada em:\n{fpath}")

    def clear_all(self):
        if not messagebox.askyesno("Confirmar", "Deseja realmente limpar todos os campos?"):
            return
        for v in self.header_vars.values(): v.set("")
        for v in self.attr_vars.values(): v.set("")
        self.vida_var.set(""); self.san_var.set(""); self.ocult_var.set("")
        for v in self.skill_vars.values(): v.set("")
        for child in self.lang_container.winfo_children():
            child.destroy()
        self.extra_lang_vars.clear()
        for t in [self.habilidades_text, self.rituals_text, self.equip_text, self.vant_text, self.back_text]:
            t.delete("1.0", "end")

    # ---------------- Rolador de dados ----------------
    def open_roll_window(self, prefill_attr=None):
        if self._roll_window and tk.Toplevel.winfo_exists(self._roll_window):
            self._roll_window.destroy()
            self._roll_window = None

        win = tk.Toplevel(self)
        win.title("Rolador de Dados")
        dialogs.set_window_icon(win)
        win.geometry("420x440")
        self._roll_window = win

        ttk.Label(win, text="Expressão (ex: 2d12+3)").pack(anchor="w", padx=8, pady=(8,2))
        self.roll_expr_var = tk.StringVar()
        ttk.Entry(win, textvariable=self.roll_expr_var).pack(fill="x", padx=8, pady=(0,8))

        ttk.Label(win, text="Atributo/Perícia (opcional)").pack(anchor="w", padx=8, pady=(4,2))
        self.roll_attr_entry = AutocompleteEntry(win, self._get_all_roll_keys())
        self.roll_attr_entry.pack(fill="x", padx=8, pady=(0,8))

        if prefill_attr:
            win.after(10, lambda: self.roll_attr_entry.var.set(prefill_attr))

        ttk.Button(win, text="Rolar", bootstyle="success", command=self.perform_roll).pack(pady=6)

        hist_frame = ttk.Labelframe(win, text="Histórico de Rolagens")
        hist_frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.history_box = tk.Text(hist_frame, height=12, wrap="word")
        self.history_box.pack(fill="both", expand=True, padx=4, pady=4)
        self.history_box.bind("<Enter>", lambda e: self._set_active_scroll(self.history_box))
        self.history_box.bind("<Leave>", lambda e: self._set_active_scroll(None))
        for line in self.roll_history:
            self.history_box.insert("end", line)
        self.history_box.see('end')

    def perform_roll(self):
        expr = self.roll_expr_var.get().strip()
        if not expr:
            messagebox.showwarning("Aviso", "Digite uma expressão de dados para rolar (ex: 2d6+3).")
            return
        attr_name = ''
        if hasattr(self, 'roll_attr_entry'):
            attr_name = self.roll_attr_entry.var.get().strip()
        bonus = 0
        if attr_name:
            if attr_name in self.attr_vars:
                try: bonus = int(self.attr_vars[attr_name].get())
                except: bonus = 0
            elif attr_name in self.skill_vars:
                try: bonus = int(self.skill_vars[attr_name].get())
                except: bonus = 0
            else:
                for name_var, val_var, _ in self.extra_lang_vars:
                    if name_var.get().strip() == attr_name:
                        try: bonus = int(val_var.get())
                        except: bonus = 0
                        break

        try:
            val, details = eval_dice_expression(expr)
        except Exception as e:
            messagebox.showerror("Erro", f"Expressão inválida: {e}")
            return
        total = val + bonus
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        out = f"[{timestamp}] {expr} = {val}"
        if attr_name:
            out += f" + {attr_name} = {bonus}"
        out += f" => Total = {total}\nDetalhes: {details}\n\n"
        self.roll_history.append(out)
        if hasattr(self, 'history_box') and self._roll_window and tk.Toplevel.winfo_exists(self._roll_window):
            self.history_box.insert('end', out)
            self.history_box.see('end')