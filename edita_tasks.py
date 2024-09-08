import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes, constants


class CategoriaAtualizador:
    def __init__(self):
        self.categorias = ["All"]
        self.id_to_nome = {}  
        self.ids_atualizados = set()  

    def atualizar_categorias(self):
        novos_id_para_nome = {}
        try:
            with open("categorias.txt", "r") as file:
                categoria = {}
                for line in file:
                    if line.startswith("Id:"):
                        categoria_id = line.split("Id:")[1].strip()
                        categoria["id"] = categoria_id
                    elif line.startswith("Nome:"):
                        categoria_nome = line.split("Nome:")[1].strip()
                        categoria["nome"] = categoria_nome
                        novos_id_para_nome[categoria["id"]] = categoria["nome"]

            self.ids_atualizados = set(novos_id_para_nome.keys())
            categorias_atualizadas = ["All"] + [nome for id_, nome in novos_id_para_nome.items()]
            self.categorias = categorias_atualizadas

            ids_removidos = set(self.id_to_nome.keys()) - self.ids_atualizados

            for id_ in ids_removidos:
                nome = self.id_to_nome[id_]
                if nome in self.categorias:
                    self.categorias.remove(nome)
                del self.id_to_nome[id_]

            self.id_to_nome.update(novos_id_para_nome)

        except FileNotFoundError:
            print("O arquivo categorias.txt não foi encontrado.")

    def get_categorias(self):
        return self.categorias



def salvar_edicao(task, janela_editar):
    task_id = task["id"]
    novo_nome = entry_nome.get().strip()
    nova_prioridade = cmb_prioridade.get()
    novo_prazo = entry_prazo.get().strip()
    novo_autor = entry_autor.get().strip()
    nova_categoria = cmb_categoria.get().strip()

    if novo_nome and nova_prioridade != "Selecione a Prioridade" and novo_prazo and novo_autor:
        with open("tasks.txt", "r") as arquivo:
            linhas = arquivo.readlines()

        with open("tasks.txt", "w") as arquivo:
            skip_lines = False
            for linha in linhas:
                if linha.startswith('Id: '):
                    current_id = linha.strip().split(': ', 1)[1]
                    skip_lines = current_id == task_id
                if skip_lines and linha.startswith('Nome da task:'):
                    arquivo.write(f"Nome da task: {novo_nome}\n")
                elif skip_lines and linha.startswith('Prioridade:'):
                    arquivo.write(f"Prioridade: {nova_prioridade}\n")
                elif skip_lines and linha.startswith('Prazo:'):
                    arquivo.write(f"Prazo: {novo_prazo}\n")
                elif skip_lines and linha.startswith('Autor:'):
                    arquivo.write(f"Autor: {novo_autor}\n")
                elif skip_lines and linha.startswith('Categoria:'):
                    arquivo.write(f"Categoria: {nova_categoria}\n")
                elif skip_lines and linha.strip() == "":
                    arquivo.write("\n")
                    skip_lines = False
                else:
                    arquivo.write(linha)

        messagebox.showinfo("Sucesso", "Task editada com sucesso!")
        janela_editar.destroy()
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def abrir_janela_editar_task(root, task):
    janela_editar = tk.Toplevel(root)
    janela_editar.title("Editar Task")
    janela_editar.geometry("400x550")
    janela_editar.resizable(False, False)
    janela_editar.configure(bg="#d3d3d3")

    global entry_nome, cmb_prioridade, entry_prazo, entry_autor, cmb_categoria

    lbl_title = tk.Label(janela_editar, text="Editar Task", font=("Arial", 18), bg="#d3d3d3", anchor="w")
    lbl_title.pack(pady=20, padx=20, anchor="w")

    lbl_nome = tk.Label(janela_editar, text="Nome:", bg="#d3d3d3", anchor="w")
    lbl_nome.pack(pady=(10, 5), padx=20, anchor="w")
    entry_nome = tk.Entry(janela_editar, width=40)
    entry_nome.insert(0, task["task"])
    entry_nome.pack(padx=20, pady=5)

    lbl_prioridade = tk.Label(janela_editar, text="Prioridade:", bg="#d3d3d3", anchor="w")
    lbl_prioridade.pack(pady=(10, 5), padx=20, anchor="w")
    cmb_prioridade = ttk.Combobox(janela_editar, values=["Baixa", "Média", "Alta"])
    cmb_prioridade.set(task["prioridade"])
    cmb_prioridade.pack(padx=20, pady=5)

    lbl_prazo = tk.Label(janela_editar, text="Prazo:", bg="#d3d3d3", anchor="w")
    lbl_prazo.pack(pady=(10, 5), padx=20, anchor="w")
    entry_prazo = tk.Entry(janela_editar, width=40)
    entry_prazo.insert(0, task["data"])
    entry_prazo.pack(padx=20, pady=5)

    def escolher_data():
            def selecionar_data():
                data_selecionada = cal.get_date()
                prazo_atual = entry_prazo.get().strip()
                entry_prazo.delete(0, tk.END)
                entry_prazo.insert(0, f"{data_selecionada} - {prazo_atual.split(' - ')[-1] if ' - ' in prazo_atual else ''}")
                janela_data.destroy()

            janela_data = tk.Toplevel(janela_editar)
            janela_data.geometry("300x300")
            cal = Calendar(janela_data, selectmode='day')
            cal.pack(pady=20)

            btn_selecionar_data = tk.Button(janela_data, text="Selecionar Data", command=selecionar_data)
            btn_selecionar_data.pack(pady=20)

    def escolher_hora():
        def selecionar_hora(time):
            hora_selecionada = "{}:{} {}".format(*time)
            prazo_atual = entry_prazo.get().strip()
            entry_prazo.delete(0, tk.END)
            entry_prazo.insert(0, f"{prazo_atual.split(' - ')[0] if ' - ' in prazo_atual else prazo_atual} {hora_selecionada}")
            janela_hora.destroy()

        janela_hora = tk.Toplevel(janela_editar)
        time_picker = AnalogPicker(janela_hora, type=constants.HOURS12)
        time_picker.pack(expand=True, fill="both")

        theme = AnalogThemes(time_picker)
        theme.setDracula()

        btn_selecionar_hora = tk.Button(janela_hora, text="Selecionar Hora", command=lambda: selecionar_hora(time_picker.time()))
        btn_selecionar_hora.pack()

    frame_botoes = tk.Frame(janela_editar, bg="#d3d3d3")
    frame_botoes.pack(pady=5)

    btn_escolher_data = tk.Button(frame_botoes, text="Escolher Data", command=escolher_data, bg="#f0f0f0")
    btn_escolher_data.pack(side="left", padx=10)

    btn_escolher_hora = tk.Button(frame_botoes, text="Escolher Hora", command=escolher_hora, bg="#f0f0f0")
    btn_escolher_hora.pack(side="left", padx=10)

    lbl_autor = tk.Label(janela_editar, text="Autor:", bg="#d3d3d3", anchor="w")
    lbl_autor.pack(pady=(10, 5), padx=20, anchor="w")
    entry_autor = tk.Entry(janela_editar, width=40)
    entry_autor.insert(0, task["autor"])
    entry_autor.pack(padx=20, pady=5)

    lbl_categoria = tk.Label(janela_editar, text="Categoria:", bg="#d3d3d3", anchor="w")
    lbl_categoria.pack(pady=(10, 5), padx=20, anchor="w")
    cmb_categoria = ttk.Combobox(janela_editar)
    cmb_categoria.set("Ver categorias")
    cmb_categoria.pack(padx=20, pady=5) 
    
    def atualizar_combobox():
        if janela_editar.winfo_exists(): 
            atualizador.atualizar_categorias()
            cmb_categoria['values'] = atualizador.get_categorias()
            janela_editar.after(2000, atualizar_combobox)  

    atualizador = CategoriaAtualizador()
    atualizar_combobox()


    btn_salvar = tk.Button(janela_editar, text="Salvar Edição", command=lambda: salvar_edicao(task, janela_editar), bg="#f0f0f0")
    btn_salvar.pack(pady=20)
