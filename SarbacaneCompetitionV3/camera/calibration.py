import cv2
import json
import math

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

    # Premier clic : centre
    if etape == 1:

        centre_x = x
        centre_y = y

        etape = 2

        print()
        print(f"Centre sélectionné : {centre_x}, {centre_y}")
        print("Cliquez maintenant sur le bord extérieur du dernier cercle bleu.")

    # Deuxième clic : rayon de référence
    elif etape == 2:

        rayon_reference = int(
            math.sqrt(
                (x - centre_x) ** 2 +
                (y - centre_y) ** 2
            )
        )

        donnees = {
            "centre_x": centre_x,
            "centre_y": centre_y,
            "rayon_reference": rayon_reference
        }

        with open(
            "data/calibration_cible.json",
            "w",
            encoding="utf-8"
        ) as fichier:

            json.dump(
                donnees,
                fichier,
                indent=4
            )

        print()
        print("Calibration sauvegardée.")
        print(f"Rayon de référence : {rayon_reference} pixels")


cap = cv2.VideoCapture(URL)

if not cap.isOpened():

    print("Impossible d'ouvrir le flux vidéo.")
    quit()

cv2.namedWindow("Calibration V3")

cv2.setMouseCallback(
    "Calibration V3",
    souris
)

print("=== CALIBRATION V3 ===")
print("1) Cliquez sur le centre du 10")
print("2) Cliquez sur le bord extérieur du dernier cercle bleu")
print("R = Réinitialiser")
print("ESC = Quitter")

while True:

    ok, frame = cap.read()

    if not ok:
        print("Image non reçue.")
        break

    # Affichage du centre
    if centre_x is not None:

        cv2.drawMarker(
            frame,
            (centre_x, centre_y),
            (0, 0, 255),
            cv2.MARKER_CROSS,
            30,
            2
        )

    # Affichage du cercle de référence
    if (
        centre_x is not None and
        rayon_reference is not None
    ):

        cv2.circle(
            frame,
            (centre_x, centre_y),
            rayon_reference,
            (255, 0, 0),
            2
        )

    cv2.imshow(
        "Calibration V3",
        frame
    )

    touche = cv2.waitKey(1) & 0xFF

    # ESC
    if touche == 27:
        break

    # R
    if touche == ord("r"):

        centre_x = None
        centre_y = None
        rayon_reference = None
        etape = 1

        print()
        print("=== CALIBRATION REINITIALISÉE ===")
        print("Cliquez sur le centre du 10")

cap.release()
cv2.destroyAllWindows()