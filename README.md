# Conecta Consultas

O **Conecta Consultas** é um sistema de agendamento de consultas médicas e gestão de cadastros (pacientes e médicos), desenvolvido em Python com persistência local em SQLite, API REST construída com FastAPI utilizando injeção de dependências e tipagem com Pydantic, além de uma interface web em desenvolvimento.

## Visão Geral

O projeto é estruturado de forma modular:
- **[backend/db.py](backend/db.py)**: Gerenciamento da conexão com o banco de dados SQLite (`database/databank.db`), ativação de chaves estrangeiras (`PRAGMA foreign_keys = ON`), generator de conexões (`get_connection`) e inicialização do schema (`init_db`) com tabelas e índices parciais únicos de horário.
- **[backend/classes.py](backend/classes.py)**: Camada de regras de negócio desacoplada que recebe a conexão SQLite via injeção de dependência e implementa as operações para:
  - `Paciente`: Cadastro com verificação de duplicidade por CPF/E-mail e listagem de pacientes.
  - `Medico`: Cadastro com verificação de duplicidade por CRM e listagem de médicos.
  - `Consulta`: Agendamento com validação de disponibilidade de data/horário por médico e listagem de consultas.
- **[backend/main.py](backend/main.py)**: API REST desenvolvida com FastAPI, gerenciamento do ciclo de vida com `lifespan`, injeção de dependências (`Depends`), validação de esquemas via Pydantic e configuração de middleware CORS.
- **[docs/requirements.md](docs/requirements.md)**: Documentação de requisitos do sistema, perfis de usuários e regras identificadas.
- **[interface/](interface/)**: Estrutura da interface frontend web ([index.html](interface/index.html), [style.css](interface/style.css), [app.js](interface/app.js)) para interação do usuário final.
- **[tests/](tests/)**: Testes automatizados e utilitários de banco:
  - [api_test.py](tests/api_test.py): Testes unitários das rotas e validações da API via `unittest`.
  - [ver_banco.py](tests/ver_banco.py): Script de consulta rápida à estrutura de tabelas criadas no SQLite.

## 🚀 Tecnologias

- **Python 3.10+**
- **FastAPI** (Construção da API REST assíncrona)
- **Pydantic** (Validação de dados, esquemas e tipagem)
- **Uvicorn** (Servidor ASGI leve e de alto desempenho)
- **SQLite3** (Persistência de dados relacional local com suporte a foreign keys e índices parciais)
- **Unittest** (Testes automatizados integrados)
- **HTML5 / CSS3 / JavaScript** (Interface frontend web)

## 📁 Estrutura do Projeto

```text
Conecta_Consultas/
├── backend/
│   ├── database/         # Armazenamento local do banco de dados (databank.db)
│   ├── classes.py        # Classes de regras de negócio (Paciente, Medico, Consulta)
│   ├── db.py             # Conexão SQLite, generator de sessões e inicialização de tabelas
│   └── main.py           # Servidor FastAPI (rotas REST, injeção de dependência e CORS)
├── docs/
│   └── requirements.md   # Especificação e requisitos do sistema
├── interface/
│   ├── app.js            # Lógica frontend e integração com a API
│   ├── index.html        # Estrutura HTML da interface
│   └── style.css         # Folha de estilos (CSS)
├── tests/
│   ├── api_test.py       # Testes unitários das rotas da API com unittest
│   └── ver_banco.py      # Script de inspeção do schema SQLite
├── .gitignore            # Arquivos ignorados pelo controle de versão Git
├── README.md             # Documentação principal do projeto
└── requirements.txt      # Dependências do projeto Python
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

Na raiz do projeto, execute o Uvicorn para iniciar o servidor backend:

```bash
uvicorn backend.main:app --reload
```

Ou utilizando o módulo Python:

```bash
python -m uvicorn backend.main:app --reload
```

A API estará acessível em `http://127.0.0.1:8000`.

### 📌 Documentação Interativa (Swagger / OpenAPI)

Com o servidor em execução, acesse a documentação interativa para visualizar e testar todos os endpoints:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🧪 Executando os Testes

Para executar a suíte de testes unitários:

```bash
python -m unittest discover -s tests -p "*test*.py"
```

Para inspecionar as tabelas criadas no banco SQLite local:

```bash
python tests/ver_banco.py
```

## 🔗 Endpoints Principais

### Pacientes
- `POST /paciente` — Cadastrar um novo paciente.
  - **Status 201**: Retorna `{"id": <id>, "message": "Paciente cadastrado com sucesso"}`.
  - **Status 409**: Se CPF ou E-mail já estiverem cadastrados.
- `GET /paciente` — Listar todos os pacientes cadastrados.

### Médicos
- `POST /medico` — Cadastrar um novo médico.
  - **Status 201**: Retorna `{"message": "Médico cadastrado com sucesso"}`.
  - **Status 409**: Se CRM já estiver cadastrado.
- `GET /medico` — Listar todos os médicos cadastrados.

### Consultas
- `POST /consulta` — Agendar uma nova consulta médica.
  - **Campos**: `paciente_id`, `medico_id`, `data_consulta` (YYYY-MM-DD), `hora_consulta` (HH:MM:SS), `observacao` (opcional), `situacao` (`'agendada'` | `'realizada'` | `'cancelada'`).
  - **Status 201**: Retorna `{"message": "Consulta agendada com sucesso"}`.
  - **Status 404**: Se o paciente ou médico referenciado não existir.
  - **Status 409**: Se a data e o horário já estiverem ocupados para o médico selecionado.
- `GET /consulta/{id}` — Listar consultas registradas no sistema.

---

## 🔒 Regras de Negócio e Integridade de Dados

- **Pacientes**: Unicidade estrita garantida para CPF e e-mail no nível de banco de dados (`UNIQUE`).
- **Médicos**: Unicidade garantida por CRM (`UNIQUE`).
- **Consultas**:
  - Chaves estrangeiras ativas vinculando a consulta a um paciente e a um médico existentes.
  - Índices únicos parciais no SQLite (`ux_medico_slot` e `ux_paciente_slot`) impedindo agendamentos duplicados no mesmo dia e horário para o mesmo médico ou paciente (exceto consultas canceladas).
  - Situação restrita via validação e constraint `CHECK` para os valores permitidos: `'agendada'`, `'realizada'`, `'cancelada'`.

---

## 📝 Status do Projeto

O projeto conta com:
- [x] Camada de persistência modular com SQLite e injeção de dependências em `backend/db.py`.
- [x] Regras de negócio desacopladas em `backend/classes.py`.
- [x] API REST com FastAPI e documentação OpenAPI ativa em `backend/main.py`.
- [x] Endpoints para Pacientes, Médicos e Consultas com validações e tratamento de erros HTTP.
- [x] Testes unitários automatizados em `tests/api_test.py`.
- [ ] Conexão e integração completa com a interface web (`interface/`).
