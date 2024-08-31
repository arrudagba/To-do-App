import tkinter as tk
from tkinter import simpledialog, messagebox

categorias = ["Categoria 1", "Categoria 2", "Categoria 3"]

def atualizar_lista_categorias(listbox):
    listbox.delete(0, tk.END)
    for categoria in categorias:
        listbox.insert(tk.END, categoria)

def adicionar_categoria(janela_gerenciar):
    nova_categoria = simpledialog.askstring("Adicionar Categoria", "Digite o nome da nova categoria:")
    if nova_categoria and nova_categoria.strip() != "":
        categorias.append(nova_categoria.strip())
        atualizar_lista_categorias(listbox_categorias)
    else:
        messagebox.showwarning("Erro", "Por favor, digite um nome válido para a categoria.")

def remover_categoria(janela_gerenciar):
    selecionado = listbox_categorias.curselection()
    if selecionado:
        categoria = listbox_categorias.get(selecionado)
        categorias.remove(categoria)
        atualizar_lista_categorias(listbox_categorias)
    else:
        messagebox.showwarning("Erro", "Por favor, selecione uma categoria para remover.")

def abrir_janela_gerenciar_categorias(root):
    janela_gerenciar = tk.Toplevel(root)
    janela_gerenciar.title("Gerenciar Categorias")
    janela_gerenciar.geometry("400x500")
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
