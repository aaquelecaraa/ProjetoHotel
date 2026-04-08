class Quarto:
    TIPOS_VALIDOS = ["single", "double", "suite"]
    STATUS_VALIDOS = ["disponivel", "ocupado", "manutencao"]

    def __init__(self, numero: int, tipo: str, preco_diaria: float, status: str = "disponivel", id: int = None):
        self.id = id
        self.numero = numero
        self.tipo = tipo.lower()
        self.preco_diaria = preco_diaria
        self.status = status.lower()

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "tipo": self.tipo,
            "preco_diaria": self.preco_diaria,
            "status": self.status
        }

    def __repr__(self):
        return f"Quarto(numero={self.numero}, tipo={self.tipo}, status={self.status})"