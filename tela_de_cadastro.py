from tkinter import messagebox, Toplevel, Button, Frame, Entry, Label, PhotoImage
from sqlite3 import DataError, IntegrityError, ProgrammingError, OperationalError, InternalError
from PIL import Image, ImageTk
from hashlib import sha256
from secrets import token_hex
from re import match, compile

class TelaCadastro:
    """Essa classe é usada em conjunto com a classe TelaLogin"""

    def __init__(self, janela_principal, banco_de_dados):
        self._banco = banco_de_dados
        self._modo_botao = True
        self._janela_login = janela_principal
        self._janela_cadastro = None
    
    def gui(self):
        """Gera a interface gráfica da tela de cadastro"""

        # Oculta a tela de login quando a tela de cadastro estiver aberta
        if self._janela_login.state() == "normal":
            self._janela_login.withdraw()

        _janela = Toplevel()
      
        # Ponteiro que nos permitirá fechar essa janela após o usuário completar o cadastro
        self._janela_cadastro = _janela

        _janela.title("Cadastro")
        _janela.geometry("500x500")
        _janela.config(bg="#fff")
        _janela.resizable(False, False)
        _janela.iconphoto(False, PhotoImage(file=".\Icones\icone_janela.png"))

        ###
                
        def customizar():

            def troca(cor1, cor2, imagem):
                _botao_alternar_cor.config(image=imagem, bg=cor1, activebackground=cor1)
                _janela.config(bg=cor1)
                _frame_login.config(bg=cor1)
                _titulo.config(bg=cor1)
                _usuario.config(bg=cor1, fg=cor2)
                _email.config(bg=cor1, fg=cor2)
                _senha.config(bg=cor1, fg=cor2)
                _frame_usuario_linha.config(bg=cor2)
                _frame_email_linha.config(bg=cor2)
                _frame_senha_linha.config(bg=cor2)
                _label_cadastrado.config(bg=cor1, fg=cor2)
                _botao_conectar.config(bg=cor1, activebackground=cor1, activeforeground=cor2)

            if self._modo_botao:
                troca("#26242f", "white", _on)
                self._modo_botao = False
            else:
                troca("white", "#26242f", _off)
                self._modo_botao = True

        _off = Image.open(".\Icones\icone_claro.png")
        _off = _off.resize((40, 40))
        _off = ImageTk.PhotoImage(_off)

        _on = Image.open(".\Icones\icone_escuro.png")
        _on = _on.resize((40, 40))
        _on = ImageTk.PhotoImage(_on)

        ###

        _botao_alternar_cor = Button(_janela, image=_off, bd=0, bg="white", activebackground="white", command=customizar)
        _botao_alternar_cor.place(x=455, y=2)

        _frame_login = Frame(_janela, width=350, height=350, bg="white")
        _frame_login.place(x=80, y=60)

        _titulo = Label(_frame_login, text="Crie sua conta", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
        _titulo.place(x=60, y=5)

       ###

        def dentro_do_campo_usuario(evento):
            if _usuario.get() != "Nome":
                pass
            else:
                _usuario.delete(0, "end")

        def fora_do_campo_usuario(evento): 
            if _usuario.get() == "":
                _usuario.insert(0, "Nome")
            
        _usuario = Entry(_frame_login, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        _usuario.place(x=30, y=80)
        _usuario.insert(0, "Nome")
        _usuario.bind("<FocusIn>", dentro_do_campo_usuario)
        _usuario.bind("<FocusOut>", fora_do_campo_usuario)

        _frame_usuario_linha = Frame(_frame_login, width=295,height=2, bg="black")
        _frame_usuario_linha.place(x=25, y=107)

        ###

        def dentro_do_campo_email(evento):
            if _email.get() != "E-mail":
                pass
            else:
                _email.delete(0, "end")

        def fora_do_campo_email(evento):
            if _email.get() == "":
                _email.insert(0, "E-mail")


        _email = Entry(_frame_login, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        _email.place(x=30, y=150)
        _email.insert(0, "E-mail")
        _email.bind("<FocusIn>", dentro_do_campo_email)
        _email.bind("<FocusOut>", fora_do_campo_email)

        _frame_email_linha = Frame(_frame_login, width=295, height=2, bg="black")
        _frame_email_linha.place(x=25, y=178)

        ###

        def dentro_do_campo_senha(evento):
            if _senha.get() != "Senha":
                pass
            else:
                _senha.delete(0, "end")
                _senha.config(show="*")

        def fora_do_campo_senha(evento):
            if _senha.get() == "":
                _senha.config(show="")
                _senha.insert(0, "Senha")

        _senha = Entry(_frame_login, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        _senha.place(x=30, y=220)
        _senha.insert(0, "Senha")
        _senha.bind("<FocusIn>", dentro_do_campo_senha)
        _senha.bind("<FocusOut>", fora_do_campo_senha)

        _frame_senha_linha = Frame(_frame_login, width=295, height=2, bg="black")
        _frame_senha_linha.place(x=25, y=250)

        ###

        _botao_cadastro = Button(_frame_login, width=39, pady=7, text="Cadastrar", bg="#57a1f8", fg="white", border=0, command=lambda: self.cadastro(_usuario.get(), _email.get(), _senha.get()))
        _botao_cadastro.place(x=35, y=280)

        _label_cadastrado = Label(_frame_login, text="Possui uma conta?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
        _label_cadastrado.place(x=80, y=320)

        _botao_conectar = Button(_frame_login, width=9, text="Conecte-se", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=self.fechar_janela)
        _botao_conectar.place(x=190, y=321)


        self._janela_cadastro.protocol("WM_DELETE_WINDOW", self.janela_existir)

        _janela.mainloop()

    def cadastro(self, nome, email, senha):
        """Realiza o cadastro do usuario"""

        # Compila os padrões de expressão regular para diferentes critérios de senha
        regex_letra_minuscula = compile(r"[a-z]")
        regex_letra_maiuscula = compile(r"[A-Z]")
        regex_numeros = compile(r"[0-9]")
        regex_simbolos = compile(r"[!@#$%&_]")

        def requisitos_senha(string):
            return all(
                regex.search(string) 
                for regex in [regex_letra_minuscula, regex_letra_maiuscula, regex_numeros, regex_simbolos]
            )

        # Validação dos campos
        if len(nome) > 0:
            if nome == "Nome":
                messagebox.showwarning("Aviso", "Nome Inválido")
                return
        else:
            messagebox.showwarning("Aviso", "Nome Inválido")
            return

        if len(email) > 0:
            if match(r".+@.+\.com", email):
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
        
        # Verifica se o email fornecido já está cadastrado no banco de dados
        self._banco._cursor.execute("SELECT e_mail from Registros_login WHERE e_mail = ?", (email, ))

        if self._banco._cursor.fetchone():
            messagebox.showwarning("Aviso" , "Esse e-mail já está cadastrado")
            return

        # Cria o salt e o adiciona na senha
        _salt = token_hex(16)
        _senha_salt = senha + _salt

        # Calcula a hash da senha com o salt usando o sha256
        _senha_hash = sha256(_senha_salt.encode()).hexdigest()

        _dados = nome, email, _senha_hash, _salt

        # Tenta registrar o usuário
        try:
            _comando = """
                INSERT INTO Registros_Login (nome_de_usuario, e_mail, senha, salt) VALUES
                (?, ?, ?, ?);
            """

            self._banco._cursor.execute(_comando, _dados)
            self._banco._conector.commit()
            
            messagebox.showinfo("Usuário criado!", "Cadastro efetuado com sucesso")
        
        # Captura erros relacionados a dados inválidos ou inconsistentes
        except DataError as erro_dados:
            messagebox.showerror("Erro de dados", f"Houve uma falha de dados, não foi possivel concluir o cadastro. \nErro: {erro_dados}")

        # Captura violações de integridade, como chaves primárias ou estrangeiras duplicadas
        except IntegrityError as erro_integridade:
            messagebox.showerror("Erro de integridade", f"Houve uma falha de integridade, não foi possivel concluir o cadastro. \nErro: {erro_integridade}")

        # Captura erros relacionados a uso incorreto da API do sqlite3 ou comandos SQL inválidos
        except ProgrammingError as erro_programacao:
            messagebox.showerror("Erro de programação", f"Houve uma falha de programação, não foi possivel concluir o cadastro. \nErro: {erro_programacao}")

        # Captura problemas operacionais, como falhas de conexão ou de tabela inexistente
        except OperationalError as erro_operacional:
            messagebox.showerror("Erro operacional", f"Houve uma falha operacional, não foi possivel concluir o cadastro. \nErro: {erro_operacional}")

        # Captura erros internos graves do banco de dados, como falhas no sistema ou inconsistências graves
        except InternalError as erro_interno:
            messagebox.showerror("Erro interno", f"Houve uma falha interna no sqlite3, não foi possivel concluir o cadastro. \nErro: {erro_interno}")

        # Captura qualquer outra exceção que não foi tratada anteriormente
        except Exception as erro_desconhecido:
            messagebox.showerror("Erro desconhecido", f"Não foi possivel concluir o cadastro. \nErro: {erro_desconhecido}")

        self.fechar_janela()

    def janela_existir(self):
        """Se a janela de cadastro for fechada, a tela de login e a conexão com o banco de dados são encerradas"""
        self._banco.fechar_conexao()
        self._janela_login.destroy()
            
    def fechar_janela(self):
        """Volta para a tela de login e encerra essa janela"""
        self._janela_cadastro.destroy()
        self._janela_login.deiconify()