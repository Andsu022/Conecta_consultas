# Conecta Consulta

O **Conecta Consulta** é um projeto em desenvolvimento para cadastro de pacientes, usando Python e persistência local em SQLite.

## Visão Geral

Este repositório atualmente concentra a lógica principal em [backend/classes.py](backend/classes.py), onde a classe `Paciente` cria a tabela `Pacientes` e realiza o cadastro com validação simples de CPF.

A persistência é feita com a biblioteca padrão do Python, `sqlite3`, sem uso de framework web neste momento.

## 🚀 Tecnologias

- **Python 3.x**
- **SQLite** via `sqlite3`

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

No momento, o projeto não depende de pacotes externos para funcionar, então o arquivo [requirements.txt](requirements.txt) serve apenas como referência de ambiente e documentação.

```bash
pip install -r requirements.txt
```

### 3. Executar a aplicação

```bash
python backend/main.py
```

> Observação: o fluxo atual está centrado na manipulação do banco local e na classe `Paciente` em [backend/classes.py](backend/classes.py).

---

## 📝 Status do Projeto

O projeto está em desenvolvimento inicial, com foco no cadastro e validação de pacientes em banco SQLite local.
