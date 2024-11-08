import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import string

__all__ = ['abrir_janela_gerenciar_categorias']

categorias = []

def gerar_id():
    caracteres = string.ascii_letters + string.digits
    id_aleatorio = ''.join(random.choice(caracteres) for _ in range(18))
    return id_aleatorio

def atualizar_lista_categorias(listbox):
    listbox.delete(0, tk.END)
    categorias = listar_categorias()[1:]
    for categoria in categorias:
        listbox.insert(tk.END, categoria)

def cria_categoria(nome_categoria):
    with open("categorias.txt", "a", encoding="utf-8") as file:
        file.write(f"Id: {gerar_id()}\n")
        file.write(f"Nome: {nome_categoria}\n\n")

def deleta_categoria(id_categoria):
    with open("categorias.txt", 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    with open("categorias.txt", 'w', encoding='utf-8') as arquivo:
        skip_lines = False
        for linha in linhas:
            if linha.startswith('Id: '):
                current_id = linha.strip().split(': ', 1)[1]
                skip_lines = current_id == id_categoria
            if not skip_lines:
                arquivo.write(linha)

def deletar_categoria_por_nome(nome_categoria):
    id_categoria = None
    linha_anterior = None  

    with open("categorias.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Nome:") and line.strip().split(': ', 1)[1] == nome_categoria:
                if linha_anterior and linha_anterior.startswith("Id:"):
                    id_categoria = linha_anterior.strip().split("Id: ", 1)[1]
                break
            linha_anterior = line  

    if id_categoria:
        deleta_categoria(id_categoria)
        messagebox.showinfo("Sucesso", f"Categoria '{nome_categoria}' deletada com sucesso!")
    else:
        messagebox.showerror("Erro", "Categoria não encontrada.")


def listar_categorias():
    categorias = ["All"]
    with open("categorias.txt", "r", encoding="utf-8") as file:
        categoria = {}
        for line in file:
            if line.startswith("Id:"):
                categoria = {"id": line.split("Id:")[1].strip()}
            elif line.startswith("Nome:"):
                categoria["nome"] = line.split("Nome:")[1].strip()
                categorias.append(categoria["nome"])
    return categorias

def adicionar_categoria(janela_gerenciar):
    nova_categoria = simpledialog.askstring("Adicionar Categoria", "Digite o nome da nova categoria:")
    if nova_categoria and nova_categoria.strip() != "":
        categorias.append(nova_categoria.strip())
        cria_categoria(nova_categoria.strip())
        atualizar_lista_categorias(listbox_categorias)
    else:
        messagebox.showwarning("Erro", "Por favor, digite um nome válido para a categoria.")

def remover_categoria(janela_gerenciar):
    selecionado = listbox_categorias.curselection()
    if selecionado:
        categoria = listbox_categorias.get(selecionado)
        categorias = listar_categorias()[1:]
        categorias.remove(categoria)
        deletar_categoria_por_nome(categoria)
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
