import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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
    janela_editar.geometry("400x500")
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

    lbl_autor = tk.Label(janela_editar, text="Autor:", bg="#d3d3d3", anchor="w")
    lbl_autor.pack(pady=(10, 5), padx=20, anchor="w")
    entry_autor = tk.Entry(janela_editar, width=40)
    entry_autor.insert(0, task["autor"])
    entry_autor.pack(padx=20, pady=5)

    lbl_categoria = tk.Label(janela_editar, text="Categoria:", bg="#d3d3d3", anchor="w")
    lbl_categoria.pack(pady=(10, 5), padx=20, anchor="w")
    cmb_categoria = ttk.Combobox(janela_editar, values=["Categoria 1", "Categoria 2", "Categoria 3"])
    cmb_categoria.set("Selecione a Categoria")
    cmb_categoria.set(task.get("categoria", "Selecione a Categoria"))
    cmb_categoria.pack(padx=20, pady=5)

    btn_salvar = tk.Button(janela_editar, text="Salvar Edição", command=lambda: salvar_edicao(task, janela_editar), bg="#f0f0f0")
    btn_salvar.pack(pady=20)
