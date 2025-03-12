import sqlite3
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")

        self.label_usuario = ctk.CTkLabel(root, text="Usuário:")
        self.label_usuario.pack(pady=10)
        self.entry_usuario = ctk.CTkEntry(root, width=200)
        self.entry_usuario.pack()

        self.label_senha = ctk.CTkLabel(root, text="Senha:")
        self.label_senha.pack(pady=10)
        self.entry_senha = ctk.CTkEntry(root, show="*", width=200)
        self.entry_senha.pack()

        self.button_login = ctk.CTkButton(root, text="Entrar", command=self.verificar_login)
        self.button_login.pack(pady=20)

    def verificar_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if usuario == "admin" and senha == "1234":
            self.root.destroy()
            main_app()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

class CatalogoEspecies:
    def __init__(self, root):
        self.root = root
        self.root.title("Catálogo de Espécies")
        self.root.geometry("950x600")

        # Conexão com o banco de dados
        self.conn = sqlite3.connect("catalogo_especies.db")
        self.cursor = self.conn.cursor()
        self.criar_tabela()

        # Elementos da interface
        self.label_nome = tk.Label(root, text="Nome da Espécie:")
        self.label_nome.place(x=20, y=20)
        self.entry_nome = tk.Entry(root, width=30)
        self.entry_nome.place(x=150, y=20)

        self.label_status = tk.Label(root, text="Nível de Extinção:")
        self.label_status.place(x=20, y=60)
        self.combobox_status = ttk.Combobox(root, values=["Crítico", "Em Perigo", "Vulnerável", "Pouco Preocupante"], state="readonly", width=27)
        self.combobox_status.place(x=150, y=60)

        self.label_imagem = tk.Label(root, text="Imagem:")
        self.label_imagem.place(x=20, y=100)
        self.button_imagem = tk.Button(root, text="Carregar Imagem", command=self.carregar_imagem)
        self.button_imagem.place(x=150, y=100)

        self.label_descricao = tk.Label(root, text="Descrição:")
        self.label_descricao.place(x=20, y=140)
        self.text_descricao = tk.Text(root, width=60, height=5)
        self.text_descricao.place(x=150, y=140)

        self.button_adicionar = tk.Button(root, text="Adicionar/Salvar Espécie", command=self.adicionar_especie)
        self.button_adicionar.place(x=20, y=250)
        self.button_remover = tk.Button(root, text="Remover Espécie", command=self.remover_especie)
        self.button_remover.place(x=200, y=250)
        self.button_buscar = tk.Button(root, text="Buscar Espécie", command=self.buscar_especie)
        self.button_buscar.place(x=400, y=250)

        # Treeview para listar espécies
        self.treeview_especies = ttk.Treeview(root, columns=("Nome", "Descrição", "Status"), show="headings", height=15)
        self.treeview_especies.place(x=20, y=300)
        self.treeview_especies.heading("Nome", text="Nome")
        self.treeview_especies.heading("Descrição", text="Descrição")
        self.treeview_especies.heading("Status", text="Status")
        self.treeview_especies.column("Nome", width=150)
        self.treeview_especies.column("Descrição", width=400)
        self.treeview_especies.column("Status", width=150)

        self.treeview_especies.bind("<<TreeviewSelect>>", self.carregar_selecionado)

        # Exibir imagem
        self.canvas_imagem = tk.Canvas(root, width=200, height=200, bg="white")
        self.canvas_imagem.place(x=700, y=20)

        self.caminho_imagem = None
        self.imagem_tk = None

        self.listar_especies()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS especies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                status TEXT,
                descricao TEXT,
                imagem BLOB
            )
        """)
        self.conn.commit()

    def carregar_imagem(self):
        self.caminho_imagem = filedialog.askopenfilename(filetypes=[("Arquivos de Imagem", "*.jpg;*.png;*.jpeg")])
        if self.caminho_imagem:
            imagem = Image.open(self.caminho_imagem)
            imagem = imagem.resize((200, 200))
            self.imagem_tk = ImageTk.PhotoImage(imagem)
            self.canvas_imagem.create_image(100, 100, image=self.imagem_tk)

    def adicionar_especie(self):
        nome = self.entry_nome.get().strip()
        status = self.combobox_status.get().strip()
        descricao = self.text_descricao.get("1.0", tk.END).strip()

        if not nome:
            messagebox.showerror("Erro", "O nome da espécie é obrigatório!")
            return

        imagem_bytes = None
        if self.caminho_imagem:
            with open(self.caminho_imagem, "rb") as file:
                imagem_bytes = file.read()

        self.cursor.execute("""
            INSERT OR REPLACE INTO especies (nome, status, descricao, imagem)
            VALUES (?, ?, ?, ?)
        """, (nome, status, descricao, imagem_bytes))
        self.conn.commit()
        self.listar_especies()

    def remover_especie(self):
        selected_item = self.treeview_especies.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma espécie para remover!")
            return

        nome = self.treeview_especies.item(selected_item, "values")[0]
        self.cursor.execute("DELETE FROM especies WHERE nome = ?", (nome,))
        self.conn.commit()
        self.listar_especies()

    def buscar_especie(self):
        nome = self.entry_nome.get().strip()
        self.cursor.execute("SELECT * FROM especies WHERE nome = ?", (nome,))
        especie = self.cursor.fetchone()
        if especie:
            self.carregar_dados_especie(especie)
        else:
            messagebox.showerror("Erro", "Espécie não encontrada!")

    def carregar_selecionado(self, event):
        selected_item = self.treeview_especies.selection()
        if selected_item:
            nome = self.treeview_especies.item(selected_item, "values")[0]
            self.cursor.execute("SELECT * FROM especies WHERE nome = ?", (nome,))
            especie = self.cursor.fetchone()
            if especie:
                self.carregar_dados_especie(especie)

    def carregar_dados_especie(self, especie):
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, especie[1])
        self.combobox_status.set(especie[2])
        self.text_descricao.delete("1.0", tk.END)
        self.text_descricao.insert("1.0", especie[3])

        if especie[4]:
            imagem = Image.open(io.BytesIO(especie[4]))
            imagem = imagem.resize((200, 200))
            self.imagem_tk = ImageTk.PhotoImage(imagem)
            self.canvas_imagem.create_image(100, 100, image=self.imagem_tk)

    def listar_especies(self):
        self.treeview_especies.delete(*self.treeview_especies.get_children())
        self.cursor.execute("SELECT nome, descricao, status FROM especies")
        for especie in self.cursor.fetchall():
            self.treeview_especies.insert("", tk.END, values=especie)

def main_app():
    ctk.set_appearance_mode("dark")
    root = tk.Tk()
    CatalogoEspecies(root)
    root.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    LoginScreen(root)
    root.geometry('300x250')
    root.mainloop()
