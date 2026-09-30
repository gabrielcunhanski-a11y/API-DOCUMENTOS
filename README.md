## Instalação

Na raiz do projeto:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dentro da pasta `API-GEOSITE` também há um `requirements.txt` caso queira instalar dependências isoladas para a API:

```bash
cd API-GEOSITE
pip install -r requirements.txt
```

## Execução

```bash
cd API-GEOSITE
python app.py
```

A aplicação será iniciada em:

```bash
http://localhost:5000
```

## Endpoints principais

### Autenticação

- `POST /auth/forgot-password` — solicita recuperação de senha
- `POST /auth/reset-password` — redefine a senha com o token recebido

### Usuários

- `POST /users/register` — cadastro de usuário
- `POST /users/login` — login do usuário
- `GET /users/me` — dados do usuário autenticado
- `PUT /users/me` — atualizar perfil do usuário autenticado
- `GET /users/` — listar todos usuários (apenas admin)
- `GET /users/<id>` — buscar usuário por id (apenas admin)
- `PUT /users/<id>` — atualizar usuário (apenas admin)
- `PATCH /users/<id>/deactivate` — desativar usuário (apenas admin)
- `PATCH /users/<id>/activate` — ativar usuário (apenas admin)

### Cidades

- `GET /cities/` — listar cidades
- `GET /cities/<slug>` — buscar cidade por slug
- `POST /cities/` — criar cidade (apenas admin)
- `PUT /cities/<slug>` — atualizar cidade (apenas admin)
- `DELETE /cities/<slug>` — remover cidade (apenas admin)

### Documentos

- `POST /documentos/` — criar documento
- `GET /documentos/` — listar documentos
- `GET /documentos/me` — listar documentos do usuário autenticado
- `GET /documentos/<id>` — buscar documento por id
- `PUT /documentos/<id>` — atualizar documento
- `DELETE /documentos/<id>` — deletar documento

## Segurança

- senhas são armazenadas com hash Argon2
- autenticação usa JWT
- chaves e credenciais ficam em variáveis de ambiente
- uploads e arquivos de ambiente ficam fora do controle de versão

## Observações

- os arquivos de upload são salvos na pasta `API-GEOSITE/uploads/`
- o banco SQLite local também pode ser usado em ambiente de desenvolvimento, dependendo da configuração do projeto
- para produção, prefira credenciais reais do PostgreSQL e uma `SECRET_KEY` forte e exclusiva

## Contribuição

1. crie uma branch
2. faça suas alterações
3. teste localmente
4. abra um pull request
