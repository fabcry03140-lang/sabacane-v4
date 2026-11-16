import cv2
import math
import numpy as np

URL = "http://192.168.1.142:8080/video"

centre_x = None
centre_y = None
rayon_reference = None

etape = 1


def souris(event, x, y, flags, param):

    global centre_x
    global centre_y
    global rayon_reference
    global etape

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if etape == 1:

        centre_x = x
        centre_y = y

        etape = 2

        print()
        print(f"Centre : {centre_x}, {centre_y}")
        print("Cliquez sur le bord extérieur du cercle bleu.")

    elif etape == 2:

        rayon_reference = int(
            math.sqrt(
                (x - centre_x) ** 2 +
                (y - centre_y) ** 2
            )
        )

        etape = 3

        print()
        print(f"Rayon : {rayon_reference}px")
        print("Recherche des marqueurs...")


cap = cv2.VideoCapture(URL)

if not cap.isOpened():

    print("Impossible d'ouvrir le flux.")
    quit()

cv2.namedWindow("Detection Coins V3")

cv2.setMouseCallback(
    "Detection Coins V3",
    souris
)

while True:

    ok, frame = cap.read()

    if not ok:
        break

    affichage = frame.copy()

    if etape == 3:

        h, w = frame.shape[:2]

        if centre_x is None or centre_y is None or rayon_reference is None:
            continue

        demi = int(rayon_reference * 2.1)

        x1 = max(0, centre_x - demi)
        y1 = max(0, centre_y - demi)

        x2 = min(w, centre_x + demi)
        y2 = min(h, centre_y + demi)

        zone = frame[y1:y2, x1:x2]

        if zone.size > 0:

            gris = cv2.cvtColor(
                zone,
                cv2.COLOR_BGR2GRAY
            )

            seuil = cv2.adaptiveThreshold(
                gris,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,
                11,
                2
            )

            hauteur, largeur = seuil.shape

            taille_zone = int(
                min(largeur, hauteur) * 0.20
            )

            coins = [

                ("HG", 0, 0),

                (
                    "HD",
                    largeur - taille_zone,
                    0
                ),

                (
                    "BG",
                    0,
                    hauteur - taille_zone
                ),

                (
                    "BD",
                    largeur - taille_zone,
                    hauteur - taille_zone
                )
            ]

            nb_detectes = 0

            for nom, zx, zy in coins:

                sous_zone = seuil[
                    zy:zy + taille_zone,
                    zx:zx + taille_zone
                ]

                ys, xs = np.where(
                    sous_zone > 0
                )

                if len(xs) == 0:
                    continue

                cx = int(np.mean(xs))
                cy = int(np.mean(ys))

                cx_global = zx + cx
                cy_global = zy + cy

                cv2.rectangle(
                    zone,
                    (zx, zy),
                    (
                        zx + taille_zone,
                        zy + taille_zone
                    ),
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    zone,
                    (cx_global, cy_global),
                    7,
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    zone,
                    nom,
                    (
                        cx_global + 10,
                        cy_global
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

                nb_detectes += 1

            affichage = cv2.resize(
                zone,
                (w, h)
            )

            cv2.putText(
                affichage,
                f"Reperes : {nb_detectes}/4",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

    cv2.imshow(
        "Detection Coins V3",
        affichage
    )

    touche = cv2.waitKey(1) & 0xFF

    if touche == 27:
        break

    if touche == ord("r"):

        centre_x = None
        centre_y = None
        rayon_reference = None
        etape = 1

cap.release()
cv2.destroyAllWindows()