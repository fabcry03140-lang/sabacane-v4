# =====================================================
# SARBACANE V3
# GESTION DU MATCH
# =====================================================

from datetime import datetime

from core.score import score_depuis_distance


class Match:

    def __init__(self, voix=None):

        self.voix = voix

        self.volee = 1
        self.flechette = 1

        self.score_total = 0
        self.score_volee = 0

        self.dernier_score = "-"

        self.tirs = []

        self.termine = False

    def annoncer(self, texte):

        if self.voix:
            self.voix.parler(texte)

    def ajouter_tir(self, distance_mm):

        score = score_depuis_distance(distance_mm)

        self.dernier_score = str(score)

        tir = {
            "Volée": self.volee,
            "Fléchette": self.flechette,
            "Score": score,
            "Distance_Centre_mm": round(distance_mm, 1),
            "Heure": datetime.now().strftime("%H:%M:%S")
        }

        self.tirs.append(tir)

        self.score_total += score
        self.score_volee += score

        if score == 10:
            self.annoncer("Plein centre ! Dix !")

        elif score == 0:
            self.annoncer("Hors cible. Zéro.")

        else:
            self.annoncer(str(score))

        fin_volee = False

        if self.flechette < 3:

            self.flechette += 1

        else:

            fin_volee = True

            self.annoncer(
                f"Fin de la volée {self.volee}"
            )

            self.annoncer(
                f"Score volée : {self.score_volee}"
            )

            self.volee += 1
            self.flechette = 1
            self.score_volee = 0

            if self.volee > 10:

                self.termine = True

        return {
            "score": score,
            "fin_volee": fin_volee,
            "match_termine": self.termine
        }

    def get_resume(self):

        return {
            "volee": self.volee,
            "flechette": self.flechette,
            "score_total": self.score_total,
            "dernier_score": self.dernier_score,
            "termine": self.termine
        }

    def get_tirs(self):

        return self.tirs

    def reset(self):

        self.volee = 1
        self.flechette = 1

        self.score_total = 0
        self.score_volee = 0

        self.dernier_score = "-"

        self.tirs = []

        self.termine = False