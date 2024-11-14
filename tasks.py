import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes, constants
import random
import string
import gerencia_categorias

tasks = []

__all__ = ['tasks']

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
        task = {
            "id": gerar_id(),
            "nome": nome_task,
            "prioridade": prioridade_task,
            "autor": autor_task,
            "prazo": prazo_task,
            "categoria": categoria_task
            }
        tasks.append(task)
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


def ver_tasks():
    global tasks
    if not tasks:
        print("Nenhuma task encontrada.")
    else:
        for task in tasks:
            print(f"ID: {task['id']}, Nome: {task['nome']}, Prioridade: {task['prioridade']}, Autor: {task['autor']}, Prazo: {task['prazo']}, Categoria: {task['categoria']}")

def deletar_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    
def buscar_id_por_nome(nome_task):
    with open('tasks.txt', 'r', encoding="utf-8") as f:
        conteudo = f.read().split('\n\n')  
        for task in conteudo:
            linhas = task.split('\n')
            if len(linhas) >= 2:
                id_ = linhas[0].split(': ')[1]
                nome = linhas[1].split(': ')[1]
                if nome == nome_task:
                    return id_
    for e in tasks:
        if e['nome'] == nome_task:
            return e['id']
    return None


def carregar_tasks():
    try:
        with open('tasks.txt', 'r', encoding="utf-8") as f:
            conteudo = f.read().strip()  
            if not conteudo:
                return
            
            tasks_arq = conteudo.split('\n\n')  
            for task in tasks_arq:
                linhas = task.split('\n')
                
                if len(linhas) < 6:
                    print("Dados da task incompletos, ignorando entrada.")
                    continue  
                
                try:
                    id_ = linhas[0].split(': ')[1]
                    nome = linhas[1].split(': ')[1]
                    prioridade = linhas[2].split(': ')[1]
                    autor = linhas[3].split(': ')[1]
                    prazo = linhas[4].split(': ')[1]
                    categoria = linhas[5].split(': ')[1]
                    
                    tasks.append({
                        'id': id_,
                        'nome': nome,
                        'prioridade': prioridade,
                        'autor': autor,
                        'prazo': prazo,
                        'categoria': categoria
                    })
                except IndexError:
                    print("Erro ao processar dados de uma task. Ignorando esta entrada.")
                    continue

    except FileNotFoundError:
        return 
    

def editar_task(id, janela_editar):
    global tasks
    task_para_editar = None
    for task in tasks:
        if task['id'] == id:
            task_para_editar = task
            break

    if task_para_editar:
        novo_nome = entry_nome.get().strip()
        nova_prioridade = cmb_prioridade.get()
        novo_prazo = entry_prazo.get().strip()
        novo_autor = entry_autor.get().strip()
        nova_categoria = cmb_categoria.get().strip()

        if novo_nome and nova_prioridade != "Selecione a Prioridade" and novo_prazo and novo_autor:
            task_para_editar['nome'] = novo_nome
            task_para_editar['prioridade'] = nova_prioridade
            task_para_editar['prazo'] = novo_prazo
            task_para_editar['autor'] = novo_autor
            task_para_editar['categoria'] = nova_categoria

            messagebox.showinfo("Sucesso", "Task editada com sucesso!")
            janela_editar.destroy()
        else:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

    else:
        print("Task não encontrada.")
    
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
    cmb_prioridade = ttk.Combobox(janela_nova_task, values=["Baixa", "Média", "Alta"])
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
            nomes_categorias = [categoria["nome"] for categoria in gerencia_categorias.categorias]
            cmb_categoria['values'] = nomes_categorias
            janela_nova_task.after(2000, atualizar_combobox)  

    atualizar_combobox()

    btn_criar = tk.Button(janela_nova_task, text="Criar Task", command=criar_task, bg="#f0f0f0")
    btn_criar.pack(pady=20)
    
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
    entry_nome.insert(0, task["nome"])
    entry_nome.pack(padx=20, pady=5)

    lbl_prioridade = tk.Label(janela_editar, text="Prioridade:", bg="#d3d3d3", anchor="w")
    lbl_prioridade.pack(pady=(10, 5), padx=20, anchor="w")
    cmb_prioridade = ttk.Combobox(janela_editar, values=["Baixa", "Média", "Alta"])
    cmb_prioridade.set(task["prioridade"])
    cmb_prioridade.pack(padx=20, pady=5)

    lbl_prazo = tk.Label(janela_editar, text="Prazo:", bg="#d3d3d3", anchor="w")
    lbl_prazo.pack(pady=(10, 5), padx=20, anchor="w")
    entry_prazo = tk.Entry(janela_editar, width=40)
    entry_prazo.insert(0, task["prazo"])
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
            nomes_categorias = [categoria["nome"] for categoria in gerencia_categorias.categorias] 
            cmb_categoria['values'] = nomes_categorias
            janela_editar.after(2000, atualizar_combobox)  

    atualizar_combobox()


    btn_salvar = tk.Button(janela_editar, text="Salvar Edição", command=lambda: editar_task(buscar_id_por_nome(task["nome"]), janela_editar), bg="#f0f0f0")
    btn_salvar.pack(pady=20)
 