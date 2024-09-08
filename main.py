import tkinter as tk
from tkinter import ttk
import cria_tasks
import tasks_concluidas
import gerencia_categorias  
import edita_tasks

categoria = "All"  

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

root = tk.Tk()
root.title("To-Do App")
root.geometry("1024x715")
root.resizable(False, False)
root.configure(bg="#d3d3d3")  

def nova_task():
    cria_tasks.abrir_janela_nova_task(root)

def ver_tasks_concluidas():
    tasks_concluidas.abrir_janela_concluidas(root)

def criar_categoria():
    gerencia_categorias.abrir_janela_gerenciar_categorias(root)  

def editar_task(task):
    edita_tasks.abrir_janela_editar_task(root, task)  

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

    atualizar_tasks(categoria)

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
                else:
                    file.write(linha)
            elif skip_lines:
                task_data.append(linha)
            else:
                file.write(linha)

    with open('tasks_concluidas.txt', 'a') as file:
        for linha in task_data:
            file.write(linha)

    atualizar_tasks(categoria)

def atualizar_tasks(categoria):
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
            elif line.startswith("Categoria:"):
                task["categoria"] = line.split("Categoria:")[1].strip()
                tasks.append(task)
                task = {}

    prioridades_ordem = {"Alta": 1, "Media": 2, "Baixa": 3}

    tasks.sort(key=lambda t: prioridades_ordem.get(t["prioridade"], 3)) 

    for task in tasks:
        if categoria == "All" or task['categoria'] == categoria:
            frame_task = tk.Frame(frame_tasks, bg="#f0f0f0", pady=5)
            frame_task.pack(fill=tk.X, padx=5, pady=5)

            lbl_task = tk.Label(frame_task, text=task["task"], font=("Arial", 12), bg="#f0f0f0")
            lbl_task.grid(row=0, column=0, sticky="w", padx=(0, 10))

            lbl_prioridade = tk.Label(frame_task, text=f"Prioridade: {task['prioridade']}", font=("Arial", 10), bg="#f0f0f0")
            lbl_prioridade.grid(row=1, column=0, sticky="w", padx=(0, 10))

            if task["prioridade"] == "Alta":
                cor_circulo = "red"
            elif task["prioridade"] == "Media":
                cor_circulo = "yellow"
            else:  
                cor_circulo = "green"

            canvas = tk.Canvas(frame_task, width=20, height=20, bg="#f0f0f0", highlightthickness=0)
            canvas.create_oval(5, 5, 15, 15, fill=cor_circulo, outline="")
            canvas.grid(row=1, column=1, sticky="w", padx=(0, 10))

            lbl_categoria = tk.Label(frame_task, text=f"Categoria: {task['categoria']}", font=("Arial", 10), bg="#f0f0f0")
            lbl_categoria.grid(row=1, column=2, sticky="w", padx=(0, 10))

            lbl_autor = tk.Label(frame_task, text=f"Autor: {task['autor']} - {task['data']}", font=("Arial", 10), bg="#f0f0f0")
            lbl_autor.grid(row=0, column=7, columnspan=2, sticky="e")

            btn_editar = tk.Button(frame_task, text="Editar", command=lambda t=task: editar_task(t), bg="#f0f0f0")
            btn_editar.grid(row=1, column=4, padx=(10, 5), sticky="e")  

            btn_concluir = tk.Button(frame_task, text="Concluir", command=lambda t=task: concluir_task(t), bg="#f0f0f0")
            btn_concluir.grid(row=1, column=5, padx=(10, 5), sticky="e")

            btn_deletar = tk.Button(frame_task, text="Deletar", command=lambda t=task: deletar_task(t), bg="#f0f0f0")
            btn_deletar.grid(row=1, column=6, padx=(5, 0), sticky="e")

frame_top = tk.Frame(root, bg="#d3d3d3")
frame_top.pack(fill=tk.X, padx=20, pady=10)

btn_nova_task = tk.Button(frame_top, text="Nova task", command=nova_task, width=20, bg="#f0f0f0")
btn_nova_task.pack(side=tk.LEFT, padx=(0, 10))

btn_ver_tasks_concluidas = tk.Button(frame_top, text="Ver tasks Concluídas", command=ver_tasks_concluidas, width=20, bg="#f0f0f0")
btn_ver_tasks_concluidas.pack(side=tk.LEFT)

frame_side = tk.Frame(root, bg="#d3d3d3")
frame_side.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=10)

btn_criar_categoria = tk.Button(frame_side, text="Gerenciar Categorias", command=criar_categoria, width=20, bg="#f0f0f0")
btn_criar_categoria.pack(pady=(0, 10))

def atualizar_combobox():
    atualizador.atualizar_categorias()
    cmb_categorias['values'] = atualizador.get_categorias()
    root.after(3000, atualizar_combobox) 

def atualizar_tasks_periodicamente():
    global categoria
    atualizar_tasks(categoria)
    root.after(3000, atualizar_tasks_periodicamente)

def selecionar_categoria(event):
    global categoria
    categoria_selecionada = cmb_categorias.get()
    lbl_categoria.config(text=f"Categoria: {categoria_selecionada}")
    categoria = categoria_selecionada
    atualizar_tasks(categoria)

cmb_categorias = ttk.Combobox(frame_side)
cmb_categorias.set("Ver Categorias")
cmb_categorias.pack(pady=(0, 10))
cmb_categorias.bind("<<ComboboxSelected>>", selecionar_categoria)

frame_main = tk.Frame(root, bg="#d3d3d3")
frame_main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)

lbl_categoria = tk.Label(frame_main, text="Categoria: All", bg="#d3d3d3")
lbl_categoria.pack(anchor="w")

canvas_tasks = tk.Canvas(frame_main, bg="#ffffff")
canvas_tasks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_tasks = tk.Scrollbar(frame_main, orient="vertical", command=canvas_tasks.yview)
scrollbar_tasks.pack(side=tk.RIGHT, fill="y")

canvas_tasks.configure(yscrollcommand=scrollbar_tasks.set)

frame_tasks = tk.Frame(canvas_tasks, bg="#ffffff")
canvas_tasks.create_window((0, 0), window=frame_tasks, anchor="nw")

frame_tasks.bind("<Configure>", lambda e: canvas_tasks.configure(scrollregion=canvas_tasks.bbox("all")))


atualizador = CategoriaAtualizador()
atualizar_combobox()
atualizar_tasks_periodicamente()

root.mainloop()
