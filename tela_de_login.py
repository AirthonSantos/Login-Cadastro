# Importando os módulos necessários
from tkinter import messagebox, Tk, Button, Frame, Entry, Label, PhotoImage, ACTIVE, DISABLED
from PIL import Image, ImageTk
from re import match
from hashlib import sha256
from sqlite3 import DataError, IntegrityError, ProgrammingError, OperationalError, DatabaseError, InterfaceError

# Importando arquivos adicionais
from tela_de_cadastro import TelaCadastro
from bancologin import BancoDados

# Essa constante possui o tempo, em segundos, que o login ficará bloqueado quando as tentativas forem excedidas
SEGUNDOS = 3

class TelaLogin:
    """Essa classe é responsável por criar a tela de login e estabelecer a conexão com o banco de dados"""

    def __init__(self):
        self._banco = BancoDados()
        self._botao_modo = True
        self.tentativas = 0
        self._janela = Tk()

    def gui(self):
        """Cria a tela de login"""

        # Inicia a janela de cadastro
        _tela2 = TelaCadastro(self._janela, self._banco)

        self._janela.title("Login")
        self._janela.geometry("500x500")
        self._janela.configure(bg="#fff")
        self._janela.resizable(False, False)
        self._janela.iconphoto(False, PhotoImage(file=".\Icones\icone_janela.png"))

        # Função responsável por alternar entre o modo claro e o escuro
        def customizar():

            # Função criada para evitar repetição de código e serve para trocar as cores da interface
            def troca(cor1, cor2, imagem):
                _botao_alternar_cor.config(image=imagem, bg=cor1, activebackground=cor1)
                self._janela.config(bg=cor1)
                _frame_login.config(bg=cor1)
                _titulo.config(bg=cor1)
                _email.config(bg=cor1, fg=cor2)
                _senha.config(bg=cor1, fg=cor2)
                _frame_email_linha.config(bg=cor2)
                _frame_senha_linha.config(bg=cor2)
                _label_registro.config(bg=cor1, fg=cor2)
                _botao_cadastro.config(bg=cor1, activebackground=cor1, activeforeground=cor2)

            if self._botao_modo: # Modo Escuro
                troca("#26242f", "white", _on)
                self._botao_modo = False
            else: # Modo Claro
                troca("white", "#26242f", _off)
                self._botao_modo = True

        # Importando e tratando as imagens
        _off = Image.open(".\Icones\icone_claro.png")
        _off = _off.resize((40, 40))
        _off = ImageTk.PhotoImage(_off)

        _on = Image.open(".\Icones\icone_escuro.png")
        _on = _on.resize((40, 40))
        _on = ImageTk.PhotoImage(_on)

        # Botão para alternar entre o modo claro e o escuro
        _botao_alternar_cor = Button(self._janela, image=_off, bd=0, bg="white", activebackground="white", command=customizar)
        _botao_alternar_cor.place(x=455, y=2)

        # Criação do título e do frame onde ficarão todos os widgets
        _frame_login = Frame(self._janela, width=350, height=350, bg="white")
        _frame_login.place(x=80, y=85)

        _titulo = Label(_frame_login, text="Login", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
        _titulo.place(x=120, y=5)

        # Campo do email
        def dentro_do_campo_email(evento):
            if _email.get() != "E-mail":
                pass
            else:
                _email.delete(0, "end")

        def fora_do_campo_email(evento): 
            if _email.get() == "":
                _email.insert(0, "E-mail")

        _email = Entry(_frame_login, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        _email.place(x=30, y=80)
        _email.insert(0, "E-mail")
        _email.bind("<FocusIn>", dentro_do_campo_email)
        _email.bind("<FocusOut>", fora_do_campo_email)

        _frame_email_linha = Frame(_frame_login, width=295,height=2, bg="black")
        _frame_email_linha.place(x=25, y=107)

        # Campo da senha
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
        _senha.place(x=30, y=150)
        _senha.insert(0, "Senha")
        _senha.bind("<FocusIn>", dentro_do_campo_senha)
        _senha.bind("<FocusOut>", fora_do_campo_senha)

        _frame_senha_linha = Frame(_frame_login, width=295,height=2, bg="black")
        _frame_senha_linha.place(x=25, y=177)

        # Botões
        self._botao_conectar = Button(_frame_login, width=39, pady=7, text="Conectar", bg="#57a1f8", fg="white", border=0, command=lambda: self.login(_email.get(), _senha.get()))
        self._botao_conectar.place(x=35, y=204)

        _label_registro = Label(_frame_login, text="Ainda não tem uma conta?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
        _label_registro.place(x=50, y=245)

        _botao_cadastro = Button(_frame_login, width=9, text="Cadastre-se", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=_tela2.gui)
        _botao_cadastro.place(x=208, y=246)

        # Caso a janela seja fechada, o resto é encerrado
        self._janela.protocol("WM_DELETE_WINDOW", self.encerrar)

        self._janela.mainloop()

    def login(self, email, senha):
        """Realiza o processo de autenticação"""

        # Valida os campos
        if len(email) > 0:
            if match(r".+@.+\..+", email):
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
        
        # Tenta buscar os dados do usuário no banco de dados
        try:
            self._banco._cursor.execute("SELECT * FROM Registros_Login WHERE e_mail = ?;", (email, ))
            _resultado = self._banco._cursor.fetchone()

        # Captura erros relacionados a dados inválidos ou inconsistentes
        except DataError as erro_dados:
            messagebox.showerror("Erro de dados", f"Houve uma falha de dados, não foi possivel concluir o login. \nErro: {erro_dados}")
            return

        # Captura violações de integridade, como chaves primárias ou estrangeiras duplicadas
        except IntegrityError as erro_integridade:
            messagebox.showerror("Erro de integridade", f"Houve uma falha de integridade, não foi possivel concluir o login. \nErro: {erro_integridade}")
            return

        # Captura erros relacionados a uso incorreto da API do sqlite3 ou comandos SQL inválidos
        except ProgrammingError as erro_programacao:
            messagebox.showerror("Erro de programação", f"Houve uma falha de programação, não foi possivel concluir o login. \nErro: {erro_programacao}")
            return

        # Captura problemas operacionais, como falhas de conexão ou de tabela inexistente
        except OperationalError as erro_operacional:
            messagebox.showerror("Erro operacional", f"Houve uma falha operacional, não foi possivel concluir o login. \nErro: {erro_operacional}")
            return

        # Captura erros gerais relacionados ao banco de dados
        except DatabaseError as erro_banco:
            messagebox.showerror("Erro do banco de dados", f"Houve uma falha no banco de dados, não foi possivel concluir o login. \nErro: {erro_banco}")
            return
        
        # Captura erros específicos da interface do banco de dados, geralmente problemas internos com a biblioteca sqlite3
        except InterfaceError as erro_interno:
            messagebox.showerror("Erro da interface", f"Houve uma falha interna do sqlite3, não foi possivel concluir o login. \nErro: {erro_interno}")
            return

        # Captura qualquer outra exceção que não foi tratada anteriormente
        except Exception as erro_desconhecido:
            messagebox.showerror("Erro desconhecido", f"Não foi possivel concluir o login. \nErro: {erro_desconhecido}")
            return

        # Se o usuário não foi encontrado, exibe uma mensagem de aviso
        if not _resultado:
            messagebox.showwarning("Aviso", "Usuário não encontrado")
            self.tentativas += 1
            self.limite_login()
            return

        # Pega a senha e o salt
        _senha_sql, _salt = _resultado[3], _resultado[4]
            
        # Calcula a hash da senha com o salt
        _senha_salt = senha + _salt
        _senha_hash = sha256(_senha_salt.encode()).hexdigest()

        # Verifica se a senha corresponde à senha no banco de dados
        if _senha_hash == _senha_sql:
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
            self._botao_conectar.config(state=DISABLED)
            messagebox.showwarning("Bloqueado", f"Foi excedido o número de tentativas!\nAguarde {SEGUNDOS} segundos")
            self._janela.after(SEGUNDOS * 1000, self.reativar_botao)

    def reativar_botao(self):
        """Desbloqueia o botão de login"""
        self._botao_conectar.config(state=ACTIVE)
        messagebox.showinfo("Info", "Login desbloqueado")

    def encerrar(self):
        """Encerra a aplicação e a conexão com o banco de dados"""
        self._banco.fechar_conexao()
        self._janela.destroy()

# Executa o código
if __name__ == "__main__":
    telalogin = TelaLogin()
    telalogin.gui()