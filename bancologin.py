from sqlite3 import connect, InterfaceError, OperationalError, DatabaseError, ProgrammingError
from tkinter import messagebox

class BancoDados:
    def __init__(self):
        """Inicia a conexão com o banco de dados, além de criar uma tabela e uma trigger"""

        try:
            # Tenta se conectar no banco de dados e cria um cursor
            self._conector = connect("banco_de_dados.db")
            self._cursor = self._conector.cursor()

        # Captura erros específicos da interface do banco de dados, geralmente problemas internos com a biblioteca sqlite3
        except InterfaceError as erro_interface :
            messagebox.showerror("Erro de interface", f"Houve uma falha na interface do sqlite3 ao tentar acessar o banco de dados. \nErro: {erro_interface}")
            return
            
        # Captura problemas operacionais, como falhas de conexão ou de tabela inexistente
        except OperationalError as erro_operacional:
            messagebox.showerror("Erro operacional", f"Houve uma falha operacional ao tentar acessar o banco de dados. \nErro: {erro_operacional}")
            return

        # Captura erros gerais relacionados ao banco de dados
        except DatabaseError as erro_banco:
            messagebox.showerror("Erro no banco de dados", f"Houve uma falha no banco de dados e não foi possivel se conectar. \nErro: {erro_banco}")
            return

        # Captura qualquer outra exceção que não foi tratada anteriormente
        except Exception as erro_desconhecido:
            messagebox.showerror("Erro desconhecido", f"Não foi possivel se conectar ao banco de dados. \nErro: {erro_desconhecido}")
            return

        # Cria a tabela onde os dados serão armazenados
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Registros_Login (
                id INTEGER PRIMARY KEY,
                nome_de_usuario VARCHAR(255) NOT NULL,
                e_mail VARCHAR(50) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL,
                salt VARCHAR(50) NOT NULL,
                data_hora DATETIME
            );
        """)

        # Verifica se existe a trigger, se não existir, ela é criada
        self._cursor.execute("SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'definir_data_hora'")

        if not self._cursor.fetchone():
            # Cria uma trigger para definir a data e hora do momento em que o usuario se cadastrou
            self._cursor.execute(""" 
                CREATE TRIGGER definir_data_hora
                AFTER INSERT ON Registros_Login
                FOR EACH ROW
                BEGIN
                    UPDATE Registros_Login SET data_hora = datetime("now", "localtime") WHERE id = NEW.id;
                END;
            """)

            self._conector.commit()

    def fechar_conexao(self):
        """Encerra a conexão com o banco de dados"""
        
        if self._cursor is not None:
            try:
                self._cursor.close()
            except ProgrammingError as erro_programacao:
                print(f"Erro ao fechar o cursor: {erro_programacao}")
            finally:
                self._cursor = None

        if self._conector is not None:
            try:
                self._conector.close()
            except ProgrammingError as erro_programacao:
                print(f"Erro ao fechar a conexão: {erro_programacao}")
            finally:
                self._conector = None