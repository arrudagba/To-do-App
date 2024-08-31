import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def criar_task():
    nome_task = entry_nome.get().strip()
    prioridade_task = cmb_prioridade.get()
    prazo_task = entry_prazo.get().strip()
    autor_task = entry_autor.get().strip()

    if nome_task and prioridade_task != "Selecione a Prioridade" and prazo_task and autor_task:
        with open("tasks.txt", "a") as file:
            file.write(f"Nome da task: {nome_task}\n")
            file.write(f"Prioridade: {prioridade_task}\n")
            file.write(f"Autor: {autor_task}\n")
            file.write(f"Prazo: {prazo_task}\n\n")
        messagebox.showinfo("Sucesso", "Task criada e salva com sucesso!")
        entry_nome.delete(0, tk.END)
        cmb_prioridade.set("Selecione a Prioridade")
        entry_prazo.delete(0, tk.END)
        entry_autor.delete(0, tk.END)
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def abrir_janela_nova_task(root):
    janela_nova_task = tk.Toplevel(root)
    janela_nova_task.title("Nova Task")
    janela_nova_task.geometry("400x500")
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
    cmb_prioridade = ttk.Combobox(janela_nova_task, values=["Alta", "Média", "Baixa"], state="readonly")
    cmb_prioridade.set("Selecione a Prioridade")
    cmb_prioridade.pack(padx=20, pady=5)

    lbl_prazo = tk.Label(janela_nova_task, text="Prazo:", bg="#d3d3d3", anchor="w")
    lbl_prazo.pack(pady=(10, 5), padx=20, anchor="w")
    global entry_prazo
    entry_prazo = tk.Entry(janela_nova_task, width=40)
    entry_prazo.pack(padx=20, pady=5)
    entry_prazo.insert(0, "Escreva o prazo em dd/mm/aaaa - hh:mm")

    lbl_autor = tk.Label(janela_nova_task, text="Dono da Task:", bg="#d3d3d3", anchor="w")
    lbl_autor.pack(pady=(10, 5), padx=20, anchor="w")
    global entry_autor
    entry_autor = tk.Entry(janela_nova_task, width=40)
    entry_autor.pack(padx=20, pady=5)
    entry_autor.insert(0, "Digite seu nome")

    btn_criar_task = tk.Button(janela_nova_task, text="Criar task", command=criar_task, bg="#f0f0f0", width=15, height=2)
    btn_criar_task.pack(pady=30, padx=20)

    janela_nova_task.mainloop()

