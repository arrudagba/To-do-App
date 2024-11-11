import tkinter as tk
from tkinter import ttk
import cria_tasks
import tasks_concluidas
import edita_tasks
import gerencia_categorias

categoria = "All"  

def salvar_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as file:
        for e in cria_tasks.tasks:
            file.write(f"Id: {e['id']}\n")
            file.write(f"Nome da task: {e['nome']}\n")
            file.write(f"Prioridade: {e['prioridade']}\n")
            file.write(f"Autor: {e['autor']}\n")
            file.write(f"Prazo: {e['prazo']}\n")
            file.write(f"Categoria: {e['categoria']}\n\n")
            
    with open("tasks_concluidas.txt", "w", encoding="utf-8") as file:
        for e in tasks_concluidas.tasks_concluidas:
            file.write(f"Id: {e['id']}\n")
            file.write(f"Nome da task: {e['nome']}\n")
            file.write(f"Prioridade: {e['prioridade']}\n")
            file.write(f"Autor: {e['autor']}\n")
            file.write(f"Prazo: {e['prazo']}\n")
            file.write(f"Categoria: {e['categoria']}\n\n")
    
    with open("categorias.txt", "w", encoding="utf-8") as file:
        for e in gerencia_categorias.categorias:
            file.write(f"Id: {e['id']}\n")
            file.write(f"Nome da categoria: {e['nome']}\n\n")

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

def atualizar_tasks(categoria):
    for widget in frame_tasks.winfo_children():
        widget.destroy()

    
    prioridades_ordem = {"Alta": 1, "Media": 2, "Baixa": 3}

    cria_tasks.tasks.sort(key=lambda t: prioridades_ordem.get(t["prioridade"], 3)) 

    for task in cria_tasks.tasks:
        if categoria == "All" or task['categoria'] == categoria:
            frame_task = tk.Frame(frame_tasks, bg="#f0f0f0", pady=5)
            frame_task.pack(fill=tk.X, padx=5, pady=5)

            lbl_task = tk.Label(frame_task, text=task["nome"], font=("Arial", 12), bg="#f0f0f0")
            lbl_task.grid(row=0, column=0, sticky="w", padx=(0, 10))

            lbl_prioridade = tk.Label(frame_task, text=f"Prioridade: {task['prioridade']}", font=("Arial", 10), bg="#f0f0f0")
            lbl_prioridade.grid(row=1, column=0, sticky="w", padx=(0, 10))

            if task["prioridade"] == "Alta":
                cor_circulo = "red"
            elif task["prioridade"] == "Média":
                cor_circulo = "yellow"
            else:  
                cor_circulo = "green"

            canvas = tk.Canvas(frame_task, width=20, height=20, bg="#f0f0f0", highlightthickness=0)
            canvas.create_oval(5, 5, 15, 15, fill=cor_circulo, outline="")
            canvas.grid(row=1, column=1, sticky="w", padx=(0, 10))

            lbl_categoria = tk.Label(frame_task, text=f"Categoria: {task['categoria']}", font=("Arial", 10), bg="#f0f0f0")
            lbl_categoria.grid(row=1, column=2, sticky="w", padx=(0, 10))

            lbl_autor = tk.Label(frame_task, text=f"Autor: {task['autor']} - {task['prazo']}", font=("Arial", 10), bg="#f0f0f0")
            lbl_autor.grid(row=0, column=6, columnspan=4, sticky="e")

            btn_editar = tk.Button(frame_task, text="Editar", command=lambda t=task: editar_task(t), bg="#f0f0f0")
            btn_editar.grid(row=1, column=4, padx=(10, 5), sticky="e")  

            btn_concluir = tk.Button(frame_task, text="Concluir", command=lambda t=task: tasks_concluidas.concluir_task(cria_tasks.buscar_id_por_nome(t["nome"])), bg="#f0f0f0")
            btn_concluir.grid(row=1, column=5, padx=(10, 5), sticky="e")

            btn_deletar = tk.Button(frame_task, text="Deletar", command=lambda t=task: cria_tasks.deletar_task(cria_tasks.buscar_id_por_nome(t["nome"])), bg="#f0f0f0")
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
    nomes_categorias = [categoria["nome"] for categoria in gerencia_categorias.categorias]
    cmb_categorias['values'] = nomes_categorias
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



if __name__ == "__main__":
    cria_tasks.carregar_tasks()
    tasks_concluidas.carregar_tasks_concluidas()
    gerencia_categorias.carregar_categorias()
    atualizar_combobox()
    atualizar_tasks_periodicamente()

    root.mainloop()
    salvar_tasks()