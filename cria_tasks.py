import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes, constants
import random
import string

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

def gerar_id():
    caracteres = string.ascii_letters + string.digits 
    id_aleatorio = ''.join(random.choice(caracteres) for _ in range(18))
    return id_aleatorio

def criar_task():
    nome_task = entry_nome.get().strip()
    prioridade_task = cmb_prioridade.get()
    prazo_task = entry_prazo.get().strip()
    autor_task = entry_autor.get().strip()
    categoria_task = cmb_categoria.get()  

    if nome_task and prioridade_task != "Selecione a Prioridade" and prazo_task and autor_task:
        with open("tasks.txt", "a") as file:
            file.write(f"Id: {gerar_id()}\n")
            file.write(f"Nome da task: {nome_task}\n")
            file.write(f"Prioridade: {prioridade_task}\n")
            file.write(f"Autor: {autor_task}\n")
            file.write(f"Prazo: {prazo_task}\n")
            file.write(f"Categoria: {categoria_task}\n\n")  
        messagebox.showinfo("Sucesso", "Task criada e salva com sucesso!")
        
        if entry_nome.winfo_exists():
            entry_nome.delete(0, tk.END)
        if cmb_prioridade.winfo_exists():
            cmb_prioridade.set("Selecione a Prioridade")
        if entry_prazo.winfo_exists():
            entry_prazo.delete(0, tk.END)
        if entry_autor.winfo_exists():
            entry_autor.delete(0, tk.END)
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def abrir_janela_nova_task(root):
    janela_nova_task = tk.Toplevel(root)
    janela_nova_task.title("Nova Task")
    janela_nova_task.geometry("400x550")
    janela_nova_task.resizable(False, False)
    janela_nova_task.configure(bg="#d3d3d3")

    lbl_title = tk.Label(janela_nova_task, text="Nova Task", font=("Arial", 18), bg="#d3d3d3", anchor="w")
    lbl_title.pack(pady=20, padx=20, anchor="w")

    lbl_nome = tk.Label(janela_nova_task, text="Nome:", bg="#d3d3d3", anchor="w")
    lbl_nome.pack(pady=(10, 5), padx=20, anchor="w")
    global entry_nome
    entry_nome = tk.Entry(janela_nova_task, width=40)
    entry_nome.pack(padx=20, pady=5)

    lbl_prioridade = tk.Label(janela_nova_task, text="Prioridade:", bg="#d3d3d3", anchor="w")
    lbl_prioridade.pack(pady=(10, 5), padx=20, anchor="w")
    global cmb_prioridade
    cmb_prioridade = ttk.Combobox(janela_nova_task, values=["Baixa", "Media", "Alta"])
    cmb_prioridade.set("Selecione a Prioridade")
    cmb_prioridade.pack(padx=20, pady=5)

    lbl_prazo = tk.Label(janela_nova_task, text="Prazo:", bg="#d3d3d3", anchor="w")
    lbl_prazo.pack(pady=(10, 5), padx=20, anchor="w")
    global entry_prazo
    entry_prazo = tk.Entry(janela_nova_task, width=40)
    entry_prazo.pack(padx=20, pady=5)

    def escolher_data():
        def selecionar_data():
            data_selecionada = cal.get_date()
            prazo_atual = entry_prazo.get().strip()
            entry_prazo.delete(0, tk.END)
            entry_prazo.insert(0, f"{data_selecionada} - {prazo_atual.split(' - ')[-1] if ' - ' in prazo_atual else ''}")
            janela_data.destroy()

        janela_data = tk.Toplevel(janela_nova_task)
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

        janela_hora = tk.Toplevel(janela_nova_task)
        time_picker = AnalogPicker(janela_hora, type=constants.HOURS12)
        time_picker.pack(expand=True, fill="both")

        theme = AnalogThemes(time_picker)
        theme.setDracula()

        btn_selecionar_hora = tk.Button(janela_hora, text="Selecionar Hora", command=lambda: selecionar_hora(time_picker.time()))
        btn_selecionar_hora.pack()

    frame_botoes = tk.Frame(janela_nova_task, bg="#d3d3d3")
    frame_botoes.pack(pady=5)

    btn_escolher_data = tk.Button(frame_botoes, text="Escolher Data", command=escolher_data, bg="#f0f0f0")
    btn_escolher_data.pack(side="left", padx=10)

    btn_escolher_hora = tk.Button(frame_botoes, text="Escolher Hora", command=escolher_hora, bg="#f0f0f0")
    btn_escolher_hora.pack(side="left", padx=10)

    lbl_autor = tk.Label(janela_nova_task, text="Autor:", bg="#d3d3d3", anchor="w")
    lbl_autor.pack(pady=(10, 5), padx=20, anchor="w")
    global entry_autor
    entry_autor = tk.Entry(janela_nova_task, width=40)
    entry_autor.pack(padx=20, pady=5)
    entry_autor.insert(0, "Digite seu nome")

    lbl_categoria = tk.Label(janela_nova_task, text="Categoria:", bg="#d3d3d3", anchor="w")
    lbl_categoria.pack(pady=(10, 5), padx=20, anchor="w")

    global cmb_categoria
    cmb_categoria = ttk.Combobox(janela_nova_task)
    cmb_categoria.set("Ver categorias")
    cmb_categoria.pack(padx=20, pady=5) 

    def atualizar_combobox():
        if janela_nova_task.winfo_exists(): 
            atualizador.atualizar_categorias()
            cmb_categoria['values'] = atualizador.get_categorias()
            janela_nova_task.after(2000, atualizar_combobox)  

    atualizador = CategoriaAtualizador()
    atualizar_combobox()

    btn_criar = tk.Button(janela_nova_task, text="Criar Task", command=criar_task, bg="#f0f0f0")
    btn_criar.pack(pady=20)
