# =====================================================
# SARBACANE V3
# GESTION DES JOUEURS
# =====================================================

class Joueur:

    def __init__(
        self,
        nom,
        club="",
        categorie=""
    ):
        self.nom = nom
        self.club = club
        self.categorie = categorie

    def to_dict(self):
        return {
            "nom": self.nom,
            "club": self.club,
            "categorie": self.categorie
        }

    def __str__(self):
        if self.club:
            return f"{self.nom} ({self.club})"
        return self.nom
hiers (*.*)