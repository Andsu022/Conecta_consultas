# Conecta Consulta

O **Conecta Consulta** é um projeto em desenvolvimento para cadastro de pacientes, usando Python e persistência local em SQLite.

## Visão Geral

Este repositório atualmente concentra a lógica principal em [backend/classes.py](backend/classes.py), onde a classe `Paciente` cria a tabela `Pacientes` e realiza o cadastro com validação simples de CPF.

A persistência é feita com a biblioteca padrão do Python, `sqlite3`, sem uso de framework web neste momento.

## 🚀 Tecnologias

- **Python 3.x**
- **SQLite** via `sqlite3`
- **FastAPI** (opcional para API local)
- **Uvicorn** (ASGI server)

## 📁 Estrutura do Projeto

```text
Conecte_Consulta/
├── backend/
│   ├── databank/         # Diretório de armazenamento local do banco
│   ├── classes.py        # Lógica de criação da tabela e cadastro de pacientes
│   └── main.py           # Arquivo de entrada atual do backend
├── requirements.txt      # Arquivo de dependências do projeto
├── .gitignore
└── README.md
```

## 🛠️ Como Executar

### Pré-requisitos

- Python 3.10 ou superior instalado.

### 1. Criar e ativar o ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências
Instale as dependências recomendadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Verificação rápida (FastAPI)

Após ativar o `venv`, confirme que `fastapi` e `uvicorn` estão instalados:

```powershell
.\venv\Scripts\Activate.ps1
pip show fastapi
pip show uvicorn
python -c "import fastapi; print(fastapi.__version__)"
```

Para testar manualmente um servidor ASGI (exemplo local):

```powershell
# se houver um app FastAPI em backend/main.py exposto como variable 'app'
python -m uvicorn backend.main:app --reload
# ou, para um pequeno teste rápido, crie um módulo temporário com um app e rode uvicorn
```

### 3. Executar a aplicação

```bash
python backend/main.py
```

> Observação: o fluxo atual está centrado na manipulação do banco local e na classe `Paciente` em [backend/classes.py](backend/classes.py).

---

## 📝 Status do Projeto

O projeto está em desenvolvimento inicial, com foco no cadastro e validação de pacientes em banco SQLite local.
