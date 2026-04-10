# 🏨 Sistema de Hospedagem – Projeto Prático POO

Projeto prático de Programação Orientada a Objetos (POO) usando:

- **Frontend**: Streamlit  
- **Backend**: Python  
- **Banco de Dados**: MySQL  
- **Armazenamento adicional**: arquivos `.csv`

O sistema permite gerenciar **clientes**, **quartos** e **reservas** de um hotel, atendendo aos requisitos do enunciado:

> - Cliente (Nome, Telefone, E-mail, ID único)  
> - Quarto (Número, Tipo, Preço por diária, Status de disponibilidade)  
> - Reserva (Dono da reserva, Quarto reservado, Datas, Status)  
> - GerenciadorDeReservas com métodos para verificar disponibilidade, criar/modificar/cancelar reservas e listar reservas/clientes.  

---

## 🧱 Estrutura do Projeto

```text
Projeto Hotel/
  ├─ backend/
  │   ├─ models/
  │   │   ├─ __init__.py        # Exporta Cliente, Quarto, Reserva
  │   │   ├─ cliente.py         # Classe Cliente
  │   │   ├─ quarto.py          # Classe Quarto
  │   │   └─ reserva.py         # Classe Reserva
  │   ├─ __init__.py            # Marca 'backend' como pacote
  │   ├─ gerenciador_reservas.py# Classe GerenciadorDeReservas
  │   ├─ database.py            # Conexão e operações com MySQL
  │   └─ csv_utils.py           # Funções para ler/gravar CSV
  ├─ frontend/
  │   └─ app.py                 # Interface Streamlit
  ├─ csv_data/                  # (criada em tempo de execução) arquivos .csv
  ├─ requirements.txt
  └─ README.md
```

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit**
- **MySQL**
- **mysql-connector-python**
- **CSV (módulo padrão `csv` do Python)**

---

## 🗃️ Banco de Dados (MySQL)

### 1. Criar o banco de dados

No MySQL (Workbench ou terminal):

```sql
CREATE DATABASE IF NOT EXISTS hotel_db;
```

### 2. Tabelas utilizadas

O código cria/garante as tabelas automaticamente, mas a estrutura é:

```sql
-- Tabela clientes
CREATE TABLE IF NOT EXISTS clientes (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    nome      VARCHAR(100) NOT NULL,
    telefone  VARCHAR(20)  NOT NULL,
    email     VARCHAR(100) NOT NULL
);

-- Tabela quartos
CREATE TABLE IF NOT EXISTS quartos (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    numero       INT           NOT NULL UNIQUE,
    tipo         VARCHAR(20)   NOT NULL,
    preco_diaria DECIMAL(10,2) NOT NULL,
    status       VARCHAR(20)   NOT NULL DEFAULT 'disponivel'
);

-- Tabela reservas
CREATE TABLE IF NOT EXISTS reservas (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id    INT  NOT NULL,
    quarto_id     INT  NOT NULL,
    data_checkin  DATE NOT NULL,
    data_checkout DATE NOT NULL,
    status        VARCHAR(20) NOT NULL DEFAULT 'ativa',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (quarto_id)  REFERENCES quartos(id)
);
```

No arquivo `backend/database.py` estão as configurações de conexão:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "SUA_SENHA_AQUI",
    "database": "hotel_db"
}
```

---

## 📦 Instalação das Dependências

Na raiz do projeto:

```bash
pip install -r requirements.txt
```

Conteúdo de `requirements.txt`:

```text
streamlit
mysql-connector-python
```

---

## ▶️ Como Executar o Projeto

1. Certifique-se de que o MySQL está rodando e o banco `hotel_db` existe.
2. Na raiz do projeto (`Projeto Hotel/`), execute:

```bash
python -m streamlit run frontend/app.py
```

O navegador abrirá em algo como:

- `http://localhost:8501`

---

## 🧩 Classes e Responsabilidades

### Cliente (`backend/models/cliente.py`)

- Atributos:
  - `id`
  - `nome`
  - `telefone`
  - `email`
- Métodos:
  - `to_dict()` – usado para exportar para CSV e exibir em tabelas.

### Quarto (`backend/models/quarto.py`)

- Atributos:
  - `id`
  - `numero`
  - `tipo` (`single`, `double`, `suite`)
  - `preco_diaria`
  - `status` (`disponivel`, `ocupado`, `manutencao`)
- Métodos:
  - `to_dict()` – para CSV e exibição.

### Reserva (`backend/models/reserva.py`)

- Atributos:
  - `id`
  - `cliente_id`
  - `quarto_id`
  - `data_checkin`
  - `data_checkout`
  - `status` (`ativa`, `cancelada`, `concluida`)
- Métodos:
  - `calcular_total(preco_diaria)` – calcula valor total da reserva.
  - `to_dict()` – para CSV e exibição.

### GerenciadorDeReservas (`backend/gerenciador_reservas.py`)

Responsável por todas as regras de negócio:

- **Clientes**
  - `criar_cliente(nome, telefone, email)`
  - `listar_clientes()`
  - `buscar_cliente_por_id(id)`

- **Quartos**
  - `criar_quarto(numero, tipo, preco_diaria, status)`
  - `listar_quartos()`
  - `buscar_quarto_por_id(id)`

- **Reservas**
  - `verificar_disponibilidade(quarto_id, data_checkin, data_checkout)`
  - `criar_reserva(cliente_id, quarto_id, data_checkin, data_checkout)`
  - `modificar_reserva(reserva_id, novos_dados)`
  - `cancelar_reserva(reserva_id)`
  - `listar_reservas()`
  - `buscar_reserva_por_id(id)`

- **Exportação CSV**
  - `exportar_clientes_para_csv()`
  - `exportar_quartos_para_csv()`
  - `exportar_reservas_para_csv()`

### CSV (`backend/csv_utils.py`)

Funções de apoio para salvar e ler dados em `.csv`:

- `salvar_clientes_csv(lista_clientes)`
- `salvar_quartos_csv(lista_quartos)`
- `salvar_reservas_csv(lista_reservas)`
- `ler_csv(nome_arquivo)`

Os arquivos são salvos na pasta `csv_data/` (criada automaticamente):

- `csv_data/clientes.csv`
- `csv_data/quartos.csv`
- `csv_data/reservas.csv`

---

## 💻 Frontend (Streamlit)

Arquivo: `frontend/app.py`

Funcionalidades principais:

- **Cadastrar Cliente**
  - Formulário com: Nome, Telefone, E-mail.

- **Cadastrar Quarto**
  - Formulário com: Número, Tipo, Preço diária, Status.

- **Criar Reserva**
  - Seleciona cliente e quarto.
  - Informa datas de check-in/check-out.
  - Verifica disponibilidade antes de gravar.

- **Listar Clientes / Quartos / Reservas**
  - Exibição em tabelas (dataframe).

- **Cancelar / Modificar Reserva**
  - Seleciona uma reserva.
  - Cancela (muda status para `cancelada`) ou altera as datas.

- **Exportar para CSV**
  - Botões para exportar clientes, quartos e reservas para `.csv`.

---

## ✅ Requisitos do Enunciado Atendidos

- [x] Frontend com **Streamlit**
- [x] Backend em **Python**
- [x] Banco de dados **MySQL**
- [x] Implementação de **módulos** (pacotes e arquivos separados)
- [x] Armazenamento de informações em **planilhas `.csv`**
- [x] Classes mínimas: `Cliente`, `Quarto`, `Reserva`, `GerenciadorDeReservas`
- [x] Métodos no `GerenciadorDeReservas`:
  - verificar disponibilidade
  - criar, modificar e cancelar reservas
  - listar reservas e informações de clientes

---

## 📝 Observações

- O projeto foi desenvolvido em Windows 11, usando:
  - Python 3.x
  - Streamlit
  - MySQL (porta padrão 3306, usuário `root`)
- Caso a senha do MySQL seja diferente, ajustar em `backend/database.py` em `DB_CONFIG`.
