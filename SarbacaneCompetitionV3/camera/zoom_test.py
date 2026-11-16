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

        print("Centre enregistré")

    elif etape == 2:

        rayon_reference = int(
            math.sqrt(
                (x - centre_x) ** 2 +
                (y - centre_y) ** 2
            )
        )

        etape = 3

        print(
            f"Rayon enregistré : {rayon_reference}px"
        )

        print(
            "Zoom automatique activé"
        )


cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("Impossible d'ouvrir le flux.")
    quit()

cv2.namedWindow("Zoom Test")

cv2.setMouseCallback(
    "Zoom Test",
    souris
)

while True:

    ok, frame = cap.read()

    if not ok:
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

    if (
        centre_x is not None and
        rayon_reference is not None
    ):

        cv2.circle(
            affichage,
            (centre_x, centre_y),
            rayon_reference,
            (255, 0, 0),
            2
        )

    # ---------------------------------
    # Zoom automatique après calibration
    # ---------------------------------

    if etape == 3:

        h, w = frame.shape[:2]

        demi_largeur = int(rayon_reference * 1.5)
        demi_hauteur = int(rayon_reference * 1.5)

        x1 = max(
            0,
            centre_x - demi_largeur
        )

        y1 = max(
            0,
            centre_y - demi_hauteur
        )

        x2 = min(
            w,
            centre_x + demi_largeur
        )

        y2 = min(
            h,
            centre_y + demi_hauteur
        )

        zone = frame[y1:y2, x1:x2]

        if zone.size > 0:

            affichage = cv2.resize(
                zone,
                (w, h)
            )

    cv2.imshow(
        "Zoom Test",
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

        print("Réinitialisation")

cap.release()
cv2.destroyAllWindows()