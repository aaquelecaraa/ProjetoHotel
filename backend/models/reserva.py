from datetime import date

class Reserva:
    STATUS_VALIDOS = ["ativa", "cancelada", "concluida"]

    def __init__(
        self,
        cliente_id: int,
        quarto_id: int,
        data_checkin: date,
        data_checkout: date,
        status: str = "ativa",
        id: int = None
    ):
        self.id = id
        self.cliente_id = cliente_id
        self.quarto_id = quarto_id
        self.data_checkin = data_checkin
        self.data_checkout = data_checkout
        self.status = status.lower()

    def calcular_total(self, preco_diaria: float) -> float:
        delta = self.data_checkout - self.data_checkin
        return delta.days * preco_diaria

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "quarto_id": self.quarto_id,
            "data_checkin": str(self.data_checkin),
            "data_checkout": str(self.data_checkout),
            "status": self.status
        }

    def __repr__(self):
        return (f"Reserva(id={self.id}, cliente_id={self.cliente_id}, "
                f"quarto_id={self.quarto_id}, status={self.status})")