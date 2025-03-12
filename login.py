import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import webbrowser
import DataBase
import os
from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def criar_banco_de_dados():
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  Local TEXT,
                  Serie INTEGER,   
                  Valor INTEGER, 
                  Pago INTEGER,
                  Data INTEGER,
                  Data2 INTEGER,
                  Data3 INTEGER,
                  Recebido INTEGER
                    )''')
    conn.commit()
    conn.close()


def deletar_item():
    try:
        # Pega o item selecionado
        item_selecionado = tree.selection()[0]

        # Pega os valores do item selecionado
        valores = tree.item(item_selecionado, 'values')
        id_selecionado = valores[0]

        # Conecta ao banco de dados e deleta o registro com o ID correspondente
        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_selecionado,))
        conexao.commit()
        conexao.close()
        tree.delete(item_selecionado)

        # Exibe uma mensagem de confirmação
        messagebox.showinfo("Sucesso", "Item deletado com sucesso!")
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um item para deletar.")


DataBase.conexao_db()


# Função para adicionar um novo usuário ao banco de dados
def add_Boletos():
    Local = entrada_Local.get()
    Serie = entrada_Serie.get()
    Valor = entrada_Valor.get()
    Pago = entrada_Pago.get()
    Data = entrada_Data.get()
    Data2 = entrada_Data2.get()
    Data3 = entrada_Data3.get()
    Recebido = entrada_Recebido.get()
    if Local and Serie and Valor and Pago and Data and Data2 and Data3 and Recebido:
        conn = sqlite3.connect('DataBase.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO users ( Local, Serie, Valor, Pago, Data, Data2, Data3, Recebido) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)",
            (Local, Serie, Valor, Pago, Data, Data2, Data3, Recebido))
        conn.commit()
        conn.close()
        entrada_Local.delete(0, tk.END)
        entrada_Serie.delete(0, tk.END)
        entrada_Valor.delete(0, tk.END)
        entrada_Pago.delete(0, tk.END)
        entrada_Data.delete(0, tk.END)
        entrada_Data2.delete(0, tk.END)
        entrada_Data3.delete(0, tk.END)
        entrada_Recebido.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Boleto adicionado com sucesso!")
        carregar_Boletos()
    else:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")


# Função para carregar os usuários do banco de dados no Treeview
def carregar_Boletos():
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    for users in users:
        tree.insert('', tk.END, values=users)


def buscar_registros():
    termo_busca = entrada_Busca.get()
    for row in tree.get_children():
        tree.delete(row)
    conexao = sqlite3.connect('DataBase.db')
    cursor = conexao.cursor()
    query = "SELECT * FROM users WHERE Local LIKE ? OR Serie LIKE ?"
    cursor.execute(query, ('%' + termo_busca + '%', '%' + termo_busca + '%'))
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conexao.close()

    if not rows:
        messagebox.showinfo("Resultado", "Nenhum registro encontrado.")


def adicionar_ao_treeview():
    Local = entrada_Local.get()
    Serie = entrada_Serie.get()
    Valor = entrada_Valor.get()
    Pago = entrada_Pago.get()
    Data = entrada_Data.get()
    Data2 = entrada_Data2.get()
    Data3 = entrada_Data3.get()
    Recebido = entrada_Recebido.get()
    if id and Local and Serie and Valor and Data and Data2 and Data3 and Recebido:
        id = len(tree.get_children()) + 1
        tree.insert('', 'end', values=(id, Local, Serie, Valor, Pago, Data, Data2, Data3, Recebido))
        entrada_Local.delete(0, tk.END)
        entrada_Serie.delete(0, tk.END)
        entrada_Valor.delete(0, tk.END)
        entrada_Pago.delete(0, tk.END)
        entrada_Data.delete(0, tk.END)
        entrada_Data2.delete(0, tk.END)
        entrada_Data3.delete(0, tk.END)
        entrada_Recebido.delete(0, tk.END)


def gerar_pdf():
    Local = entrada_Local.get()
    Serie = entrada_Serie.get()
    Valor = entrada_Valor.get()
    Pago = entrada_Pago.get()
    Data = entrada_Data.get()
    Data2 = entrada_Data2.get()
    Data3 = entrada_Data3.get()
    Recebido = entrada_Recebido.get()

    nome_arquivo = "Boleto.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    # Título
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(largura / 2.0, altura - 50, "Esquadrias Souza")

    # Dados
    c.setFont("Helvetica", 14)
    c.drawString(100, altura - 100, f"Local: {Local}")
    c.drawString(100, altura - 130, f"Serie: {Serie}")
    c.drawString(100, altura - 160, f"Valor: {Valor}")
    c.drawString(100, altura - 190, f"Pago: {Pago}")
    c.drawString(100, altura - 220, f"Data Venc.: {Data}")
    c.drawString(100, altura - 250, f"Data Venc-2: {Data2}")
    c.drawString(100, altura - 285, f"Data Venc-3: {Data3}")
    c.drawString(100, altura - 310, f"Recebido: {Recebido}")
    c.showPage()
    c.save()
    webbrowser.open_new('Boleto.pdf')
    if not Local or not Recebido:
        messagebox.showwarning("Entrada Inválida", "Por favor, Preencha todos os campos.")
        return

    pdf_filename = "Boletos.pdf"

    try:
        messagebox.showinfo("Sucesso", f"O PDF '{pdf_filename}' Foi gerado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o PDF: {e}")


# Configuração da janela principal do Tkinter
root = tk.Tk()
root.title("Gerenciador de Boletos")
root.geometry('900x505')
root.resizable(False, False)
root.config(bg='#089471')
Bg1 = '#089471'
Cor1 = '#FDFFFE'
Cor2 = '#44B356'
Cor3 = '#B4C9B7'

criar_banco_de_dados()

# Configuração do Treeview para exibir múltiplas colunas
tree = ttk.Treeview(root, columns=('id', 'Local', 'Serie', 'Valor', 'Pago', 'Data', 'Data2', 'Data3', 'Recebido'),
                    show='headings', )
tree.heading('id', text='id')
tree.heading('Local', text='Local')
tree.heading('Serie', text='Serie')
tree.heading('Valor', text='Valor')
tree.heading('Pago', text='Pago')
tree.heading('Data', text='Data')
tree.heading('Data2', text='Data2')
tree.heading('Data3', text='Data3')
tree.heading('Recebido', text='Recebido')
# Definindo largura das colunas
tree.column('id', width=70)
tree.column('Local', width=70)
tree.column('Serie', width=70)
tree.column('Valor', width=90)
tree.column('Pago', width=70)
tree.column('Data', width=70)
tree.column('Data2', width=70)
tree.column('Data3', width=60)
tree.column('Recebido', width=60)

# Exibe o Treeview na janela
tree.place(x=5, y=212, relheight=0.52, relwidth=0.99, height=25, )
# Criando frame da logo

pastaApp = os.path.dirname(__file__)

frame = tk.Frame(root, width=680, bg=Cor3, highlightcolor='#32a89b', highlightbackground='#48d5da',
                 highlightthickness=3)
frame.place(x=5, y=6, relheight=0.40, relwidth=0.99, )

image = Image.open("img/RS.png")
photo = ImageTk.PhotoImage(image)
# Labels e Entradas para Nome, Idad
label = tk.Label(frame, image=photo, bg=Cor3, )
label.image = photo
label.place(x=580, y=10, )

tk.Label(root, text="Local", bg=Cor3).place(x=15, y=15)
entrada_Local = tk.Entry(root, border=3)
entrada_Local.place(x=100, y=10)

tk.Label(root, text="N° do Doc", bg=Cor3).place(x=15, y=40)
entrada_Serie = tk.Entry(root, border=3)
entrada_Serie.place(x=100, y=40)

tk.Label(root, text="Valor", bg=Cor3).place(x=15, y=70)
entrada_Valor = tk.Entry(root, border=3)
entrada_Valor.place(x=100, y=70)

tk.Label(root, text='Pago', bg=Cor3).place(x=15, y=100)
entrada_Pago = tk.Entry(root, border=3)
entrada_Pago.place(x=100, y=100)

tk.Label(root, text='Busca', bg=Cor3, ).place(x=280, y=18)
entrada_Busca = tk.Entry(root, border=3, width=40)
entrada_Busca.place(x=335, y=18)

tk.Label(root, text='Data Venc.', bg=Cor3).place(x=205, y=150)
entrada_Data = tk.Entry(root, border=3)
entrada_Data.place(x=280, y=145)

tk.Label(root, text='Data Venc-2', bg=Cor3).place(x=205, y=175)
entrada_Data2 = tk.Entry(root, border=3, )
entrada_Data2.place(x=280, y=175)

tk.Label(root, text='Recebido', bg=Cor3).place(x=410, y=150)
entrada_Recebido = tk.Entry(root, border=3)
entrada_Recebido.place(x=510, y=145)

tk.Label(root, text='Data Venc-3', bg=Cor3).place(x=410, y=180)
entrada_Data3 = tk.Entry(root, border=3, )
entrada_Data3.place(x=510, y=175)

# Botão para gerar o PDF com os dados do Treeview
botao_gerar_pdf = tk.Button(root, text="Gerar PDF", bg=Cor2, font='Arial  8 bold', command=gerar_pdf)
botao_gerar_pdf.place(x=130, y=170)

# Botão para adicionar o usuário
botao_adicionar = tk.Button(root, text="Adicionar Boleto", bg=Cor2, font='Arial  8 bold', command=add_Boletos)
botao_adicionar.place(x=10, y=170)

botao_adicionar = tk.Button(root, text="DELETAR", bg=Cor2, font='Arial  8 bold', command=deletar_item)
botao_adicionar.place(x=10, y=130)

botao_adicionar = tk.Button(root, text="BUSCAR", bg=Cor2, font='Arial  8 bold', command=buscar_registros)
botao_adicionar.place(x=335, y=45)

# Carrega os usuários existentes ao iniciar a aplicação

DataBase.conexao_db()
# Inicia o loop principal do Tkinter
root.mainloop()
