import tkinter as tk

def deletar_task_concluida(task):
    id = task.get("id")
    with open("tasks_concluidas.txt", 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    with open("tasks_concluidas.txt", 'w', encoding='utf-8') as arquivo:
        skip_lines = False
        for linha in linhas:
            if linha.startswith('Id: '):
                current_id = linha.strip().split(': ', 1)[1]
                skip_lines = current_id == id
            if not skip_lines:
                arquivo.write(linha)
                
    update_concluded_tasks()

def abrir_janela_concluidas(root):
    janela_concluidas = tk.Toplevel(root)
    janela_concluidas.title("Tasks Concluídas")
    janela_concluidas.geometry("500x600")
    janela_concluidas.resizable(False, False)
    janela_concluidas.configure(bg="#d3d3d3")

    global frame_tasks_concluidas
    frame_tasks_concluidas = tk.Frame(janela_concluidas, bg="white", bd=1, relief=tk.SOLID)
    frame_tasks_concluidas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    update_concluded_tasks()

def update_concluded_tasks():
    for widget in frame_tasks_concluidas.winfo_children():
        widget.destroy()

    tasks = []
    try:
        with open("tasks_concluidas.txt", "r") as file:
            task = {}
            for line in file:
                if line.startswith("Id:"):
                    task = {"id": line.split(":")[1].strip()}
                elif line.startswith("Nome da task:"):
                    task["task"] = line.split(":")[1].strip()
                elif line.startswith("Prioridade:"):
                    task["prioridade"] = line.split(":")[1].strip()
                elif line.startswith("Autor:"):
                    task["autor"] = line.split(":")[1].strip()
                elif line.startswith("Prazo:"):
                    task["data"] = line.split(":")[1].strip()
                    tasks.append(task)
                    task = {}
    except FileNotFoundError:
        pass

    for task in tasks:
        frame_task = tk.Frame(frame_tasks_concluidas, bg="#1ebd23", pady=5)
        frame_task.pack(fill=tk.X, padx=5, pady=5)

        lbl_task = tk.Label(frame_task, text=task["task"], font=("Arial", 12), bg="#1ebd23")
        lbl_task.grid(row=0, column=0, sticky="w", padx=(0, 10))

        lbl_prioridade = tk.Label(frame_task, text=f"Prioridade: {task['prioridade']}", font=("Arial", 10), bg="#1ebd23")
        lbl_prioridade.grid(row=1, column=0, sticky="w", padx=(0, 10))

        lbl_autor = tk.Label(frame_task, text=f"Autor: {task['autor']} - {task['data']}", font=("Arial", 10), bg="#1ebd23")
        lbl_autor.grid(row=0, column=1, columnspan=2, sticky="e")

        btn_voltar_task = tk.Button(frame_task, text="Voltar task", command=lambda t=task: voltar_task_concluida(t), bg="#cc0a17")
        btn_voltar_task.grid(row=1, column=1, padx=(10, 5), sticky="e")
        
        btn_deletar_task = tk.Button(frame_task, text="Deletar task", command=lambda t=task: deletar_task_concluida(t), bg="#cc0a17")
        btn_deletar_task.grid(row=1, column=2, padx=(10, 5), sticky="e")

    frame_tasks_concluidas.after(5000, update_concluded_tasks)

def voltar_task_concluida(task):
    id = task.get("id")
    task_data = []

    with open('tasks_concluidas.txt', 'r') as file:
        tasks = file.readlines()

    with open('tasks_concluidas.txt', 'w') as file:
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

    with open('tasks.txt', 'a') as file:
        for linha in task_data:
            file.write(linha)

    update_concluded_tasks()


def atualizar_tasks_no_main():
    import main
    main.atualizar_tasks()

