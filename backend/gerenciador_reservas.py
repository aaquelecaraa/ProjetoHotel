class GerenciadorDeReservas:
    def __init__(self):
        # Aqui vamos conectar com o banco de dados futuramente
        pass

    def verificar_disponibilidade(self, quarto_id: int, data_checkin, data_checkout) -> bool:
        """
        Verifica se o quarto está disponível no período informado.
        Retorna True se disponível, False se não.
        """
        pass

    def criar_reserva(self, cliente_id: int, quarto_id: int, data_checkin, data_checkout):
        """
        Cria uma nova reserva se o quarto estiver disponível.
        """
        pass

    def modificar_reserva(self, reserva_id: int, novos_dados: dict):
        """
        Modifica uma reserva existente com os novos dados fornecidos.
        """
        pass

    def cancelar_reserva(self, reserva_id: int):
        """
        Cancela uma reserva existente pelo ID.
        """
        pass

    def listar_reservas(self) -> list:
        """
        Retorna uma lista com todas as reservas.
        """
        pass

    def listar_clientes(self) -> list:
        """
        Retorna uma lista com todos os clientes.
        """
        pass