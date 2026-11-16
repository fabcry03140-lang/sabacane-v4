import cv2
import math

URL = "http://192.168.1.142:8080/video"

centre_x = None
centre_y = None
rayon_reference = None

cadres = []

cadre_temp = None

etape = 1

# ---------------------------------------
# SOURIS
# ---------------------------------------

def souris(event, x, y, flags, param):

    global centre_x
    global centre_y
    global rayon_reference

    global cadre_temp
    global etape

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    # Centre du 10

    if etape == 1:

        centre_x = x
        centre_y = y

        etape = 2

        print("Centre valide")
        print("Clique cercle bleu")

        return

    # Rayon

    if etape == 2:

        rayon_reference = int(
            math.sqrt(
                (x - centre_x) ** 2 +
                (y - centre_y) ** 2
            )
        )

        etape = 3

        print("Rayon valide")
        print("Touche V pour commencer")

        return

    # Validation marqueurs

    if etape >= 4:

        taille = 40

        cadre_temp = (
            x - taille // 2,
            y - taille // 2,
            taille,
            taille
        )


# ---------------------------------------
# CAMERA
# ---------------------------------------

cap = cv2.VideoCapture(URL)

if not cap.isOpened():

    print("Camera inaccessible")
    quit()

cv2.namedWindow("Calibration V4.1")

cv2.setMouseCallback(
    "Calibration V4.1",
    souris
)

# ---------------------------------------
# BOUCLE
# ---------------------------------------

while True:

    ok, frame = cap.read()

    if not ok:
        break

    affichage = frame.copy()

    # Croix rouge

    if centre_x is not None:

        cv2.drawMarker(
            affichage,
            (centre_x, centre_y),
            (0, 0, 255),
            cv2.MARKER_CROSS,
            30,
            2
        )

    # Cercle bleu

    if (
        centre_x is not None
        and rayon_reference is not None
    ):

        cv2.circle(
            affichage,
            (centre_x, centre_y),
            rayon_reference,
            (255, 0, 0),
            2
        )

    # Zoom

    if (
        centre_x is not None
        and rayon_reference is not None
    ):

        h, w = frame.shape[:2]

        demi = int(
            rayon_reference * 2.1
        )

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

        zone = frame[
            y1:y2,
            x1:x2
        ]

        if zone.size > 0:

            affichage = cv2.resize(
                zone,
                (w, h)
            )

    # Cadres validés

    for x, y, wc, hc in cadres:

        cv2.rectangle(
            affichage,
            (x, y),
            (x + wc, y + hc),
            (0, 255, 0),
            2
        )

    # Cadre temporaire

    if cadre_temp is not None:

        x, y, wc, hc = cadre_temp

        cv2.rectangle(
            affichage,
            (x, y),
            (x + wc, y + hc),
            (0, 255, 255),
            2
        )

    # Centres des cadres

    centres = []

    for x, y, wc, hc in cadres:

        centres.append(
            (
                x + wc // 2,
                y + hc // 2
            )
        )

    # Croisement

    if len(centres) == 4:

        for cx, cy in centres:

            cv2.circle(
                affichage,
                (cx, cy),
                5,
                (0, 255, 255),
                -1
            )

        centre_auto_x = int(
            sum(
                p[0]
                for p in centres
            ) / 4
        )

        centre_auto_y = int(
            sum(
                p[1]
                for p in centres
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
            2
        )

    cv2.putText(
        affichage,
        f"Cadres : {len(cadres)}/4",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "Calibration V4.1",
        affichage
    )

    touche = cv2.waitKey(1) & 0xFF

    # ESC

    if touche == 27:
        break

    # V = démarrer sélection

    if touche == ord("v"):

        if etape == 3:

            etape = 4

            print()
            print("Selection des marqueurs")
            print("Clique HG")

    # ENTREE = valider cadre

    if touche == 13:

        if (
            cadre_temp is not None
            and len(cadres) < 4
        ):

            cadres.append(
                cadre_temp
            )

            cadre_temp = None

            print(
                f"Cadre valide {len(cadres)}/4"
            )

    # R = reset

    if touche == ord("r"):

        centre_x = None
        centre_y = None

        rayon_reference = None

        cadres.clear()

        cadre_temp = None

        etape = 1

        print("Reset")

cap.release()

cv2.destroyAllWindows()