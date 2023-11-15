import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Inicialize o Firebase
import os
os.chdir("C:/Users/rafae/OneDrive/Documentos/projetoescola/myenv/Include/")
escola = credentials.Certificate("cred.json")
firebase_admin.initialize_app(escola, {
    'databaseURL': 'https://escola-4c1a5-default-rtdb.firebaseio.com/'
})

# Função para cadastrar um aluno no Firebase
def cadastrar_aluno():
    estudante = entry_estudante.get()
    curso = entry_curso.get()
    idade = entry_idade.get()

    # Referência ao banco de dados do Firebase
    ref = db.reference('/escola')
    
    novo_aluno = {
        'estudante': estudante,
        'curso': curso,
        'idade': idade
    }

    try:
        ref.push().set(novo_aluno)
        messagebox.showinfo("Cadastro de aluno", "aluno cadastrado com sucesso.")
        # Limpa os campos de entrada após o cadastro
        entry_estudante.delete(0, tk.END)
        entry_curso.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar aluno: {str(e)}")

# Função para exibir os alunos cadastrados
def exibir_alunos():
    ref = db.reference('/escola')
    alunos = ref.get()
    
    # Limpa a Treeview antes de exibir os dados
    for item in tree.get_children():
        tree.delete(item)
    
    if alunos:
        for aluno_id, aluno_info in alunos.items():
            estudante = aluno_info.get('estudante', 'Desconhecido')
            curso = aluno_info.get('curso', 'Desconhecido')
            idade = aluno_info.get('idade', 'Desconhecido')
            tree.insert('', 'end', values=(estudante, curso, idade, aluno_id))

# Função para excluir um aluno
def excluir_aluno():
    selected_item = tree.selection()
    if selected_item:
        aluno_id = tree.item(selected_item, 'values')[-1]  # Obtém o ID do aluno
        ref = db.reference(f'/escola/{aluno_id}')
        ref.delete()
        exibir_alunos()  # Atualiza a exibição da tabela

# Função para editar um aluno
def editar_aluno():
    selected_item = tree.selection()
    if selected_item:
        aluno_id = tree.item(selected_item, 'values')[-1]  # Obtém o ID do aluno
        estudante = entry_estudante.get()
        curso = entry_curso.get()
        idade = entry_idade.get()
        ref = db.reference(f'/escola/{aluno_id}')
        ref.update({
            'estudante': estudante,
            'curso': curso,
            'idade': idade
        })
        exibir_alunos()  # Atualiza a exibição da tabela
        entry_estudante.delete(0, tk.END)
        entry_curso.delete(0, tk.END)
        entry_idade.delete(0, tk.END)

# Criação da janela principal
window = tk.Tk()
window.title("Cadastro de alunos")

# Personalização de estilo
window.geometry("815x460")  # Define o tamanho da janela

# Componentes da interface
label_estudante = tk.Label(window, text="Nome do aluno:")
entry_estudante = tk.Entry(window)

label_curso = tk.Label(window, text="curso:")
entry_curso = tk.Entry(window)

label_idade = tk.Label(window, text="idade:")
entry_idade = tk.Entry(window)

button_cadastrar = tk.Button(window, text="Cadastrar aluno", command=cadastrar_aluno, bg="green", fg="white")

# Botões para exibir os alunos, editar aluno e excluir aluno
button_exibir = tk.Button(window, text="Exibir alunos", command=exibir_alunos, bg="blue", fg="white")
button_editar = tk.Button(window, text="Editar aluno", command=editar_aluno, bg="blue", fg="white")
button_excluir = tk.Button(window, text="Excluir aluno", command=excluir_aluno, bg="red", fg="white")

# Treeview para exibir os alunos
tree = ttk.Treeview(window, columns=("Título", "curso", "idade", "ID"), show="headings")
tree.heading("Título", text="Título")
tree.heading("curso", text="curso")
tree.heading("idade", text="idade")
tree.heading("ID", text="ID")

# Organização dos componentes na janela
label_estudante.grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_estudante.grid(row=0, column=1,columnspan=2, padx=5, pady=5, sticky='w')
label_curso.grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_curso.grid(row=1, column=1,columnspan=2, padx=5, pady=5, sticky='w')
label_idade.grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_idade.grid(row=2, column=1,columnspan=5, padx=5, pady=5, sticky='w')
button_cadastrar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='we')
button_exibir.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='we')
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
button_editar.grid(row=6, column=0, padx=5, pady=5, sticky='w')
button_excluir.grid(row=6, column=1, padx=5, pady=5, sticky='e')

# Iniciar a janela
window.mainloop()
