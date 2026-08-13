# Conecta Consulta

O **Conecta Consulta** é um sistema de agendamento de consultas médicas e gestão de cadastros (pacientes e médicos), desenvolvido em Python com persistência local em SQLite e API REST construída com FastAPI.

## Visão Geral

O projeto está estruturado em:
- **[backend/classes.py](backend/classes.py)**: Camada de regras de negócio e manipulação do banco de dados SQLite (`databank.db`), contemplando as classes:
  - `Paciente`: Criação de tabela, verificação de duplicidade por CPF/Email, cadastro e listagem.
  - `Medico`: Criação de tabela, verificação de duplicidade por CRM, cadastro e listagem.
  - `Consulta`: Criação de tabela com relacionamentos (Foreign Keys para Paciente e Médico), verificação de disponibilidade de horário e agendamento.
- **[backend/main.py](backend/main.py)**: API REST desenvolvida com FastAPI e Pydantic para validação de dados e comunicação HTTP, contando com suporte a CORS.

## 🚀 Tecnologias

- **Python 3.10+**
- **FastAPI** (API REST backend)
- **Pydantic** (Validação de schemas e dados de entrada)
- **Uvicorn** (Servidor ASGI)
- **SQLite3** (Persistência de dados local)

## 📁 Estrutura do Projeto

```text
Conecte_Consulta/
├── backend/
│   ├── database/         # Armazenamento local do banco de dados (databank.db)
│   ├── classes.py        # Classes (Paciente, Medico, Consulta) e operações SQLite
│   └── main.py           # Servidor FastAPI (rotas REST, validação Pydantic e CORS)
├── requirements.txt      # Dependências do projeto
├── .gitignore
└── README.md
```

## 🛠️ Como Executar

### Pré-requisitos

- Python 3.10 ou superior instalado.

### 1. Criar e ativar o ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv backend/venv
.\backend\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
```

### 2. Instalar dependências

Instale as dependências listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Executar a aplicação (Servidor FastAPI)

Na raiz do projeto, execute o Uvicorn para subir o servidor backend:

```bash
uvicorn backend.main:app --reload
```

A API estará acessível em `http://127.0.0.1:8000`.

### 📌 Documentação Interativa (Swagger / OpenAPI)

Após iniciar o servidor, você pode acessar e testar as rotas via documentação interativa:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🔗 Endpoints Principais

- `POST /paciente` — Cadastrar um novo paciente.
- `GET /paciente` — Listar todos os pacientes cadastrados.
- `POST /medico` — Cadastrar um novo médico.

---

## 📝 Status do Projeto

O projeto conta com a estrutura completa de classes e banco de dados para Pacientes, Médicos e Consultas, além da integração inicial de rotas HTTP com FastAPI. Em desenvolvimento contínuo.

