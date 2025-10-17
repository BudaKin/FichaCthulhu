import os
import sys
import json
import datetime
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

from ui.autocomplete import AutocompleteEntry
from ui import dialogs
from core.dice import eval_dice_expression
from core import storage

from ui.tela_ficha import TelaFicha
from ui.tela_info import TelaInfo
from ui.tela_build import TelaBuild
from ui.tela_rituais import TelaRituais

def resource_path(relative_path):
    """Retorna o caminho absoluto para recursos, compatível com PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



class PerditioGUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="vapor")
        self.title("Ficha de personagem (Lixo's Enterprise)")
        self.geometry("1100x800")
        self.minsize(900, 600)
        self._set_icon()

        self.default_font = ("Metal Mania", 11)
        self.option_add("*Font", self.default_font)

        self.fichas_dir = os.path.join(os.getcwd(), "fichas")
        os.makedirs(self.fichas_dir, exist_ok=True)
        self.selected_path = os.path.join(self.fichas_dir, "selected.json")

        self.roll_history = []
        self.header_vars = {}
        self.attr_vars = {}
        self.skill_vars = {}
        self.extra_lang_vars = []
        self.vida_var = tk.StringVar()
        self.san_var = tk.StringVar()
        self.ocult_var = tk.StringVar()

        self.habilidades_text = None
        self.equip_text = None
        self.vant_text = None
        self.comp_text = None
        self.back_text = None
        self.rituals_text = None
        self.rituals_text2 = None
        self.lang_container = None

        self.create_widgets()
        self._try_load_selected()
        self.after(10, self._centralize_window)

    def _set_icon(self):
        try:
            icon_path = resource_path("assets/cthulhu.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass


    def _centralize_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _try_load_selected(self):
        try:
            if os.path.exists(self.selected_path):
                with open(self.selected_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._apply_data(data)
        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao abrir selected.json:\n{e}")

    def create_widgets(self):
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=4, padx=4)

        ttk.Button(top_bar, text="Salvar (JSON)", command=self.save_json, bootstyle="success").pack(side="right", padx=4)
        ttk.Button(top_bar, text="Carregar", command=self.load_json, bootstyle="info").pack(side="right", padx=4)
        ttk.Button(top_bar, text="Rolar Dados", command=self.open_roll_window, bootstyle="primary").pack(side="right", padx=4)
        ttk.Button(top_bar, text="Limpar", command=self.clear_all, bootstyle="danger").pack(side="right", padx=4)

        notebook = ttk.Notebook(self, bootstyle="primary")
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.tela_ficha = TelaFicha(notebook, self)
        self.tela_build = TelaBuild(notebook, self)
        self.tela_info = TelaInfo(notebook, self)
        self.tela_rituais = TelaRituais(notebook, self)

        notebook.add(self.tela_ficha, text="Ficha")
        notebook.add(self.tela_info, text="Info")
        notebook.add(self.tela_build, text="Build")
        notebook.add(self.tela_rituais, text="Rituais")

        self.notebook = notebook

    # -------------------------- ARQUIVOS --------------------------
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
            "habilidades": self.habilidades_text.get("1.0", "end").strip() if self.habilidades_text else "",
            "rituals": self.rituals_text.get("1.0", "end").strip() if self.rituals_text else "",
            "rituals2": self.rituals_text2.get("1.0", "end").strip() if self.rituals_text2 else "",
            "equipment": self.equip_text.get("1.0", "end").strip() if self.equip_text else "",
            "advantages": self.vant_text.get("1.0", "end").strip() if self.vant_text else "",
            "complications": self.comp_text.get("1.0", "end").strip() if self.comp_text else "",
            "backstory": self.back_text.get("1.0", "end").strip() if self.back_text else ""
        }

    def save_json(self):
        data = self.gather_data()
        fpath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not fpath:
            return
        storage.save_json_to_path(data, fpath)
        messagebox.showinfo("Salvo", f"Ficha salva em:\n{fpath}")

    def load_json(self):
        fpath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], initialdir=self.fichas_dir)
        if not fpath:
            return
        data = storage.load_json_from_path(fpath)
        self._apply_data(data)
        try:
            storage.save_json_to_path(data, self.selected_path)
        except Exception:
            pass
        messagebox.showinfo("Carregado", f"Ficha carregada:\n{fpath}")

    # -------------------------- ROLADOR --------------------------
    def open_roll_window(self):
        roll_win = ttk.Toplevel(self)
        roll_win.title("Rolador de Dados")
        roll_win.geometry("420x520")
        roll_win.resizable(False, False)

        # Define ícone
        dialogs.set_window_icon(roll_win)

        # Centraliza
        roll_win.update_idletasks()
        x = (roll_win.winfo_screenwidth() // 2) - (420 // 2)
        y = (roll_win.winfo_screenheight() // 2) - (520 // 2)
        roll_win.geometry(f"+{x}+{y}")

        frm = ttk.Frame(roll_win, padding=10)
        frm.pack(fill="both", expand=True)

        # Perícia ou Atributo
        ttk.Label(frm, text="Perícia ou Atributo:").pack(pady=4)
        
        # Pega nomes das outras perícias adicionadas dinamicamente
        dynamic_skills = [n_var.get() for n_var, _, _ in self.extra_lang_vars if n_var.get().strip()]

        # Lista completa para autocomplete
        all_names = list(self.skill_vars.keys()) + list(self.attr_vars.keys()) + dynamic_skills

        entry = AutocompleteEntry(frm, all_names)

        entry.pack(pady=3)

        # Expressão de dados
        ttk.Label(frm, text="Expressão de dados (ex: 2d12):").pack(pady=4)
        dice_var = tk.StringVar(value="2d12")
        ttk.Entry(frm, textvariable=dice_var, width=12).pack(pady=3)

        # Botão de rolar
        ttk.Button(
            frm,
            text="Rolar!",
            bootstyle="success",
            command=lambda: self._perform_roll(entry.get(), dice_var.get(), output, show_popup=False)
        ).pack(pady=6)

        # Histórico
        ttk.Label(frm, text="Histórico").pack(pady=(10, 0))
        output = tk.Text(frm, height=14, wrap="word", state="normal")
        output.pack(fill="both", expand=True)
        output.insert("1.0", "".join(self.roll_history))
        output.configure(state="disabled")

        roll_win.grab_set()

    def _perform_roll(self, nome, expr, output=None, show_popup=True):
        from datetime import datetime
        nome = nome.strip()
        if not nome:
            messagebox.showwarning("Aviso", "Escolha uma perícia ou atributo primeiro.")
            return

        # Pega apenas o valor da perícia ou atributo
        if nome in self.skill_vars:
            try:
                mod = int(self.skill_vars[nome].get() or 0)
            except:
                mod = 0
        elif nome in self.attr_vars:
            try:
                mod = int(self.attr_vars[nome].get() or 0)
            except:
                mod = 0
        else:
            # Outras perícias adicionadas dinamicamente
            for n_var, v_var, _ in self.extra_lang_vars:
                if n_var.get().strip() == nome:
                    try:
                        mod = int(v_var.get() or 0)
                    except:
                        mod = 0
                    break
            else:
                mod = 0

        expr = expr.strip()
        if not expr or "d" not in expr:
            expr = "2d12"

        try:
            val, details = eval_dice_expression(expr)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na expressão de dados: {e}")
            return

        total = val + mod  # SOMENTE o modificador da perícia/atributo

        # Mostra mod somente se diferente de 0
        mod_str = f"+{mod}" if mod != 0 else ""
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {expr}{mod_str} (de {nome}) => {total}\nDetalhes: {details}\n\n"

        # Atualiza histórico
        self.roll_history.append(line)
        if output:
            output.configure(state="normal")
            output.insert("1.0", line)
            output.configure(state="disabled")

        # Só mostra popup se for uma rolagem rápida (duplo clique)
        if show_popup:
            dialogs.show_quick_roll_popup(self, f"Rolagem: {nome}", line)

    # -------------------------- DADOS / LIMPEZA --------------------------
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

        if self.lang_container:
            for child in self.lang_container.winfo_children():
                child.destroy()
        self.extra_lang_vars.clear()
        for lang in data.get("languages", []):
            self.tela_ficha.add_language(self, lang.get("nome", ""), lang.get("valor", ""))

        def s(widget, value):
            if widget:
                widget.delete("1.0", "end")
                widget.insert("1.0", value)

        s(self.habilidades_text, data.get("habilidades", ""))
        s(self.rituals_text, data.get("rituals", ""))
        s(self.rituals_text2, data.get("rituals2", ""))
        s(self.equip_text, data.get("equipment", ""))
        s(self.vant_text, data.get("advantages", ""))
        s(self.comp_text, data.get("complications", ""))
        s(self.back_text, data.get("backstory", ""))

    def clear_all(self):
        if not messagebox.askyesno("Confirmar", "Deseja realmente limpar todos os campos?"):
            return
        for v in self.header_vars.values(): v.set("")
        for v in self.attr_vars.values(): v.set("")
        for v in self.skill_vars.values(): v.set("")
        self.vida_var.set(""); self.san_var.set(""); self.ocult_var.set("")
        if self.lang_container:
            for c in self.lang_container.winfo_children(): c.destroy()
        self.extra_lang_vars.clear()
        for t in [self.habilidades_text, self.rituals_text, self.rituals_text2, self.equip_text, self.vant_text, self.comp_text, self.back_text]:
            if t:
                t.delete("1.0", "end")

    # def add_language(self, nome="", valor=""):
    #     if not self.lang_container:
    #         return
    #     frame = ttk.Frame(self.lang_container)
    #     frame.pack(fill="x", pady=2)
    #     name_var = tk.StringVar(value=nome)
    #     val_var = tk.StringVar(value=valor)
    #     e1 = ttk.Entry(frame, textvariable=name_var, width=25)
    #     e1.pack(side="left", padx=3)
    #     e2 = ttk.Entry(frame, textvariable=val_var, width=8)
    #     e2.pack(side="left", padx=3)
    #     btn = ttk.Button(frame, text="x", bootstyle="danger", command=frame.destroy, width=2)
    #     btn.pack(side="left")
    #     self.extra_lang_vars.append((name_var, val_var, frame))