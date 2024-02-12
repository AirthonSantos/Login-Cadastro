# Importando algumas funções necessárias
from tkinter import messagebox, Toplevel, Button, Frame, Entry, Label, PhotoImage
from PIL import Image, ImageTk
from hashlib import sha256
from secrets import token_hex
from re import search

class TelaCadastro:
    """Essa classe é usada em conjunto com a classe TelaLogin"""

    def __init__(self, janelaPrincipal, banco_de_dados):
        self.banco = banco_de_dados
        self.modo_botao = True
        self.janelaLogin = janelaPrincipal
        self.janelaCadastro = None
    
    def GUI(self):
        """Gera a interface gráfica da tela de cadastro"""

        # Oculta a tela de login quando a tela de cadastro estiver aberta
        if self.janelaLogin.state() == "normal":
            self.janelaLogin.withdraw()

        janela = Toplevel()
      
        # Ponteiro que vai apontar pra essa janela
        self.janelaCadastro = janela

        janela.title("Cadastro")
        janela.geometry("500x500")
        janela.config(bg="#fff")
        janela.resizable(False, False)
        janela.iconphoto(False, PhotoImage(file=".\Icones\Icone_da_Janela.png"))

        # Função responsável por alternar entre o light e o dark mode
        def customizar():

            # Função criada para evitar repetição de codigo
            def troca(cor1, cor2, imagem):
                botao_alternar_cor.config(image=imagem, bg=cor1, activebackground=cor1)
                janela.config(bg=cor1)
                frame_login.config(bg=cor1)
                titulo.config(bg=cor1)
                usuario.config(bg=cor1, fg=cor2)
                email.config(bg=cor1, fg=cor2)
                senha.config(bg=cor1, fg=cor2)
                frame_usuario_linha.config(bg=cor2)
                frame_email_linha.config(bg=cor2)
                frame_senha_linha.config(bg=cor2)
                label_cadastrado.config(bg=cor1, fg=cor2)
                botao_conectar.config(bg=cor1, activebackground=cor1, activeforeground=cor2)

            if self.modo_botao: # Dark Mode
                troca("#26242f", "white", on)
                self.modo_botao = False
            else: # Light Mode
                troca("white", "#26242f", off)
                self.modo_botao = True

        # Importando e tratando as imagens
        off = Image.open(".\Icones\Icone_Claro.png")
        off = off.resize((40, 40))
        off = ImageTk.PhotoImage(off)

        on = Image.open(".\Icones\Icone_Escuro.png")
        on = on.resize((40, 40))
        on = ImageTk.PhotoImage(on)

        # Botão para alternar entre o light ou o dark mode
        botao_alternar_cor = Button(janela, image=off, bd=0, bg="white", activebackground="white", command=customizar)
        botao_alternar_cor.place(x=455, y=2)

        # Criação do título e do frame onde ficarão todos os widgets
        frame_login = Frame(janela, width=350, height=350, bg="white")
        frame_login.place(x=80, y=60)

        titulo = Label(frame_login, text="Crie sua conta", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
        titulo.place(x=60, y=5)

        # Campo do usuário
        def dentro_usuario(evento):
            if usuario.get() != "Nome":
                pass
            else:
                usuario.delete(0, "end")

        def fora_usuario(evento): 
            if usuario.get() == "":
                usuario.insert(0, "Nome")
            
        usuario = Entry(frame_login, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        usuario.place(x=30, y=80)
        usuario.insert(0, "Nome")
        usuario.bind("<FocusIn>", dentro_usuario)
        usuario.bind("<FocusOut>", fora_usuario)

        frame_usuario_linha = Frame(frame_login, width=295,height=2, bg="black")
        frame_usuario_linha.place(x=25, y=107)

        # Campo do email
        def dentro_email(evento):
            if email.get() != "E-mail":
                pass
            else:
                email.delete(0, "end")

        def fora_email(evento):
            if email.get() == "":
                email.insert(0, "E-mail")


        email = Entry(frame_login, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        email.place(x=30, y=150)
        email.insert(0, "E-mail")
        email.bind("<FocusIn>", dentro_email)
        email.bind("<FocusOut>", fora_email)


        frame_email_linha = Frame(frame_login, width=295, height=2, bg="black")
        frame_email_linha.place(x=25, y=178)

        # Campo da senha
        def dentro_senha(evento):
            if senha.get() != "Senha":
                pass
            else:
                senha.delete(0, "end")
                senha.config(show="*")

        def fora_senha(evento):
            if senha.get() == "":
                senha.config(show="")
                senha.insert(0, "Senha")

        senha = Entry(frame_login, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        senha.place(x=30, y=220)
        senha.insert(0, "Senha")
        senha.bind("<FocusIn>", dentro_senha)
        senha.bind("<FocusOut>", fora_senha)

        frame_senha_linha = Frame(frame_login, width=295, height=2, bg="black")
        frame_senha_linha.place(x=25, y=250)

        # Botões
        botao_cadastro = Button(frame_login, width=39, pady=7, text="Cadastrar", bg="#57a1f8", fg="white", border=0, command=lambda: self.cadastro(usuario.get(), email.get(), senha.get()))
        botao_cadastro.place(x=35, y=280)

        label_cadastrado = Label(frame_login, text="Possui uma conta?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
        label_cadastrado.place(x=80, y=320)

        botao_conectar = Button(frame_login, width=9, text="Conecte-se", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=self.fechar_janela)
        botao_conectar.place(x=190, y=321)

        # Caso a janela seja fechada, todo o restante é encerrado
        self.janelaCadastro.protocol("WM_DELETE_WINDOW", self.janela_existir)

        janela.mainloop()

    def cadastro(self, nome, email, senha):
        """Realiza a operação de cadastro do usuario"""

        # Função que serve para identificar se a senha cumpre os requisitos
        def requisitos_senha(string):
            lower_case = r"[a-z]"
            upper_case = r"[A-Z]"
            numeros = r"[0-9]"
            simbolos = r"[!@#$%&_]"
            return bool(search(numeros, string)) and bool(search(upper_case, string)) and bool(search(lower_case, string) and bool(search(simbolos, string)))
        
        # Verifica os campos
        if len(nome) > 0:
            if nome == "Nome":
                messagebox.showwarning("Aviso", "Nome Inválido")
                return
        else:
            messagebox.showwarning("Aviso", "Nome Inválido")
            return

        if len(email) > 0:
            if "@" in email and ".com" in email:
                pass         
            else:
                messagebox.showwarning("Aviso", "E-mail Inválido")
                return
        else:
            messagebox.showwarning("Aviso", "E-mail Inválido")
            return

        if len(senha) > 0:
            if senha == "Senha":
                messagebox.showwarning("Aviso", "Senha Inválida")
                return
            
            if requisitos_senha(senha):
                pass
            else:
                messagebox.showwarning("Aviso", "Sua senha precisa ter no mínimo 8 caracteres e deve possuir pelo menos uma letra maiúscula, minúscula, um número e um símbolo (!, @, #, $, %, & ou _)")
                return
        else:
            messagebox.showwarning("Aviso", "Senha Inválida")
            return
        
        self.banco.cursor.execute("SELECT e_mail from Registros_login WHERE e_mail = ?", (email, ))

        # Verifica se já existe um email cadastrado
        if self.banco.cursor.fetchone():
            messagebox.showwarning("Aviso" , "Esse e-mail já está cadastrado")
            return

        # Pega o salt e adiciona na senha
        salt = token_hex(16)
        senha_salt = senha + salt

        # Calcula a hash da senha com o salt usando o sha256
        senha_hash = sha256(senha_salt.encode()).hexdigest()

        dados = nome, email, senha_hash, salt

        try:
            # Realiza o cadastro do usuário
            comando = """
                INSERT INTO Registros_Login (nome_de_usuario, e_mail, senha, salt) VALUES
                (?, ?, ?, ?);
            """

            self.banco.cursor.execute(comando, dados)
            self.banco.conector.commit()
            
            messagebox.showinfo("Usuário criado!", "Cadastro efetuado com sucesso")

        except:
            # Caso aconteça algum erro no cadastro
            messagebox.showerror("Operação mal sucedida", "Aconteceu alguma coisa de errado\n")
            return

        self.fechar_janela()

    def janela_existir(self):
        """Se a janela de cadastro for fechada, a tela de login e a conexão com o banco de dados são encerradas"""
        self.banco.fechar_conexao()
        self.janelaLogin.destroy()
            
    def fechar_janela(self):
        """Volta para a tela de login"""
        self.janelaCadastro.destroy()
        self.janelaLogin.deiconify()