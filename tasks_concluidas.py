import tkinter as tk
import cria_tasks

tasks_concluidas = []

__all_ = ['tasks_concluidas']

def concluir_task(id):
    task_para_concluir = None
    for task in cria_tasks.tasks:
        if task['id'] == id:
            task_para_concluir = task
            break

    if task_para_concluir:
        tasks_concluidas.append(task_para_concluir)  
        cria_tasks.tasks = [task for task in cria_tasks.tasks if task['id'] != id]  
    else:
        print("Task não encontrada.")

def voltar_task(id):
    global tasks_concluidas
    task_para_voltar = None
    for task in tasks_concluidas:
        if task['id'] == id:
            task_para_voltar = task
            break

    if task_para_voltar:
        cria_tasks.tasks.append(task_para_voltar)  
        tasks_concluidas = [task for task in tasks_concluidas if task['id'] != id]  
    else:
        print("Task não encontrada.")
        
def deletar_task_concluida(task_id):
    global tasks_concluidas
    tasks_concluidas = [task for task in tasks_concluidas if task['id'] != task_id]
    

def buscar_id_por_nome_concluidas(nome_task):
    with open('tasks_concluidas.txt', 'r', encoding="utf-8") as f:
        conteudo = f.read().split('\n\n')  
        for task in conteudo:
            linhas = task.split('\n')
            if len(linhas) >= 2:
                id_ = linhas[0].split(': ')[1]
                nome = linhas[1].split(': ')[1]
                if nome == nome_task:
                    return id_
    for e in tasks_concluidas:
        if e['nome'] == nome_task:
            return e['id']
    return None

    
def carregar_tasks_concluidas():
    try:
        with open('tasks_concluidas.txt', 'r', encoding="utf-8") as f:
            conteudo = f.read().strip()  
            if not conteudo:
                return
            
            tasks = conteudo.split('\n\n')  
            for task in tasks:
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
                    
                    tasks_concluidas.append({
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
    global tasks_concluidas  
    for widget in frame_tasks_concluidas.winfo_children():
        widget.destroy()

    for task in tasks_concluidas:
        frame_task = tk.Frame(frame_tasks_concluidas, bg="#1ebd23", pady=5)
        frame_task.pack(fill=tk.X, padx=5, pady=5)

        lbl_task = tk.Label(frame_task, text=task["nome"], font=("Arial", 12), bg="#1ebd23")
        lbl_task.grid(row=0, column=0, sticky="w", padx=(0, 10))

        lbl_prioridade = tk.Label(frame_task, text=f"Prioridade: {task['prioridade']}", font=("Arial", 10), bg="#1ebd23")
        lbl_prioridade.grid(row=1, column=0, sticky="w", padx=(0, 10))

        lbl_autor = tk.Label(frame_task, text=f"Autor: {task['autor']} - {task['prazo']}", font=("Arial", 10), bg="#1ebd23")
        lbl_autor.grid(row=0, column=1, columnspan=2, sticky="e")

        btn_voltar_task = tk.Button(frame_task, text="Voltar task", command=lambda t=task: voltar_task(buscar_id_por_nome_concluidas(t["nome"])), bg="#cc0a17")
        btn_voltar_task.grid(row=1, column=1, padx=(10, 5), sticky="e")
        
        btn_deletar_task = tk.Button(frame_task, text="Deletar task", command=lambda t=task: deletar_task_concluida(buscar_id_por_nome_concluidas(t["nome"])), bg="#cc0a17")
        btn_deletar_task.grid(row=1, column=2, padx=(10, 5), sticky="e")

    frame_tasks_concluidas.after(5000, update_concluded_tasks)