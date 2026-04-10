import mysql.connector
from mysql.connector import Error

# ─────────────────────────────────────────────────────
# CONFIGURAÇÕES DE CONEXÃO COM O MYSQL
# ─────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "Senha",
    "database": "hotel_db"
}

# ─────────────────────────────────────────────────────
# FUNÇÃO: CONECTAR AO BANCO
# ─────────────────────────────────────────────────────
def conectar():
    """
    Abre e retorna uma conexão com o banco de dados MySQL.
    Retorna None se falhar.
    """
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        return conexao
    except Error as e:
        print(f"[ERRO] Não foi possível conectar ao banco: {e}")
        return None

# ─────────────────────────────────────────────────────
# FUNÇÃO: CRIAR TABELAS
# Roda toda vez que o sistema inicia.
# Se as tabelas já existirem, não faz nada.
# ─────────────────────────────────────────────────────
def criar_tabelas():
    """
    Cria as tabelas clientes, quartos e reservas
    no banco de dados, caso ainda não existam.
    """
    conexao = conectar()
    if conexao is None:
        print("[ERRO] Não foi possível criar as tabelas.")
        return

    cursor = conexao.cursor()

    # ── Tabela: clientes ──────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id        INT AUTO_INCREMENT PRIMARY KEY,
            nome      VARCHAR(100) NOT NULL,
            telefone  VARCHAR(20)  NOT NULL,
            email     VARCHAR(100) NOT NULL
        )
    """)

    # ── Tabela: quartos ───────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quartos (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            numero       INT           NOT NULL UNIQUE,
            tipo         VARCHAR(20)   NOT NULL,
            preco_diaria DECIMAL(10,2) NOT NULL,
            status       VARCHAR(20)   NOT NULL DEFAULT 'disponivel'
        )
    """)

    # ── Tabela: reservas ──────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id    INT  NOT NULL,
            quarto_id     INT  NOT NULL,
            data_checkin  DATE NOT NULL,
            data_checkout DATE NOT NULL,
            status        VARCHAR(20) NOT NULL DEFAULT 'ativa',
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (quarto_id)  REFERENCES quartos(id)
        )
    """)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("[OK] Tabelas verificadas/criadas com sucesso!")


# ─────────────────────────────────────────────────────
# FUNÇÃO: EXECUTAR INSERT / UPDATE / DELETE
# ─────────────────────────────────────────────────────
def executar_query(query: str, valores: tuple = ()):
    """
    Executa comandos que modificam o banco
    (INSERT, UPDATE, DELETE).
    Retorna o ID do último registro inserido,
    ou None em caso de erro.
    """
    conexao = conectar()
    if conexao is None:
        return None

    cursor = conexao.cursor()
    try:
        cursor.execute(query, valores)
        conexao.commit()
        return cursor.lastrowid

    except Error as e:
        print(f"[ERRO] Falha ao executar query: {e}")
        conexao.rollback()
        return None

    finally:
        cursor.close()
        conexao.close()


# ─────────────────────────────────────────────────────
# FUNÇÃO: BUSCAR DADOS (SELECT)
# ─────────────────────────────────────────────────────
def buscar_query(query: str, valores: tuple = ()):
    """
    Executa comandos SELECT.
    Retorna uma lista de dicionários com os resultados.
    Ex: [{"id": 1, "nome": "João", ...}, ...]
    """
    conexao = conectar()
    if conexao is None:
        return []

    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(query, valores)
        return cursor.fetchall()

    except Error as e:
        print(f"[ERRO] Falha ao buscar dados: {e}")
        return []

    finally:
        cursor.close()
        conexao.close()
