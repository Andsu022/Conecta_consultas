# Conecta Consulta

O **Conecta Consulta** é um sistema para agendamento e gerenciamento de consultas médicas rápidas.

## 🚀 Tecnologias

- **Python 3.x**
- **FastAPI** / **Uvicorn**
- **SQLite**
- **SQLModel** / **Pydantic**

## 📁 Estrutura do Projeto

```
Conecte_Consulta/
├── backend/
│   ├── databank/         # Diretório do banco de dados SQLite (databank.db)
│   ├── classes.py        # Definição de classes e modelos de dados
│   ├── main.py           # Ponto de entrada da aplicação backend
│   └── requirements.txt  # Dependências Python do projeto
├── .gitignore
└── README.md
```

## 🛠️ Como Executar o Projeto

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

### 2. Instalar as dependências

```bash
pip install -r backend/requirements.txt
```

### 3. Executar a aplicação

```bash
python backend/main.py
```

*(Se estiver utilizando o Uvicorn diretamente: `uvicorn backend.main:app --reload`)*

---

## 📝 Licença
Este projeto está em desenvolvimento.
