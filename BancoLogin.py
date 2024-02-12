import sqlite3

class BancoDados:
    def __init__(self):
        """Inicia a conexão com o banco de dados, além de criar uma tabela e uma trigger"""
        try:
            self.conector = sqlite3.connect("BancoDados.db")
            self.cursor = self.conector.cursor()
        except:
            raise Exception("Não foi possivel se conectar no banco de dados")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Registros_Login (
                id INTEGER PRIMARY KEY,
                nome_de_usuario VARCHAR(255) NOT NULL,
                e_mail VARCHAR(50) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL,
                salt VARCHAR(50) NOT NULL,
                data_hora DATETIME
            );
        """)

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'definir_data_hora'")

        if not self.cursor.fetchone():
            self.cursor.execute(""" 
                CREATE TRIGGER definir_data_hora
                AFTER INSERT ON Registros_Login
                FOR EACH ROW
                BEGIN
                    UPDATE Registros_Login SET data_hora = datetime("now", "localtime") WHERE id = NEW.id;
                END;
            """)

            self.conector.commit()

    def fechar_conexao(self):
        """Encerra a conexão com o banco de dados"""
        self.cursor.close()
        self.conector.close()