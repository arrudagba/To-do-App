import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import string

categorias = [{"id": "0", "nome": "All"}]  

__all__ = ['categorias']

def carregar_categorias():
    try:
        with open('categorias.txt', 'r', encoding="utf-8") as f:
            conteudo = f.read().strip()  
            if not conteudo:
                return
            
            categorias_arq = conteudo.split('\n\n')  
            for categoria in categorias_arq:
                linhas = categoria.split('\n')
                
                try:
                    id_ = linhas[0].split(': ')[1]
                    nome = linhas[1].split(': ')[1]
                    
                    if nome == "All" and any(cat['nome'] == "All" for cat in categorias):
                        continue  
                    
                    categorias.append({
                        'id': id_,
                        'nome': nome,
                    })
                except IndexError:
                    print("Erro ao processar dados de uma categoria. Ignorando esta entrada.")
                    continue

    except FileNotFoundError:
        return 


def gerar_id():
    caracteres = string.ascii_letters + string.digits
    id_aleatorio = ''.join(random.choice(caracteres) for _ in range(18))
    return id_aleatorio

def cria_categorias(nome_categoria):
    global categorias
    categoria = {
        "id": gerar_id(),
        "nome": nome_categoria
    }
    categorias.append(categoria)

def buscar_id_por_nome(nome_categoria):
    for e in categorias:
        if e['nome'] == nome_categoria:
            return e['id']
    return None

def atualizar_lista_categorias(listbox):
    global categorias
    listbox.delete(0, tk.END)
    for categoria in categorias:
        if categoria['nome'] != "All":
            listbox.insert(tk.END, categoria['nome'])

def adicionar_categoria(janela_gerenciar):
    global categorias
    nova_categoria = simpledialog.askstring("Adicionar Categoria", "Digite o nome da nova categoria:")
    if nova_categoria and nova_categoria.strip() != "":
        cria_categorias(nova_categoria.strip())
        atualizar_lista_categorias(listbox_categorias)
    else:
        messagebox.showwarning("Erro", "Por favor, digite um nome válido para a categoria.")

def remover_categoria(janela_gerenciar):
    global categorias
    selecionado = listbox_categorias.curselection()
    if selecionado:
        nome_categoria = listbox_categorias.get(selecionado)
        categoria_id = buscar_id_por_nome(nome_categoria)
        categorias = [categoria for categoria in categorias if categoria['id'] != categoria_id]
        atualizar_lista_categorias(listbox_categorias)
    else:
        messagebox.showwarning("Erro", "Por favor, selecione uma categoria para remover.")

def abrir_janela_gerenciar_categorias(root):
    janela_gerenciar = tk.Toplevel(root)
    janela_gerenciar.title("Gerenciar Categorias")
    janela_gerenciar.geometry("400x500")
    janela_gerenciar.resizable(False, False)
    janela_gerenciar.configure(bg="#d3d3d3")

    global listbox_categorias

    lbl_title = tk.Label(janela_gerenciar, text="Gerenciar Categorias", font=("Arial", 18), bg="#d3d3d3", anchor="w")
    lbl_title.pack(pady=20, padx=20, anchor="w")

    listbox_categorias = tk.Listbox(janela_gerenciar, selectmode=tk.SINGLE, bg="#f0f0f0", width=40, height=15)
    listbox_categorias.pack(padx=20, pady=10)
    atualizar_lista_categorias(listbox_categorias)

    btn_adicionar = tk.Button(janela_gerenciar, text="Adicionar Categoria", command=lambda: adicionar_categoria(janela_gerenciar), bg="#f0f0f0")
    btn_adicionar.pack(pady=10)

    btn_remover = tk.Button(janela_gerenciar, text="Remover Categoria", command=lambda: remover_categoria(janela_gerenciar), bg="#f0f0f0")
    btn_remover.pack(pady=10)