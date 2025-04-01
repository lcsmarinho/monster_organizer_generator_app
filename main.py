import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MonsterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adicionar Monstros")
        self.root.geometry("1200x800")  # Janela maior

        # Dicionários para armazenar os monstros
        self.file_monsters = {}          # Monstros carregados do JSON selecionado
        self.added_monsters = {}         # Monstros adicionados ou carregados do histórico
        self.modified_file_monsters = set()  # Nomes dos monstros do arquivo que foram modificados

        self.file_path = None  # Caminho do arquivo JSON selecionado

        # Definições de quais campos são numéricos ou de lista
        self.numeric_fields = ['classeArmadura', 'forca', 'destreza', 'constituição',
                               'inteligencia', 'sabedoria', 'carisma', 'nivelDesafio']
        self.list_fields = ['ataques', 'ações']
        self.fields = [
            "id", "foto", "nome", "tipo", "alinhamento", "classeArmadura",
            "pontosVida", "deslocamento", "forca", "destreza", "constituição",
            "inteligencia", "sabedoria", "carisma", "pericias", "sentidos",
            "idiomas", "nivelDesafio", "ataques", "ações"
        ]

        self.entries = {}     # Widgets de entrada do formulário
        self.check_vars = {}  # Variáveis dos checkbuttons

        # Carrega histórico automaticamente, se existir
        self.load_history()

        self.setup_ui()

        # Ao fechar, salva o histórico
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        # Frame superior: seleção de arquivo JSON
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        btn_select = ttk.Button(top_frame, text="Selecionar Arquivo .json", command=self.select_file)
        btn_select.pack(side=tk.LEFT)
        self.file_label = ttk.Label(top_frame, text="Nenhum arquivo selecionado")
        self.file_label.pack(side=tk.LEFT, padx=10)

        # Frame principal: à esquerda o formulário; à direita, um Notebook com 2 abas
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Formulário de dados do monstro (lado esquerdo)
        form_frame = ttk.LabelFrame(main_frame, text="Dados do Monstro")
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Canvas com scrollbar para os muitos campos
        canvas = tk.Canvas(form_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        self.form_inner = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.form_inner, anchor="nw")
        self.form_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # Vincula o scroll do mouse enquanto o cursor estiver sobre o canvas
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, canvas)))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Cria um label, campo de entrada (ou Text para campos de lista) e checkbox para cada campo
        for idx, field in enumerate(self.fields):
            lbl = ttk.Label(self.form_inner, text=field)
            lbl.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=2)
            if field in self.list_fields:
                txt = tk.Text(self.form_inner, height=3, width=40)
                txt.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=2)
                self.entries[field] = txt
            else:
                ent = ttk.Entry(self.form_inner, width=40)
                ent.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=2)
                self.entries[field] = ent
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.form_inner, text="Não tem", variable=var,
                                  command=lambda f=field, v=var: self.toggle_field(f, v))
            chk.grid(row=idx, column=2, padx=5, pady=2)
            self.check_vars[field] = var

        # Notebook à direita: duas abas para exibir os monstros
        notebook = ttk.Notebook(main_frame)
        notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Aba dos monstros do arquivo
        self.tab_file = ttk.Frame(notebook)
        notebook.add(self.tab_file, text="Monstros do Arquivo")
        self.file_monster_listbox = tk.Listbox(self.tab_file, width=40)
        self.file_monster_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file_monster_listbox.bind("<Double-Button-1>", lambda event: self.edit_monster_popup("file"))
        # Botões para a aba de monstros do arquivo
        file_button_frame = ttk.Frame(self.tab_file)
        file_button_frame.pack(fill=tk.X, padx=5, pady=5)
        btn_excluir_file = ttk.Button(file_button_frame, text="Excluir", command=self.delete_monster_from_file)
        btn_excluir_file.pack(side=tk.LEFT, padx=5)

        # Aba dos monstros adicionados (histórico)
        self.tab_added = ttk.Frame(notebook)
        notebook.add(self.tab_added, text="Monstros Adicionados")
        self.added_monster_listbox = tk.Listbox(self.tab_added, width=40)
        self.added_monster_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.added_monster_listbox.bind("<Double-Button-1>", lambda event: self.edit_monster_popup("added"))
        # Botões para a aba de histórico
        added_button_frame = ttk.Frame(self.tab_added)
        added_button_frame.pack(fill=tk.X, padx=5, pady=5)
        btn_adicionar_history = ttk.Button(added_button_frame, text="Adicionar ao JSON", command=self.add_monster_from_history)
        btn_adicionar_history.pack(side=tk.LEFT, padx=5)
        btn_excluir_history = ttk.Button(added_button_frame, text="Excluir", command=self.delete_monster_from_history)
        btn_excluir_history.pack(side=tk.LEFT, padx=5)

        # Frame inferior: botões de ação do formulário
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        btn_add = ttk.Button(bottom_frame, text="Adicionar Monstro", command=self.add_monster)
        btn_add.pack(side=tk.LEFT, padx=5)
        btn_generate = ttk.Button(bottom_frame, text="Gerar Arquivo", command=self.generate_file)
        btn_generate.pack(side=tk.LEFT, padx=5)

    def _on_mousewheel(self, event, canvas):
        # Para Windows (event.delta geralmente é múltiplo de 120)
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def toggle_field(self, field, var):
        """
        Se o checkbox é marcado, desabilita o campo e insere o valor padrão:
        - "0" para campos numéricos
        - "nenhum" para os demais (inclusive listas)
        """
        widget = self.entries[field]
        if var.get():
            default = "0" if field in self.numeric_fields else "nenhum"
            if field in self.list_fields:
                widget.config(state=tk.NORMAL)
                widget.delete("1.0", tk.END)
                widget.insert(tk.END, default)
                widget.config(state=tk.DISABLED)
            else:
                widget.config(state=tk.NORMAL)
                widget.delete(0, tk.END)
                widget.insert(0, default)
                widget.config(state="disabled")
        else:
            if field in self.list_fields:
                widget.config(state=tk.NORMAL)
                widget.delete("1.0", tk.END)
            else:
                widget.config(state="normal")
                widget.delete(0, tk.END)

    def add_monster(self):
        """
        Lê os valores do formulário e adiciona o monstro à coleção de
        monstros adicionados (histórico).
        """
        monster = {}
        for field in self.fields:
            widget = self.entries[field]
            if field in self.list_fields:
                if self.check_vars[field].get():
                    value = ["nenhum"]
                else:
                    text = widget.get("1.0", tk.END).strip()
                    value = [line.strip() for line in text.splitlines() if line.strip()]
            else:
                if self.check_vars[field].get():
                    value = "0" if field in self.numeric_fields else "nenhum"
                else:
                    value = widget.get().strip()
            monster[field] = value

        if not monster.get("nome") or monster["nome"] == "nenhum":
            messagebox.showerror("Erro", "O campo 'nome' é obrigatório.")
            return

        self.added_monsters[monster["nome"]] = monster
        self.update_listboxes()
        messagebox.showinfo("Sucesso", f"Monstro '{monster['nome']}' adicionado com sucesso!")
        self.clear_form()

    def update_listboxes(self):
        """Atualiza os dois Listbox (do JSON atual e do histórico)."""
        self.file_monster_listbox.delete(0, tk.END)
        for name in self.file_monsters:
            self.file_monster_listbox.insert(tk.END, name)
        self.added_monster_listbox.delete(0, tk.END)
        for name in self.added_monsters:
            self.added_monster_listbox.insert(tk.END, name)

    def clear_form(self):
        """Limpa os campos do formulário e desmarca os checkbuttons."""
        for field in self.fields:
            widget = self.entries[field]
            if field in self.list_fields:
                widget.config(state=tk.NORMAL)
                widget.delete("1.0", tk.END)
            else:
                widget.config(state=tk.NORMAL)
                widget.delete(0, tk.END)
            self.check_vars[field].set(False)

    def select_file(self):
        """Abre o seletor de arquivo e carrega o JSON selecionado."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.load_file_monsters()
        else:
            self.file_label.config(text="Nenhum arquivo selecionado")

    def load_file_monsters(self):
        """Carrega os monstros do arquivo selecionado."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.file_monsters = {}
                for monster in data:
                    if "nome" in monster:
                        self.file_monsters[monster["nome"]] = monster
            else:
                if "nome" in data:
                    self.file_monsters = {data["nome"]: data}
                else:
                    self.file_monsters = {}
            self.update_listboxes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar monstros do arquivo: {e}")

    def load_history(self):
        """Se existir, carrega os monstros do histórico (historico_monstros.json)."""
        if os.path.exists("historico_monstros.json"):
            try:
                with open("historico_monstros.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for monster in data:
                        if "nome" in monster:
                            self.added_monsters[monster["nome"]] = monster
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar o histórico: {e}")

    def edit_monster_popup(self, source):
        """
        Abre um pop-up para editar o monstro selecionado.
        'source' indica se o monstro vem do arquivo ("file") ou do histórico ("added").
        """
        if source == "file":
            selection = self.file_monster_listbox.curselection()
            if not selection:
                return
            name = self.file_monster_listbox.get(selection[0])
            monster = self.file_monsters[name]
        else:
            selection = self.added_monster_listbox.curselection()
            if not selection:
                return
            name = self.added_monster_listbox.get(selection[0])
            monster = self.added_monsters[name]

        popup = tk.Toplevel(self.root)
        popup.title(f"Editar Monstro - {name}")
        popup.geometry("600x600")
        canvas = tk.Canvas(popup)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # Vincula o scroll do mouse no pop-up
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, canvas)))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        edit_entries = {}
        edit_check_vars = {}
        for idx, field in enumerate(self.fields):
            lbl = ttk.Label(frame, text=field)
            lbl.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=2)
            if field in self.list_fields:
                txt = tk.Text(frame, height=3, width=40)
                txt.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=2)
                current_val = monster.get(field, [])
                if isinstance(current_val, list):
                    txt.insert(tk.END, "\n".join(current_val))
                else:
                    txt.insert(tk.END, current_val)
                edit_entries[field] = txt
            else:
                ent = ttk.Entry(frame, width=40)
                ent.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=2)
                ent.insert(0, monster.get(field, ""))
                edit_entries[field] = ent
            var = tk.BooleanVar(value=(monster.get(field, "") in ["nenhum", "0"]))
            chk = ttk.Checkbutton(frame, text="Não tem", variable=var,
                                  command=lambda f=field, v=var, key=field: self.toggle_field_edit(f, v, edit_entries, key))
            chk.grid(row=idx, column=2, padx=5, pady=2)
            edit_check_vars[field] = var

        def save_changes():
            for field in self.fields:
                widget = edit_entries[field]
                if field in self.list_fields:
                    if edit_check_vars[field].get():
                        value = ["nenhum"]
                    else:
                        text = widget.get("1.0", tk.END).strip()
                        value = [line.strip() for line in text.splitlines() if line.strip()]
                else:
                    if edit_check_vars[field].get():
                        value = "0" if field in self.numeric_fields else "nenhum"
                    else:
                        value = widget.get().strip()
                monster[field] = value
            if source == "file":
                self.modified_file_monsters.add(name)
            self.update_listboxes()
            messagebox.showinfo("Sucesso", f"Monstro '{name}' atualizado com sucesso!")
            popup.destroy()

        btn_save = ttk.Button(frame, text="Salvar Alterações", command=save_changes)
        btn_save.grid(row=len(self.fields), column=0, columnspan=3, pady=10)

    def toggle_field_edit(self, field, var, entries, key):
        widget = entries[key]
        if var.get():
            default = "0" if field in self.numeric_fields else "nenhum"
            if field in self.list_fields:
                widget.config(state=tk.NORMAL)
                widget.delete("1.0", tk.END)
                widget.insert(tk.END, default)
                widget.config(state=tk.DISABLED)
            else:
                widget.config(state=tk.NORMAL)
                widget.delete(0, tk.END)
                widget.insert(0, default)
                widget.config(state="disabled")
        else:
            if field in self.list_fields:
                widget.config(state=tk.NORMAL)
                widget.delete("1.0", tk.END)
            else:
                widget.config(state="normal")
                widget.delete(0, tk.END)

    def delete_monster_from_file(self):
        """Exclui o monstro selecionado da lista do JSON atual."""
        selection = self.file_monster_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um monstro para excluir.")
            return
        name = self.file_monster_listbox.get(selection[0])
        if messagebox.askyesno("Confirmação", f"Excluir o monstro '{name}' do JSON atual?"):
            if name in self.file_monsters:
                del self.file_monsters[name]
            if name in self.modified_file_monsters:
                self.modified_file_monsters.remove(name)
            self.update_listboxes()

    def delete_monster_from_history(self):
        """Exclui o monstro selecionado da lista do histórico."""
        selection = self.added_monster_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um monstro para excluir do histórico.")
            return
        name = self.added_monster_listbox.get(selection[0])
        if messagebox.askyesno("Confirmação", f"Excluir o monstro '{name}' do histórico?"):
            if name in self.added_monsters:
                del self.added_monsters[name]
            self.update_listboxes()

    def add_monster_from_history(self):
        """
        Adiciona o monstro selecionado do histórico ao JSON atual (caso ainda não esteja lá).
        """
        selection = self.added_monster_listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um monstro do histórico para adicionar ao JSON atual.")
            return
        name = self.added_monster_listbox.get(selection[0])
        if name in self.file_monsters:
            messagebox.showinfo("Informação", f"O monstro '{name}' já está no JSON atual.")
            return
        self.file_monsters[name] = self.added_monsters[name]
        self.update_listboxes()
        messagebox.showinfo("Sucesso", f"Monstro '{name}' adicionado ao JSON atual.")

    def generate_file(self):
        """
        Exibe um pop-up com o resumo das alterações e, se confirmado,
        gera um novo arquivo (sem sobrescrever o original) com os monstros do JSON atual.
        """
        summary = "Resumo das alterações:\n\n"
        if self.modified_file_monsters:
            summary += "Monstros modificados (do arquivo):\n"
            for name in self.modified_file_monsters:
                summary += f" - {name}\n"
        if self.added_monsters:
            summary += "\nMonstros adicionados (do histórico):\n"
            for name in self.added_monsters:
                summary += f" - {name}\n"
        summary += "\nDeseja gerar o novo arquivo?\n\n"
        summary += ("Observação: O arquivo original não será alterado; "
                    "um novo arquivo será criado contendo as alterações e adições.")
        if not messagebox.askyesno("Confirmar Geração de Arquivo", summary):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                original_data = json.load(f)
            if not isinstance(original_data, list):
                original_data = [original_data]
            # Atualiza os monstros modificados do JSON original
            for i, monster in enumerate(original_data):
                if monster.get("nome") in self.modified_file_monsters:
                    original_data[i] = self.file_monsters[monster.get("nome")]
            # Adiciona os monstros do JSON atual que não estão no original
            for name, monster in self.file_monsters.items():
                if not any(m.get("nome") == name for m in original_data):
                    original_data.append(monster)
            base, ext = os.path.splitext(self.file_path)
            new_file_path = f"{base}_novos_monstros{ext}"
            with open(new_file_path, "w", encoding="utf-8") as f:
                json.dump(original_data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Sucesso", f"Novo arquivo gerado: {os.path.basename(new_file_path)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar novo arquivo: {e}")

    def on_closing(self):
        """Salva o histórico (monstros adicionados) em 'historico_monstros.json' ao fechar."""
        if self.added_monsters:
            try:
                with open("historico_monstros.json", "w", encoding="utf-8") as f:
                    json.dump(list(self.added_monsters.values()), f, ensure_ascii=False, indent=4)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o histórico: {e}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MonsterApp(root)
    root.mainloop()
