# Login-Cadastro

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://github.com/AirthonSantos/Login-Cadastro/blob/master/LICENSE)

## Sobre este projeto

Esse é um projeto pessoal criado para integrar meu portfólio e colocar em prática certos conceitos que aprendi. Refinei esse projeto o máximo que pude. Importante dizer também que esse é o meu primeiro projeto no GitHub, portanto estou aberto a qualquer conselho.

A aplicação apresenta uma tela de login. Caso o usuário não possua uma conta, ele pode se cadastrar em outra janela. Além disso, todos os dados são armazenados em um banco de dados local.

Esse projeto foi desenvolvido utilizando as seguintes bibliotecas e módulos:

- **Tkinter**: utilizado para criar a interface gráfica.
- **SQLite3**: usado para gerenciar o banco de dados.
- **Pillow**: utilizado para importar e processar algumas imagens.
- **Hashlib**: responsável por calcular a hash da senha do usuário.
- **Re:** utilizado para criar expressões regulares que validam campos como senha e e-mail.
- **Secrets**: utilizado para gerar um valor aleatório que é concatenado à senha do usuário antes do cálculo da hash.

Além disso, busquei implementar diversos recursos que, inicialmente, podem passar despercebidos. Esses recursos incluem:

- **Bloqueio de login**: O acesso é bloqueado após três tentativas malsucedidas, prevenindo ataques de força bruta.
- **Modo claro e escuro**: O usuário pode alternar entre os modos de visualização.
- **Ocultação da senha**: A senha é exibida como asteriscos (*).
- **Armazenamento seguro de senhas**: A hash da senha é armazenada no banco de dados, em vez da senha em texto claro.
- **Validação de e-mail**: O usuário só pode cadastrar um e-mail válido, que deve incluir um nome de usuário, seguido pelo nome de domínio e pelo domínio de nível superior (TLD).
- **Verificação de e-mail duplicado**: Se o e-mail já existir no banco de dados, a operação é interrompida e uma mensagem de erro é exibida.
- **Proteção contra SQL Injection**: As queries SQL utilizam placeholders para evitar esse tipo de ataque.
- **Uso de salt**: O salt aumenta a segurança do hash da senha, dificultando ataques de dicionário e força bruta.
- **Registro de data e hora**: Um campo denominado "data_hora" no banco de dados armazena a data e hora de cadastro do usuário, essencial para registros de log.
- **Diretrizes de senha forte**: A senha deve ter no mínimo 8 caracteres e incluir uma mistura de letras maiúsculas, minúsculas, números e símbolos (!, @, #, $, %, &, _).
- **Práticas de codificação**: Segui algumas diretrizes da PEP-8.

Vale ressaltar que o codificador utilizado neste projeto foi o UTF-8.

## Layout

### Tela de Login

<div align="center">
    <img width=49% src="./Imagens_README/telalogin1.png">
    <img width=49% src="./Imagens_README/telalogin2.png">
</div>

### Tela de Cadastro

<div align="center">
    <img width=49% src="./Imagens_README/telacadastro1.png">
    <img width=49% src="./Imagens_README/telacadastro2.png">
</div>

## Como executar

### Pré-requisitos

É necessário ter o python3 (Versão 3.11 ou superior) e as bibliotecas citadas anteriormente. Praticamente todas as bibliotecas citadas já integram o Python, com exceção do Pillow. Portanto, para instalá-lo usamos o comando:

```bash
pip install Pillow
```

Obs: Este projeto foi desenvolvido para ser executado no Windows 10. Se você estiver usando outro sistema operacional, algumas funcionalidades podem não funcionar corretamente.

### Execução

Basta executar o comando `git clone` nesse repositório, entrar no diretório "Login-Cadastro" e executar o código.

```bash
# Clona esse repositorio
git clone https://github.com/AirthonSantos/Login-Cadastro

# Entra no diretorio
cd "Login-Cadastro"

# Executa o código
python "tela_de_login.py"
```

# Autor

Airthon Santos

https://www.linkedin.com/in/airthonsantos/
