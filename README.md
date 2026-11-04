# Conecta Consultas

O **Conecta Consultas** é um sistema de agendamento de consultas médicas e gestão de cadastros (pacientes e médicos), desenvolvido em Python com persistência local em SQLite, API REST construída com FastAPI utilizando arquitetura modular, injeção de dependências e validação com Pydantic, além de uma interface web em desenvolvimento.

## Visão Geral

O projeto é estruturado de forma modular e desacoplada:
- **[backend/routes/](backend/routes/)**: Roteadores modulares da API (`APIRouter`) separados por domínio:
  - `route_paciente.py`: Endpoints de cadastro e listagem de pacientes.
  - `route_medico.py`: Endpoints de cadastro e listagem de médicos.
  - `route_consulta.py`: Endpoints de agendamento e consulta por identificador (`ID`).
- **[backend/schemas/](backend/schemas/)**: Modelos de dados e validação de entrada com Pydantic:
  - `schema_paciente.py`: Validação de dados de pacientes (limites de tamanho, normalização e validação de CPF para 11 dígitos, e-mail com `EmailStr`).
  - `schema_medico.py`: Validação de dados cadastrais de médicos (nome, CRM e especialidade).
  - `schema_consulta.py`: Validação dos dados de agendamento de consultas com datas, horários e tipos literais (`Literal['agendada', 'realizada', 'cancelada']`).
- **[backend/dependencies.py](backend/dependencies.py)**: Provedores de injeção de dependência (`Depends`) que gerenciam a conexão com o banco e fornecem as instâncias dos serviços (`get_paciente_service`, `get_medico_service`, `get_consulta_service`).
- **[backend/classes.py](backend/classes.py)**: Camada de regras de negócio e persistência que recebe a conexão SQLite e implementa as operações:
  - `Paciente`: Cadastro com verificação de duplicidade por CPF/E-mail e listagem de pacientes.
  - `Medico`: Cadastro com verificação de duplicidade por CRM e listagem de médicos.
  - `Consulta`: Agendamento com validação de chaves estrangeiras, restrições de horários e busca detalhada por ID.
- **[backend/db.py](backend/db.py)**: Gerenciamento da conexão com o SQLite (`database/databank.db`), ativação de chaves estrangeiras (`PRAGMA foreign_keys = ON`), modo WAL (`PRAGMA journal_mode = WAL`), generator de conexões (`get_connection`) e inicialização do schema (`init_db`) com tabelas e índices parciais únicos de horário.
- **[backend/main.py](backend/main.py)**: Ponto de entrada da aplicação FastAPI, gerenciamento do ciclo de vida com `lifespan` (`init_db`), configuração de CORS e registro dos roteadores.
- **[docs/requirements.md](docs/requirements.md)**: Documentação de requisitos do sistema, perfis de usuários e regras de negócio.
- **[interface/](interface/)**: Estrutura da interface frontend web ([index.html](interface/index.html), [style.css](interface/style.css), [app.js](interface/app.js)) para interação do usuário final.
- **[tests/](tests/)**: Testes automatizados e utilitários de banco:
  - [api_test.py](tests/api_test.py): Testes unitários das rotas da API com `unittest`.
  - [ver_banco.py](tests/ver_banco.py): Script utilitário para inspeção do schema e tabelas no SQLite.

## 🚀 Tecnologias

- **Python 3.10+**
- **FastAPI** (Construção da API REST moderna e assíncrona)
- **Pydantic & Email-Validator** (Validação rigorosa de dados, esquemas e tipagem)
- **Uvicorn** (Servidor ASGI leve e de alto desempenho)
- **SQLite3** (Persistência relacional local com chaves estrangeiras ativas e índices parciais)
- **Unittest** (Testes automatizados integrados)
- **HTML5 / CSS3 / JavaScript** (Interface frontend web)

## 📁 Estrutura do Projeto

```text
Conecta_Consultas/
├── backend/
│   ├── database/         # Armazenamento local do banco de dados (databank.db)
│   ├── routes/           # Rotas da API divididas por domínio (APIRouter)
│   │   ├── route_consulta.py
│   │   ├── route_medico.py
│   │   └── route_paciente.py
│   ├── schemas/          # Modelos de validação de dados com Pydantic
│   │   ├── schema_consulta.py
│   │   ├── schema_medico.py
│   │   └── schema_paciente.py
│   ├── classes.py        # Camada de regras de negócio (Paciente, Medico, Consulta)
│   ├── db.py             # Conexão SQLite, generator de sessões e schema
│   ├── dependencies.py   # Provedores de injeção de dependência do FastAPI
│   └── main.py           # Configuração do FastAPI, lifespan, CORS e roteadores
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
├── LICENSE               # Licença MIT do projeto
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

### Pacientes (`/paciente`)
- `POST /paciente` — Cadastrar um novo paciente.
  - **Body (JSON)**: `nome` (str, 2 a 120 caracteres), `cpf` (str, normalizado para 11 dígitos), `data_nascimento` (date: `YYYY-MM-DD`), `telefone` (str, 8 a 20 caracteres), `email` (EmailStr válido).
  - **Status 201**: Retorna `{"id": <id>, "message": "Paciente cadastrado com sucesso"}`.
  - **Status 409**: Se CPF ou E-mail já estiverem cadastrados.
  - **Status 422**: Erro de validação nos dados fornecidos.
- `GET /paciente` — Listar todos os pacientes cadastrados.
  - **Status 200**: Retorna lista de objetos com os dados dos pacientes.

### Médicos (`/medico`)
- `POST /medico` — Cadastrar um novo médico.
  - **Body (JSON)**: `nome` (str), `crm` (str), `especialidade` (str).
  - **Status 201**: Retorna `{"id": <id>, "message": "Médico cadastrado com sucesso"}`.
  - **Status 409**: Se CRM já estiver cadastrado.
  - **Status 422**: Erro de validação nos dados fornecidos.
- `GET /medico` — Listar todos os médicos cadastrados.
  - **Status 200**: Retorna lista de objetos com os dados dos médicos.

### Consultas (`/consulta`)
- `POST /consulta` — Agendar uma nova consulta médica.
  - **Body (JSON)**: `paciente_id` (int), `medico_id` (int), `data_consulta` (date: `YYYY-MM-DD`), `hora_consulta` (time: `HH:MM:SS`), `observacao` (str | null, opcional), `situacao` (`'agendada'` | `'realizada'` | `'cancelada'`, padrão: `'agendada'`).
  - **Status 201**: Retorna `{"id": <id>, "message": "Consulta agendada com sucesso"}`.
  - **Status 404**: Se o paciente ou médico referenciado não existir (`"Paciente ou médico informado não existe"`).
  - **Status 409**: Se houver conflito de horário para o médico ou para o paciente selecionado.
- `GET /consulta/{id}` — Buscar consulta específica por ID.
  - **Status 200**: Retorna os detalhes da consulta encontrada.
  - **Status 404**: Se a consulta não for encontrada (`"Consulta não encontrada !"`).

---

## 🔒 Regras de Negócio e Integridade de Dados

- **Pacientes**: Unicidade garantida para CPF e E-mail no nível de banco de dados (`UNIQUE`) e validação de formato via Pydantic.
- **Médicos**: Unicidade garantida por CRM (`UNIQUE`).
- **Consultas**:
  - Chaves estrangeiras ativas vinculando a consulta a um paciente e a um médico existentes.
  - Índices únicos parciais no SQLite (`ux_medico_slot` e `ux_paciente_slot`) impedindo agendamentos duplicados no mesmo dia e horário tanto para o mesmo médico quanto para o mesmo paciente (exceto consultas com situação `'cancelada'`).
  - Situação restrita via validação e constraint `CHECK` para os valores permitidos: `'agendada'`, `'realizada'`, `'cancelada'`.
- **Retorno Padronizado**: Operações de criação retornam o identificador (`id`) gerado no banco de dados para facilitar a integração com o frontend.

---

## 📝 Status do Projeto

O projeto conta com:
- [x] Camada de persistência modular com SQLite e injeção de dependências em `backend/db.py`.
- [x] Regras de negócio desacopladas em `backend/classes.py`.
- [x] Arquitetura modular de rotas com `APIRouter` em `backend/routes/`.
- [x] Esquemas e validação de entrada separados em `backend/schemas/`.
- [x] Provedores de injeção de dependência desacoplados em `backend/dependencies.py`.
- [x] API REST com FastAPI e documentação OpenAPI ativa em `backend/main.py`.
- [x] Endpoints para Pacientes, Médicos e Consultas com validações e tratamento de erros HTTP.
- [x] Testes unitários automatizados em `tests/api_test.py`.
- [ ] Conexão e integração completa com a interface web (`interface/`).
