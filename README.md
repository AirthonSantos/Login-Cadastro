# Login-Cadastro

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://github.com/AirthonSantos/Login-Cadastro/blob/master/LICENSE)

## Sobre este projeto

Esse é um projeto pessoal criado para integrar meu portfólio e colocar em prática certos conceitos que aprendi. Refinei esse projeto o máximo que pude. Importante dizer também que esse é o meu primeiro projeto no GitHub, portanto estou aberto a qualquer conselho.

A aplicação em questão apresenta uma tela de login com a opção do usuário se autenticar. Além disso, o usuário também pode efetuar o cadastro em outra janela, caso o mesmo não possua.

Esse projeto foi feito com tkinter, sqlite3, Pillow, re, hashlib e secrets.

- O tkinter foi usado para criar a interface gráfica;
- O sqlite3 para criar o banco de dados;
- O Pillow para importar e tratar algumas imagens;
- O hashlib para calcular a hash da senha do usuário;
- O re para criar uma expressão regular para validar alguns campos, como a senha e o email;
- O secrets serve para gerar um valor aleatório que é concatenado com a senha do usuário antes de calcular a hash.

Além disso, busquei implementar diversos recursos que, inicialmente, podem passar despercebidos. Esses recursos incluem:

- Bloqueio de login, o login é bloqueado após certas tentativas mal sucedidas, com o propósito de prevenir ataques de força bruta;
- Modo claro e escuro;
- A senha do usuário fica escondida (só aparece \*);
- A hash da senha do usuario é armazenada no banco de dados ao invés de armazenar diretamente a senha;
- O usuário só pode cadastrar um e-mail válido, ou seja, precisa ter alguma coisa antes e depois do "@" e terminar com ".com";
- Se o e-mail que o usuário está tentando cadastrar já existir no banco de dados, a operação é interrompida e uma mensagem de erro é exibida;
- As queries do SQL utilizam placeholders que servem para impedir ataques SQL Injection;
- O salt permite aumentar a segurança do hash da senha, dificultando ataques de dicionário e força bruta;
- Implementei um recurso que encerra o programa, incluindo a conexão com o banco de dados ao fechar a tela de cadastro, garantindo o encerramento correto da aplicação. Isso foi necessário porque, quando a tela de cadastro é aberta, a tela de login é apenas ocultada, mas continua em execução. Se a tela de cadastro fosse fechada, a tela de login continuaria oculta e o usuário não poderia encerrar a aplicação corretamente. Por isso, foi necessário implementar esse recurso;
- No banco de dados, há um campo denominado "data_hora" que armazena o registro da data e hora de cadastro do usuário. Essa informação é crucial para auxiliar nos registros de log;
- A senha deve atender às diretrizes de uma senha forte:
    - Possuir no mínimo 8 caracteres;
    - Precisa ter uma mistura de letras maiúsculas, minúsculas, números e símbolos (!, @, #, $, %, &, \_).
- Por fim, resolvi seguir algumas práticas da PEP-8.

Vale ressaltar que o codificador usado nesse projeto foi o UTF-8.

## Layout

### Tela de Login

<div style="display: flex;">
    <img src="./Imagens_README/telalogin1.png" style="flex: 1;">
    <img src="./Imagens_README/telalogin2.png" style="flex: 1;">
</div>

### Tela de Cadastro

<div style="display: flex;">
    <img src="./Imagens_README/telacadastro1.png" style="flex: 1;">
    <img src="./Imagens_README/telacadastro2.png" style="flex: 1;">
</div>

## Como executar

### Pré-requisitos

Para esse projeto é necessário ter o python3 (Versão 3.11 ou superior) e as bibliotecas citadas anteriormente. Praticamente todas as bibliotecas citadas já integram o Python, com exceção do Pillow. Portanto, para instalá-lo usamos o comando:

```bash
pip install Pillow
```

Obs: Este projeto foi desenvolvido para ser executado no Windows 10. Se você estiver usando outro sistema operacional, algumas funcionalidades podem não funcionar corretamente.

### Execução

Para executar esse projeto, basta executar o comando `git clone` nesse repositório, entrar no diretório "Login-Cadastro" e executar o código.

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
