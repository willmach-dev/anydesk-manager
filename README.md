# Sistema de Gerenciamento de Clientes AnyDesk

Este é um sistema web desenvolvido em Python usando Flask para gerenciar clientes AnyDesk e usuários do sistema.

## Funcionalidades

- Sistema de login com diferentes níveis de acesso (admin e usuário)
- Gerenciamento de usuários (CRUD)
- Gerenciamento de clientes AnyDesk (CRUD)
- Interface moderna e responsiva usando Bootstrap
- Botões para copiar ID e senha do AnyDesk

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório ou baixe os arquivos
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

1. O sistema já vem com um usuário administrador padrão:
   - Usuário: admin
   - Senha: admin

2. É recomendado alterar a senha do administrador após o primeiro acesso

## Executando o Sistema

1. Execute o arquivo principal:
```bash
python app.py
```

2. Acesse o sistema em seu navegador:
```
http://localhost:5000
```

## Estrutura do Projeto

- `app.py`: Arquivo principal com as rotas e modelos
- `templates/`: Pasta com os templates HTML
  - `base.html`: Template base com a estrutura comum
  - `entrar.html`: Página de login
  - `painel_admin.html`: Painel do administrador
  - `painel_usuario.html`: Painel do usuário
  - `gerenciar_usuarios.html`: Gerenciamento de usuários
  - `clientes_anydesk.html`: Lista de clientes AnyDesk
  - `adicionar_cliente_anydesk.html`: Formulário para adicionar/editar clientes

## Segurança

- As senhas dos usuários são armazenadas com hash
- Acesso restrito baseado em nível de usuário
- Proteção contra CSRF
- Sessões seguras

## Contribuição

Sinta-se à vontade para contribuir com o projeto através de pull requests ou reportando issues. 