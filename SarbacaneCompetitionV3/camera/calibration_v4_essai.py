import cv2
import math

URL = "http://192.168.1.142:8080/video"

centre_x = None
centre_y = None
rayon_reference = None

hg = None
hd = None
bg = None
bd = None

etape = 1


def souris(event, x, y, flags, param):

    global centre_x
    global centre_y
    global rayon_reference

    global hg
    global hd
    global bg
    global bd

    global etape

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    # ---------------------------------
    # Centre cible
    # ---------------------------------

    if etape == 1:

        centre_x = x
        centre_y = y

        etape = 2

        print("Centre du 10 valide")
        print("Clique sur le cercle bleu")

    # ---------------------------------
    # Rayon
    # ---------------------------------

    elif etape == 2:

        rayon_reference = int(
            math.sqrt(
                (x - centre_x) ** 2 +
                (y - centre_y) ** 2
            )
        )

        etape = 3

        print("Rayon valide")
        print("Clique marqueur HG")

    # ---------------------------------
    # Marqueurs
    # ---------------------------------

    elif etape == 3:

        hg = (x, y)

        etape = 4

        print("HG valide")
        print("Clique marqueur HD")

    elif etape == 4:

        hd = (x, y)

        etape = 5

        print("HD valide")
        print("Clique marqueur BG")

    elif etape == 5:

        bg = (x, y)

        etape = 6

        print("BG valide")
        print("Clique marqueur BD")

    elif etape == 6:

        bd = (x, y)

        etape = 7

        print("BD valide")
        print("Calcul termine")


cap = cv2.VideoCapture(URL)

if not cap.isOpened():

    print("Camera inaccessible")
    quit()

cv2.namedWindow("Calibration V4")

cv2.setMouseCallback(
    "Calibration V4",
    souris
)

while True:

    ok, frame = cap.read()

    if not ok:
        break

    affichage = frame.copy()

    # ---------------------------------
    # Croix rouge
    # ---------------------------------

    if centre_x is not None and centre_y is not None:

        cv2.drawMarker(
            affichage,
            (centre_x, centre_y),
            (0, 0, 255),
            cv2.MARKER_CROSS,
            30,
            2
        )

    # ---------------------------------
    # Cercle bleu
    # ---------------------------------

    if (
        centre_x is not None and
        centre_y is not None and
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
    # Zoom
    # ---------------------------------

    if (
        centre_x is not None and
        centre_y is not None and
        rayon_reference is not None
    ):

        h, w = frame.shape[:2]

        demi = int(rayon_reference * 2.1)

        x1 = max(
            0,
            centre_x - demi
        )

        y1 = max(
            0,
            centre_y - demi
        )

        x2 = min(
            w,
            centre_x + demi
        )

        y2 = min(
            h,
            centre_y + demi
        )

        zone = frame[y1:y2, x1:x2]

        if zone.size > 0:

            affichage = cv2.resize(
                zone,
                (w, h)
            )

    # ---------------------------------
    # Affichage marqueurs
    # ---------------------------------

    marqueurs = [
        hg,
        hd,
        bg,
        bd
    ]

    for pt in marqueurs:

        if pt is None:
            continue

        cv2.circle(
            affichage,
            pt,
            8,
            (0, 255, 255),
            -1
        )

    # ---------------------------------
    # Croix verte
    # ---------------------------------

    if (
        hg is not None and
        hd is not None and
        bg is not None and
        bd is not None and
        centre_x is not None and
        centre_y is not None
    ):

        cv2.line(
            affichage,
            hg,
            bd,
            (0, 255, 0),
            2
        )

        cv2.line(
            affichage,
            hd,
            bg,
            (0, 255, 0),
            2
        )

        centre_auto_x = int(
            (
                hg[0] +
                hd[0] +
                bg[0] +
                bd[0]
            ) / 4
        )

        centre_auto_y = int(
            (
                hg[1] +
                hd[1] +
                bg[1] +
                bd[1]
            ) / 4
        )

        cv2.drawMarker(
            affichage,
            (
                centre_auto_x,
                centre_auto_y
            ),
            (0, 255, 0),
            cv2.MARKER_CROSS,
            40,
            3
        )

        ecart = int(
            math.sqrt(
                (centre_auto_x - centre_x) ** 2
                +
                (centre_auto_y - centre_y) ** 2
            )
        )

        cv2.putText(
            affichage,
            f"Ecart : {ecart}px",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

    cv2.imshow(
        "Calibration V4",
        affichage
    )

    touche = cv2.waitKey(1) & 0xFF

    if touche == 27:
        break

    if touche == ord("r"):

        centre_x = None
        centre_y = None
        rayon_reference = None

        hg = None
        hd = None
        bg = None
        bd = None

        etape = 1

        print("Reinitialisation")

cap.release()
cv2.destroyAllWindows()