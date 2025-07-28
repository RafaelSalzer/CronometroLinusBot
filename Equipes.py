class Equipe:
    def __init__(self, nome, cor):
        self.nome = nome
        self.cor = cor
        self.voltas = []
    def exibeTitulo(self):
        return f"Equipe {self.cor}: {self.nome}"

    