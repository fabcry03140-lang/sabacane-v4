#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import time
from tkinter import Tk
from tkinter.filedialog import askdirectory

# ==================================================
# CHOIX DU DOSSIER
# ==================================================

root = Tk()
root.withdraw()
root.attributes("-topmost", True)

DOSSIER_IMAGES = askdirectory(title="Choisir le dossier des images")
root.destroy()

if not DOSSIER_IMAGES:
    print("Aucun dossier sélectionné")
    raise SystemExit

# ==================================================
# PARAMETRES DE DETECTION DE VOLEE
# ==================================================

TAILLE_SORTIE = 800
MARGE_EXTERIEURE = 100
FLECHES_PAR_VOLEE = 3

SEUIL_DIFF_PIXEL = 35
MIN_PIXELS_FLECHE = 250
MAX_PIXELS_CORPS = 25000
DELAI_STABILISATION = 0.6

# ==================================================
# ARUCO
# ==================================================

dictionnaire = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parametres = cv2.aruco.DetectorParameters()
detecteur = cv2.aruco.ArucoDetector(dictionnaire, parametres)

# ==================================================
# CAMERA
# ==================================================

source = input("Camera (0, 1 ou adresse IP) : ").strip()
if source.isdigit():
    source = int(source)

cap = cv2.VideoCapture(source)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("Impossible d'ouvrir la caméra")
    raise SystemExit

# ==================================================
# REDRESSEMENT STABILISE AVEC MARGE
# ==================================================

derniere_matrice = None
IDS_ATTENDUS = (0, 1, 2, 3)


def redresser_cible_stable(image):
    global derniere_matrice

    coins, ids, _ = detecteur.detectMarkers(image)
    aruco_direct = False

    if ids is not None and len(ids) >= 4:
        ids_liste = ids.flatten().tolist()

        if all(marqueur_id in ids_liste for marqueur_id in IDS_ATTENDUS):
            pts_src = np.zeros((4, 2), dtype=np.float32)
            for idx_id in IDS_ATTENDUS:
                index = ids_liste.index(idx_id)
                centre = np.mean(coins[index][0], axis=0)
                pts_src[idx_id] = centre

            m = MARGE_EXTERIEURE
            fin = TAILLE_SORTIE - 1 - m

            pts_dst = np.array([
                [m, m],
                [fin, m],
                [fin, fin],
                [m, fin]
            ], dtype=np.float32)

            derniere_matrice = cv2.getPerspectiveTransform(pts_src, pts_dst)
            aruco_direct = True

    if derniere_matrice is not None:
        image_redressee = cv2.warpPerspective(
            image,
            derniere_matrice,
            (TAILLE_SORTIE, TAILLE_SORTIE)
        )
        return image_redressee, aruco_direct, True

    return None, False, False


def preparer_gris(image):
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gris, (7, 7), 0)


# ==================================================
# VARIABLES D'ETAT DE LA VOLEE
# ==================================================

mode_ecoute = False
fleches_capturees = 0
image_reference_gris = None
moment_detection = None

NOM_FENETRE = "Capture Auto Volee (3 Fleches)"
cv2.namedWindow(NOM_FENETRE, cv2.WINDOW_NORMAL)
cv2.resizeWindow(NOM_FENETRE, 800, 800)

# ==================================================
# BOUCLE PRINCIPALE
# ==================================================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_redressee, aruco_direct, matrice_dispo = redresser_cible_stable(frame)

    if not matrice_dispo:
        apercu = cv2.resize(frame, (TAILLE_SORTIE, TAILLE_SORTIE))
        cv2.putText(
            apercu,
            "CADREZ LES 4 MARQUEURS ARUCO (0,1,2,3)...",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 0, 255),
            2
        )
        cv2.imshow(NOM_FENETRE, apercu)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        continue

    if image_redressee is None:
        continue

    apercu = image_redressee.copy()
    gris_actuel = preparer_gris(image_redressee)

    if mode_ecoute and image_reference_gris is not None:
        diff = cv2.absdiff(image_reference_gris, gris_actuel)
        _, masque = cv2.threshold(diff, SEUIL_DIFF_PIXEL, 255, cv2.THRESH_BINARY)
        pixels_modifies = cv2.countNonZero(masque)

        if pixels_modifies > MAX_PIXELS_CORPS:
            moment_detection = None
            statut_texte = f"PASSAGE DETECTE - ATTENTE ({fleches_capturees}/{FLECHES_PAR_VOLEE})"
            couleur_statut = (0, 165, 255)

        elif pixels_modifies > MIN_PIXELS_FLECHE:
            if moment_detection is None:
                moment_detection = time.time()

            temps_ecoule = time.time() - moment_detection
            statut_texte = f"IMPACT ! Stabilisation ({temps_ecoule:.1f}s)..."
            couleur_statut = (0, 255, 255)

            if temps_ecoule >= DELAI_STABILISATION:
                fleches_capturees += 1
                nom = f"volee_f{fleches_capturees}_{int(time.time() * 1000)}.jpg"
                chemin = os.path.join(DOSSIER_IMAGES, nom)
                cv2.imwrite(chemin, image_redressee)

                print(f"\a[OK] Photo {fleches_capturees}/{FLECHES_PAR_VOLEE} : {nom}")

                image_reference_gris = gris_actuel.copy()
                moment_detection = None

                cv2.rectangle(
                    apercu,
                    (0, 0),
                    (TAILLE_SORTIE, TAILLE_SORTIE),
                    (0, 255, 0),
                    20
                )

                if fleches_capturees >= FLECHES_PAR_VOLEE:
                    mode_ecoute = False
                    print("=== VOLEE TERMINEE (3/3) - Retirez vos fleches ===\n")

        else:
            moment_detection = None
            statut_texte = f"PRET A TIRER : Fleche {fleches_capturees + 1}/{FLECHES_PAR_VOLEE} (Q=Quitter)"
            couleur_statut = (0, 255, 0)

    else:
        statut_texte = "EN PAUSE | Retirez les fleches puis appuyez sur [V] ou [P]"
        couleur_statut = (255, 200, 0)

    cv2.rectangle(apercu, (0, 0), (TAILLE_SORTIE, 50), (0, 0, 0), -1)
    cv2.putText(
        apercu,
        statut_texte,
        (15, 33),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        couleur_statut,
        2
    )

    cv2.imshow(NOM_FENETRE, apercu)
    touche = cv2.waitKey(1) & 0xFF

    if touche in (ord("v"), ord("p")):
        mode_ecoute = True
        fleches_capturees = 0
        moment_detection = None
        image_reference_gris = gris_actuel.copy()
        print("\n>>> NOUVELLE VOLEE DEMARREE (0/3) - Vous pouvez tirer ! <<<")

    if touche == ord("q"):
        break

# ==================================================
# FERMETURE
# ==================================================

cap.release()
cv2.destroyAllWindows()
