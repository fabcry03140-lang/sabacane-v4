import cv2
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

    if etape == 1:

        centre_x = x
        centre_y = y

        etape = 2

        print()
        print(f"Centre sélectionné : {centre_x}, {centre_y}")
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
        print(f"Rayon : {rayon_reference} px")
        print("Zoom automatique activé.")


cap = cv2.VideoCapture(URL)

if not cap.isOpened():

    print("Impossible d'ouvrir le flux.")
    quit()

cv2.namedWindow("Calibration V2 Essai")

cv2.setMouseCallback(
    "Calibration V2 Essai",
    souris
)

print("=== CALIBRATION V2 ESSAI ===")
print("1 : centre du 10")
print("2 : cercle bleu extérieur")
print("R : réinitialiser")
print("ESC : quitter")

while True:

    ok, frame = cap.read()

    if not ok:
        print("Image non reçue.")
        break

    affichage = frame.copy()

    if centre_x is not None:

        cv2.drawMarker(
            affichage,
            (centre_x, centre_y),
            (0, 0, 255),
            cv2.MARKER_CROSS,
            30,
            2
        )

    if centre_x is not None and rayon_reference is not None:

        cv2.circle(
            affichage,
            (centre_x, centre_y),
            rayon_reference,
            (255, 0, 0),
            2
        )

    if etape == 3:

        h, w = frame.shape[:2]

        demi_largeur = int(rayon_reference * 2.1)
        demi_hauteur = int(rayon_reference * 2.1)

        x1 = max(0, centre_x - demi_largeur)
        y1 = max(0, centre_y - demi_hauteur)

        x2 = min(w, centre_x + demi_largeur)
        y2 = min(h, centre_y + demi_hauteur)

        zone = frame[y1:y2, x1:x2]

        if zone.size > 0:

            gris = cv2.cvtColor(
                zone,
                cv2.COLOR_BGR2GRAY
            )

            _, seuil = cv2.threshold(
                gris,
                100,
                255,
                cv2.THRESH_BINARY_INV
            )

            contours, _ = cv2.findContours(
                seuil,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            nb_objets = 0
            centres = []

            for contour in contours:

                aire = cv2.contourArea(contour)

                if aire < 80:
                    continue

                if aire > 30000:
                    continue

                x, y, wc, hc = cv2.boundingRect(contour)

                ratio = wc / hc

                if 0.7 <= ratio <= 1.3:

                    cx = x + wc // 2
                    cy = y + hc // 2

                    centres.append((cx, cy))

                    cv2.rectangle(
                        zone,
                        (x, y),
                        (x + wc, y + hc),
                        (0, 255, 0),
                        2
                    )

                    cv2.circle(
                        zone,
                        (cx, cy),
                        5,
                        (0, 0, 255),
                        -1
                    )

                    nb_objets += 1

            affichage = cv2.resize(
                zone,
                (w, h)
            )

            cv2.putText(
                affichage,
                f"Objets : {nb_objets}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            cv2.putText(
                affichage,
                f"Centres : {len(centres)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

    cv2.imshow(
        "Calibration V2 Essai",
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

        print()
        print("=== REINITIALISATION ===")

cap.release()
cv2.destroyAllWindows()
