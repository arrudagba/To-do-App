import tkinter as tk
from tkinter import ttk
import cria_tasks
import tasks_concluidas

root = tk.Tk()
root.title("To-Do App")
root.geometry("1024x715")
root.configure(bg="#d3d3d3")  

def nova_task():
    cria_tasks.abrir_janela_nova_task(root)

def ver_tasks_concluidas():
    tasks_concluidas.abrir_janela_concluidas(root)

def criar_categoria():
    print("Criar categoria")

def ver_categorias():
    print("Ver categorias")

def deletar_task(task):
    id = task.get("id")
    with open("tasks.txt", 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    with open("tasks.txt", 'w', encoding='utf-8') as arquivo:
        skip_lines = False
        for linha in linhas:
            if linha.startswith('Id: '):
                current_id = linha.strip().split(': ', 1)[1]
                skip_lines = current_id == id
            if not skip_lines:
                arquivo.write(linha)

    atualizar_tasks()

def concluir_task(task):
    id = task.get("id")
    task_data = []
    
    with open('tasks.txt', 'r') as file:
        tasks = file.readlines()

    with open('tasks.txt', 'w') as file:
        skip_lines = False
        for linha in tasks:
            if linha.startswith('Id: '):
                current_id = linha.strip().split(': ', 1)[1]
                skip_lines = current_id == id
                if skip_lines:
                    task_data.append(linha)
            elif skip_lines:
                task_data.append(linha)
            else:
                file.write(linha)

    with open('tasks_concluidas.txt', 'a') as file:
        for linha in task_data:
            file.write(linha)

    atualizar_tasks()

def atualizar_tasks():
    for widget in frame_tasks.winfo_children():
        widget.destroy()

    tasks = []
    with open("tasks.txt", "r") as file:
        task = {}
        for line in file:
            if line.startswith("Id:"):
                task = {"id": line.split("Id:")[1].strip()}
            elif line.startswith("Nome da task:"):
                task["task"] = line.split("Nome da task:")[1].strip()
            elif line.startswith("Prioridade:"):
                task["prioridade"] = line.split("Prioridade:")[1].strip()
            elif line.startswith("Autor:"):
                task["autor"] = line.split("Autor:")[1].strip()
            elif line.startswith("Prazo:"):
                task["data"] = line.split("Prazo:")[1].strip()
                tasks.append(task)
                task = {}

    for task in tasks:
        frame_task = tk.Frame(frame_tasks, bg="#f0f0f0", pady=5)
        frame_task.pack(fill=tk.X, padx=5, pady=5)

        lbl_task = tk.Label(frame_task, text=task["task"], font=("Arial", 12), bg="#f0f0f0")
        lbl_task.grid(row=0, column=0, sticky="w", padx=(0, 10))

        lbl_prioridade = tk.Label(frame_task, text=f"Prioridade: {task['prioridade']}", font=("Arial", 10), bg="#f0f0f0")
        lbl_prioridade.grid(row=1, column=0, sticky="w", padx=(0, 10))

        lbl_autor = tk.Label(frame_task, text=f"Autor: {task['autor']} - {task['data']}", font=("Arial", 10), bg="#f0f0f0")
        lbl_autor.grid(row=0, column=1, columnspan=2, sticky="e")

        btn_concluir = tk.Button(frame_task, text="Concluir", command=lambda t=task: concluir_task(t), bg="#f0f0f0")
        btn_concluir.grid(row=1, column=1, padx=(10, 5), sticky="e")

        btn_deletar = tk.Button(frame_task, text="Deletar", command=lambda t=task: deletar_task(t), bg="#f0f0f0")
        btn_deletar.grid(row=1, column=2, padx=(5, 0), sticky="e")

    root.after(3000, atualizar_tasks)

frame_top = tk.Frame(root, bg="#d3d3d3")
frame_top.pack(fill=tk.X, padx=20, pady=10)

btn_nova_task = tk.Button(frame_top, text="Nova task", command=nova_task, width=20, bg="#f0f0f0")
btn_nova_task.pack(side=tk.LEFT, padx=(0, 10))

btn_ver_tasks_concluidas = tk.Button(frame_top, text="Ver tasks Concluídas", command=ver_tasks_concluidas, width=20, bg="#f0f0f0")
btn_ver_tasks_concluidas.pack(side=tk.LEFT)

frame_side = tk.Frame(root, bg="#d3d3d3")
frame_side.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=10)

btn_criar_categoria = tk.Button(frame_side, text="Criar Categoria", command=criar_categoria, width=20, bg="#f0f0f0")
btn_criar_categoria.pack(pady=(0, 10))

cmb_categorias = ttk.Combobox(frame_side, values=["All", "Categoria 1", "Categoria 2"])
cmb_categorias.set("Ver categorias")
cmb_categorias.pack()

frame_main = tk.Frame(root, bg="#d3d3d3")
frame_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

lbl_categoria = tk.Label(frame_main, text="Categoria: All", anchor="w", bg="#d3d3d3")
lbl_categoria.pack(fill=tk.X, pady=(0, 5))

frame_tasks = tk.Frame(frame_main, bg="white", bd=1, relief=tk.SOLID)
frame_tasks.pack(fill=tk.BOTH, expand=True)

atualizar_tasks()

root.mainloop()

