class Cliente:
    def __init__(self, nome: str, telefone: str, email: str, id: int = None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email
        }

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, email={self.email})"