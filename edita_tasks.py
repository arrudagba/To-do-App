import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes, constants
import cria_tasks
import gerencia_categorias

def editar_task(id, janela_editar):
    task_para_editar = None
    for task in cria_tasks.tasks:
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
    for e in cria_tasks.tasks:
        if e['nome'] == nome_task:
            return e['id']
    return None
       
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
