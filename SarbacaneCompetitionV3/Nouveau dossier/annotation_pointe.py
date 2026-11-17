#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==========================================================
# ANNOTATION POINTE DE FLECHETTE
# Version simple et modifiable
# ==========================================================

import os
import cv2

# ----------------------------------------------------------
# PARAMETRES
# ----------------------------------------------------------

from tkinter import Tk
from tkinter.filedialog import askdirectory

Tk().withdraw()

DOSSIER_IMAGES = askdirectory(
    title="Choisir le dossier des images"
)

# ----------------------------------------------------------
# VARIABLES GLOBALES
# ----------------------------------------------------------

point = None
vue_dirty = True

# ----------------------------------------------------------
# SOURIS
# ----------------------------------------------------------

def souris(event, x, y, flags, param):
    global point, vue_dirty

    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        vue_dirty = True

# ----------------------------------------------------------
# CHARGEMENT DES IMAGES
# ----------------------------------------------------------

images = sorted([
    f for f in os.listdir(DOSSIER_IMAGES)
    if f.lower().endswith(
        (".jpg", ".jpeg", ".png")
    )
])

if len(images) == 0:
    print("Aucune image trouvée")
    raise SystemExit

# ----------------------------------------------------------
# FENETRE
# ----------------------------------------------------------

cv2.namedWindow("Annotation")

cv2.setMouseCallback(
    "Annotation",
    souris
)

index = 0

# ----------------------------------------------------------
# BOUCLE PRINCIPALE
# ----------------------------------------------------------

while True:

    if index < 0:
        index = 0

    if index >= len(images):
        print("Fin des annotations")
        break

    nom_image = images[index]

    chemin_image = os.path.join(
        DOSSIER_IMAGES,
        nom_image
    )

    chemin_txt = os.path.splitext(
        chemin_image
    )[0] + ".txt"

    image = cv2.imread(
        chemin_image
    )

    if image is None:
        print(f"Image introuvable ou illisible : {chemin_image}")
        index += 1
        continue

    point = None
    vue_dirty = True

    # ------------------------------------------------------
    # CHARGER ANNOTATION EXISTANTE
    # ------------------------------------------------------

    if os.path.exists(chemin_txt):

        try:

            with open(
                chemin_txt,
                "r",
                encoding="utf-8"
            ) as fichier:

                contenu = fichier.read().strip()

                x, y = map(
                    int,
                    contenu.split()
                )

                point = (x, y)

        except Exception:
            pass

    # ------------------------------------------------------
    # AFFICHAGE
    # ------------------------------------------------------

    while True:

        # Ne reconstruire et recopier l'image qu'après une modification.
        if vue_dirty:
            vue = image.copy()

            if point is not None:
                cv2.circle(
                    vue,
                    point,
                    8,
                    (0, 0, 255),
                    -1
                )

            cv2.putText(
                vue,
                f"{index+1}/{len(images)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

            cv2.putText(
                vue,
                nom_image,
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            cv2.imshow(
                "Annotation",
                vue
            )
            vue_dirty = False

        touche = cv2.waitKey(20) & 0xFF

        # --------------------------------------------------
        # S = sauvegarder
        # --------------------------------------------------

        if touche == ord("s"):

            if point is not None:

                with open(
                    chemin_txt,
                    "w",
                    encoding="utf-8"
                ) as fichier:

                    fichier.write(
                        f"{point[0]} {point[1]}"
                    )

                print(
                    f"Sauvegardé : {nom_image}"
                )

            index += 1

            break

        # --------------------------------------------------
        # N = suivant
        # --------------------------------------------------

        if touche == ord("n"):

            index += 1

            break

        # --------------------------------------------------
        # P = précédent
        # --------------------------------------------------

        if touche == ord("p"):

            index -= 1

            break

        # --------------------------------------------------
        # E = effacer annotation
        # --------------------------------------------------

        if touche == ord("e"):

            point = None
            vue_dirty = True

            print(
                "Annotation effacée"
            )

        # --------------------------------------------------
        # Q = quitter
        # --------------------------------------------------

        if touche == ord("q"):

            cv2.destroyAllWindows()

            raise SystemExit

cv2.destroyAllWindows()
