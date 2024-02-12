# Codificação: UTF-8
# Importando funções necessárias
from tkinter import messagebox, Tk, Button, Frame, Entry, Label, PhotoImage, ACTIVE, DISABLED
from PIL import Image, ImageTk
from hashlib import sha256

# Importando arquivos adicionais
from Tela_de_cadastro import TelaCadastro
from BancoLogin import BancoDados

# Essa constante possui o tempo, em segundos, que o login ficará bloqueado quando exceder as tentativas
SEGUNDOS = 3

class TelaLogin:
    """Essa classe é responsável por criar a tela de login e estabelecer a conexão com o banco de dados"""

    def __init__(self):
        self.banco = BancoDados()
        self.botao_modo = True
        self.tentativas = 0
        self.janela = Tk()

    def GUI(self):
        """Cria a tela de login"""

        # Inicia a janela de cadastro
        Tela2 = TelaCadastro(self.janela, self.banco)

        self.janela.title("Login")
        self.janela.geometry("500x500")
        self.janela.configure(bg="#fff")
        self.janela.resizable(False, False)
        self.janela.iconphoto(False, PhotoImage(file=".\Icones\Icone_da_Janela.png"))

        # Função responsável por alternar entre o light e o dark mode
        def customizar():

            # Função criada para evitar repetição de codigo
            def troca(cor1, cor2, imagem):
                botao_alternar_cor.config(image=imagem, bg=cor1, activebackground=cor1)
                self.janela.config(bg=cor1)
                frame_login.config(bg=cor1)
                titulo.config(bg=cor1)
                email.config(bg=cor1, fg=cor2)
                senha.config(bg=cor1, fg=cor2)
                frame_email_linha.config(bg=cor2)
                frame_senha_linha.config(bg=cor2)
                label_registro.config(bg=cor1, fg=cor2)
                botao_cadastro.config(bg=cor1, activebackground=cor1, activeforeground=cor2)

            # Alternando as cores
            if self.botao_modo: # Dark Mode
                troca("#26242f", "white", on)
                self.botao_modo = False
            else: # Light Mode
                troca("white", "#26242f", off)
                self.botao_modo = True

        # Importando e tratando as imagens
        off = Image.open(".\Icones\Icone_Claro.png")
        off = off.resize((40, 40))
        off = ImageTk.PhotoImage(off)

        on = Image.open(".\Icones\Icone_Escuro.png")
        on = on.resize((40, 40))
        on = ImageTk.PhotoImage(on)

        # Botão para alternar entre o light ou o dark
        botao_alternar_cor = Button(self.janela, image=off, bd=0, bg="white", activebackground="white", command=customizar)
        botao_alternar_cor.place(x=455, y=2)

        # Criação do título e do frame onde ficarão todos os widgets
        frame_login = Frame(self.janela, width=350, height=350, bg="white")
        frame_login.place(x=80, y=85)

        titulo = Label(frame_login, text="Login", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
        titulo.place(x=120, y=5)

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
        email.place(x=30, y=80)
        email.insert(0, "E-mail")
        email.bind("<FocusIn>", dentro_email)
        email.bind("<FocusOut>", fora_email)

        frame_email_linha = Frame(frame_login, width=295,height=2, bg="black")
        frame_email_linha.place(x=25, y=107)

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
        senha.place(x=30, y=150)
        senha.insert(0, "Senha")
        senha.bind("<FocusIn>", dentro_senha)
        senha.bind("<FocusOut>", fora_senha)

        frame_senha_linha = Frame(frame_login, width=295,height=2, bg="black")
        frame_senha_linha.place(x=25, y=177)

        # Botões
        self.botao_conectar = Button(frame_login, width=39, pady=7, text="Conectar", bg="#57a1f8", fg="white", border=0, command=lambda: self.login(email.get(), senha.get()))
        self.botao_conectar.place(x=35, y=204)

        label_registro = Label(frame_login, text="Ainda não tem uma conta?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
        label_registro.place(x=50, y=245)

        botao_cadastro = Button(frame_login, width=9, text="Cadastre-se", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=Tela2.GUI)
        botao_cadastro.place(x=208, y=246)

        # Caso a janela seja fechada, todo o restante é encerrado
        self.janela.protocol("WM_DELETE_WINDOW", self.encerrar)

        self.janela.mainloop()

    def login(self, email, senha):
        """Realiza o processo de autenticação"""

        # Verifica se os dados são válidos
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
        else:
            messagebox.showwarning("Aviso", "Senha Inválida")
            return

        self.banco.cursor.execute("SELECT * FROM Registros_Login WHERE e_mail = ?;", (email, ))
        resultado = self.banco.cursor.fetchone()

        # Verifica se existe o email no banco de dados
        if not resultado:
            messagebox.showwarning("Aviso", "Usuário não encontrado")
            self.tentativas += 1
            self.limite_login()
            return
        
        # Pega a senha e o salt do banco
        senha_sql, salt = resultado[3], resultado[4]
            
        # Calcula a hash da senha com o salt
        senha_salt = senha + salt
        senha_hash = sha256(senha_salt.encode()).hexdigest()

        # Verifica se a senha está certa
        if senha_hash == senha_sql:
            messagebox.showinfo("Acesso Autorizado", "Usuário encontrado!")
            self.tentativas = 0
            return
        else:
            messagebox.showwarning("Aviso", "Usuário não encontrado")
            self.tentativas += 1
            self.limite_login()
            return

    def limite_login(self): 
        """Verifica se o limite de tentativas foi alcançado"""
        if self.tentativas == 3:
            self.tentativas = 0
            self.botao_conectar.config(state=DISABLED)
            messagebox.showwarning("Bloqueado", f"Foi excedido o número de tentativas\nAguarde {SEGUNDOS} segundos")
            self.janela.after(SEGUNDOS * 1000, self.reativar_botao)

    def reativar_botao(self):
        """Desbloqueia o botão de login"""
        self.botao_conectar.config(state=ACTIVE)
        messagebox.showinfo("Info", "Login desbloqueado")

    def encerrar(self):
        """Encerra a aplicação e a conexão com o banco de dados"""
        self.banco.fechar_conexao()
        self.janela.destroy()

# Executa o programa
if __name__ == "__main__":
    telalogin = TelaLogin()
    telalogin.GUI()