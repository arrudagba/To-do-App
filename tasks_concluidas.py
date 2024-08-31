import tkinter as tk

def abrir_janela_concluidas(root):
    janela_concluidas = tk.Toplevel(root)
    janela_concluidas.title("Tasks Concluídas")
    janela_concluidas.geometry("500x600")
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
                if line.startswith("Nome da task:"):
                    if task:
                        tasks.append(task)
                    task = {"task": line.split(":")[1].strip()}
                elif line.startswith("Prioridade:"):
                    task["prioridade"] = line.split(":")[1].strip()
                elif line.startswith("Autor:"):
                    task["autor"] = line.split(":")[1].strip()
                elif line.startswith("Prazo:"):
                    task["data"] = line.split(":")[1].strip()
            if task:
                tasks.append(task)
    except FileNotFoundError:
        pass

    for task in tasks:
        frame_task = tk.Frame(frame_tasks_concluidas, bg="lightgreen", pady=5)
        frame_task.pack(fill=tk.X, padx=5, pady=5)

        lbl_task = tk.Label(frame_task, text=task["task"], font=("Arial", 12), bg="lightgreen")
        lbl_task.grid(row=0, column=0, sticky="w", padx=(0, 10))

        lbl_prioridade = tk.Label(frame_task, text=f"Prioridade: {task['prioridade']}", font=("Arial", 10), bg="lightgreen")
        lbl_prioridade.grid(row=1, column=0, sticky="w", padx=(0, 10))

        lbl_autor = tk.Label(frame_task, text=f"Autor: {task['autor']} - {task['data']}", font=("Arial", 10), bg="lightgreen")
        lbl_autor.grid(row=0, column=1, columnspan=2, sticky="e")

        btn_voltar = tk.Button(frame_task, text="Voltar task", command=lambda t=task: voltar_task(t), bg="lightgreen")
        btn_voltar.grid(row=1, column=1, padx=(10, 5), sticky="e")

        btn_deletar = tk.Button(frame_task, text="Deletar a task", command=lambda t=task: deletar_task_concluida(t), bg="lightgreen")
        btn_deletar.grid(row=1, column=2, padx=(5, 0), sticky="e")

def voltar_task(task):
    with open("tasks_concluidas.txt", "r") as file:
        lines = file.readlines()

    with open("tasks_concluidas.txt", "w") as file:
        for line in lines:
            if line.strip("\n") != f"Nome da task: {task['task']}":
                file.write(line)

    with open("tasks.txt", "a") as file:
        file.write(f"Nome da task: {task['task']}\n")
        file.write(f"Prioridade: {task['prioridade']}\n")
        file.write(f"Autor: {task['autor']}\n")
        file.write(f"Prazo: {task['data']}\n")
        file.write("\n")

    update_concluded_tasks()
    atualizar_tasks_no_main()

def deletar_task_concluida(task):
    with open("tasks_concluidas.txt", "r") as file:
        lines = file.readlines()

    with open("tasks_concluidas.txt", "w") as file:
        for line in lines:
            if line.strip("\n") != f"Nome da task: {task['task']}":
                file.write(line)

    update_concluded_tasks()

def atualizar_tasks_no_main():
    import main
    main.atualizar_tasks()

