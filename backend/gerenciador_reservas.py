from datetime import datetime
from typing import List, Optional

from .database import buscar_query, executar_query
from .models.cliente import Cliente
from .models.quarto import Quarto
from .models.reserva import Reserva
from . import csv_utils


class GerenciadorDeReservas:
    def __init__(self):
        # Conexão é feita pelo database.py a cada operação
        pass

    # ─────────────────────────────────────────────
    # CLIENTES
    # ─────────────────────────────────────────────
    def criar_cliente(self, nome: str, telefone: str, email: str) -> Optional[Cliente]:
        """Cadastra um novo cliente no banco."""
        query = """
            INSERT INTO clientes (nome, telefone, email)
            VALUES (%s, %s, %s)
        """
        novo_id = executar_query(query, (nome, telefone, email))
        if novo_id is None:
            return None
        return Cliente(id=novo_id, nome=nome, telefone=telefone, email=email)

    def listar_clientes(self) -> list:
        """Retorna uma lista com todos os clientes."""
        dados = buscar_query("SELECT * FROM clientes")
        clientes = []
        for d in dados:
            clientes.append(
                Cliente(
                    id=d["id"],
                    nome=d["nome"],
                    telefone=d["telefone"],
                    email=d["email"],
                )
            )
        return clientes

    def buscar_cliente_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca um cliente específico pelo ID."""
        dados = buscar_query(
            "SELECT * FROM clientes WHERE id = %s",
            (cliente_id,)
        )
        if not dados:
            return None
        d = dados[0]
        return Cliente(
            id=d["id"],
            nome=d["nome"],
            telefone=d["telefone"],
            email=d["email"],
        )

    # ─────────────────────────────────────────────
    # QUARTOS
    # ─────────────────────────────────────────────
    def criar_quarto(
        self,
        numero: int,
        tipo: str,
        preco_diaria: float,
        status: str = "disponivel"
    ) -> Optional[Quarto]:
        """Cadastra um novo quarto no banco."""
        query = """
            INSERT INTO quartos (numero, tipo, preco_diaria, status)
            VALUES (%s, %s, %s, %s)
        """
        novo_id = executar_query(query, (numero, tipo, preco_diaria, status))
        if novo_id is None:
            return None
        return Quarto(
            id=novo_id,
            numero=numero,
            tipo=tipo,
            preco_diaria=preco_diaria,
            status=status
        )

    def listar_quartos(self) -> list:
        """Retorna uma lista com todos os quartos."""
        dados = buscar_query("SELECT * FROM quartos")
        quartos = []
        for d in dados:
            quartos.append(
                Quarto(
                    id=d["id"],
                    numero=d["numero"],
                    tipo=d["tipo"],
                    preco_diaria=float(d["preco_diaria"]),
                    status=d["status"],
                )
            )
        return quartos

    def buscar_quarto_por_id(self, quarto_id: int) -> Optional[Quarto]:
        """Busca um quarto específico pelo ID."""
        dados = buscar_query(
            "SELECT * FROM quartos WHERE id = %s",
            (quarto_id,)
        )
        if not dados:
            return None
        d = dados[0]
        return Quarto(
            id=d["id"],
            numero=d["numero"],
            tipo=d["tipo"],
            preco_diaria=float(d["preco_diaria"]),
            status=d["status"],
        )

    # ─────────────────────────────────────────────
    # DISPONIBILIDADE
    # ─────────────────────────────────────────────
    def verificar_disponibilidade(
        self,
        quarto_id: int,
        data_checkin,
        data_checkout
    ) -> bool:
        """
        Verifica se o quarto está disponível no período informado.
        Retorna True se disponível, False se não.
        """
        if not isinstance(data_checkin, str):
            data_checkin = data_checkin.strftime("%Y-%m-%d")
        if not isinstance(data_checkout, str):
            data_checkout = data_checkout.strftime("%Y-%m-%d")

        query = """
            SELECT * FROM reservas
            WHERE quarto_id = %s
              AND status = 'ativa'
              AND (
                    (data_checkin  <= %s AND data_checkout > %s) OR
                    (data_checkin  <  %s AND data_checkout >= %s) OR
                    (data_checkin  >= %s AND data_checkout <= %s)
                  )
        """
        conflitos = buscar_query(
            query,
            (
                quarto_id,
                data_checkin,  data_checkin,
                data_checkout, data_checkout,
                data_checkin,  data_checkout
            )
        )
        return len(conflitos) == 0   # True = disponível

    # ─────────────────────────────────────────────
    # RESERVAS
    # ─────────────────────────────────────────────
    def criar_reserva(
        self,
        cliente_id: int,
        quarto_id: int,
        data_checkin,
        data_checkout
    ) -> Optional[Reserva]:
        """
        Cria uma nova reserva se o quarto estiver disponível.
        """
        # Valida se cliente e quarto existem
        cliente = self.buscar_cliente_por_id(cliente_id)
        quarto  = self.buscar_quarto_por_id(quarto_id)

        if cliente is None or quarto is None:
            print("[ERRO] Cliente ou quarto inexistente.")
            return None
        
        if quarto.status != "disponivel":
            print(f"[ERRO] Quarto com status '{quarto.status}' não pode ser reservado.")
            return None

        # Verifica disponibilidade antes de criar
        if not self.verificar_disponibilidade(quarto_id, data_checkin, data_checkout):
            print("[ERRO] Quarto não disponível no período informado.")
            return None

        # Garante formato de string para o banco
        if not isinstance(data_checkin, str):
            data_checkin = data_checkin.strftime("%Y-%m-%d")
        if not isinstance(data_checkout, str):
            data_checkout = data_checkout.strftime("%Y-%m-%d")

        query = """
            INSERT INTO reservas (cliente_id, quarto_id, data_checkin, data_checkout, status)
            VALUES (%s, %s, %s, %s, 'ativa')
        """
        novo_id = executar_query(query, (cliente_id, quarto_id, data_checkin, data_checkout))
        if novo_id is None:
            return None

        dt_checkin  = datetime.strptime(data_checkin,  "%Y-%m-%d").date()
        dt_checkout = datetime.strptime(data_checkout, "%Y-%m-%d").date()

        executar_query(
            "UPDATE quartos SET status = 'ocupado' WHERE id = %s",
            (quarto_id,)
        )

        return Reserva(
            id=novo_id,
            cliente_id=cliente_id,
            quarto_id=quarto_id,
            data_checkin=dt_checkin,
            data_checkout=dt_checkout,
            status="ativa",
        )

    def modificar_reserva(self, reserva_id: int, novos_dados: dict) -> bool:
        """
        Modifica uma reserva existente com os novos dados fornecidos.
        novos_dados pode conter: cliente_id, quarto_id,
                                 data_checkin, data_checkout, status.
        """
        reserva = self.buscar_reserva_por_id(reserva_id)
        if reserva is None:
            print("[ERRO] Reserva não encontrada.")
            return False

        campos  = []
        valores = []

        if "cliente_id" in novos_dados:
            campos.append("cliente_id = %s")
            valores.append(novos_dados["cliente_id"])

        if "quarto_id" in novos_dados:
            campos.append("quarto_id = %s")
            valores.append(novos_dados["quarto_id"])

        if "data_checkin" in novos_dados:
            data = novos_dados["data_checkin"]
            if not isinstance(data, str):
                data = data.strftime("%Y-%m-%d")
            campos.append("data_checkin = %s")
            valores.append(data)

        if "data_checkout" in novos_dados:
            data = novos_dados["data_checkout"]
            if not isinstance(data, str):
                data = data.strftime("%Y-%m-%d")
            campos.append("data_checkout = %s")
            valores.append(data)

        if "status" in novos_dados:
            campos.append("status = %s")
            valores.append(novos_dados["status"])

        if not campos:
            print("[AVISO] Nenhum campo para atualizar.")
            return False

        valores.append(reserva_id)
        query = f"UPDATE reservas SET {', '.join(campos)} WHERE id = %s"
        return executar_query(query, tuple(valores)) is not None

    def cancelar_reserva(self, reserva_id: int) -> bool:
        """
        Cancela uma reserva existente pelo ID.
        """
        reserva = self.buscar_reserva_por_id(reserva_id)
        if reserva is None:
            print("[ERRO] Reserva não encontrada.")
            return False

        query = "UPDATE reservas SET status = 'cancelada' WHERE id = %s"
        resultado = executar_query(query, (reserva_id,))
        if resultado is not None:
            executar_query(
                "UPDATE quartos SET status = 'disponivel' WHERE id = %s",
                (reserva.quarto_id,)
        )
        return resultado is not None
    

    def listar_reservas(self) -> list:
        """
        Retorna uma lista com todas as reservas.
        """
        dados = buscar_query("SELECT * FROM reservas")
        reservas = []
        for d in dados:
            reservas.append(
                Reserva(
                    id=d["id"],
                    cliente_id=d["cliente_id"],
                    quarto_id=d["quarto_id"],
                    data_checkin=d["data_checkin"],
                    data_checkout=d["data_checkout"],
                    status=d["status"],
                )
            )
        return reservas

    def buscar_reserva_por_id(self, reserva_id: int) -> Optional[Reserva]:
        """Busca uma reserva específica pelo ID."""
        dados = buscar_query(
            "SELECT * FROM reservas WHERE id = %s",
            (reserva_id,)
        )
        if not dados:
            return None
        d = dados[0]
        return Reserva(
            id=d["id"],
            cliente_id=d["cliente_id"],
            quarto_id=d["quarto_id"],
            data_checkin=d["data_checkin"],
            data_checkout=d["data_checkout"],
            status=d["status"],
        )

    # ─────────────────────────────────────────────
    # EXPORTAÇÃO PARA CSV
    # ─────────────────────────────────────────────
    def exportar_clientes_para_csv(self):
        """Exporta todos os clientes para clientes.csv"""
        csv_utils.salvar_clientes_csv(self.listar_clientes())

    def exportar_quartos_para_csv(self):
        """Exporta todos os quartos para quartos.csv"""
        csv_utils.salvar_quartos_csv(self.listar_quartos())

    def exportar_reservas_para_csv(self):
        """Exporta todas as reservas para reservas.csv"""
        csv_utils.salvar_reservas_csv(self.listar_reservas())
