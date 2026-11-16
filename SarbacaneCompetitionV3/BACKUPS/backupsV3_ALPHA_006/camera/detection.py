import cv2
import json
import math

URL = "http://192.168.1.142:8080/video"

# ----------------------------------
# Chargement calibration
# ----------------------------------

with open(
    "data/calibration_cible.json",
    "r",
    encoding="utf-8"
) as fichier:

    calibration = json.load(fichier)

centre_x = calibration["centre_x"]
centre_y = calibration["centre_y"]
rayon_reference = calibration["rayon_reference"]

# ----------------------------------
# Variables
# ----------------------------------

distance_pixels = None
pourcentage = None

point_x = None
point_y = None

# ----------------------------------
# Souris
# ----------------------------------

def souris(event, x, y, flags, param):

    global distance_pixels
    global pourcentage
    global point_x
    global point_y

    if event == cv2.EVENT_LBUTTONDOWN:

        point_x = x
        point_y = y

        distance_pixels = int(
            math.sqrt(
                (x - centre_x) ** 2 +
                (y - centre_y) ** 2
            )
        )

        pourcentage = (
            distance_pixels /
            rayon_reference
        ) * 100

        print()
        print(f"Distance : {distance_pixels} pixels")
        print(f"Rayon : {pourcentage:.1f}%")

# ----------------------------------
# Caméra
# ----------------------------------

cap = cv2.VideoCapture(URL)

if not cap.isOpened():

    print("Impossible d'ouvrir le flux.")
    quit()

cv2.namedWindow("Detection V3")

cv2.setMouseCallback(
    "Detection V3",
    souris
)

print("=== DETECTION V3 ===")
print("Cliquez dans la cible")
print("R = Réinitialiser")
print("ESC = Quitter")

# ----------------------------------
# Boucle principale
# ----------------------------------

while True:

    ok, frame = cap.read()

    if not ok:
        print("Image non reçue.")
        break

    # ----------------------------------
    # Anneaux théoriques
    # ----------------------------------

    for score in range(1, 11):

        rayon = int(
            rayon_reference * score / 10
        )

        cv2.circle(
            frame,
            (centre_x, centre_y),
            rayon,
            (120, 120, 120),
            1
        )

    # ----------------------------------
    # Cercle de référence
    # ----------------------------------

    cv2.circle(
        frame,
        (centre_x, centre_y),
        rayon_reference,
        (255, 0, 0),
        2
    )

    # ----------------------------------
    # Croix centrale
    # ----------------------------------

    cv2.drawMarker(
        frame,
        (centre_x, centre_y),
        (0, 0, 255),
        cv2.MARKER_CROSS,
        30,
        2
    )

    # ----------------------------------
    # Point mesuré
    # ----------------------------------

    if point_x is not None:

        cv2.circle(
            frame,
            (point_x, point_y),
            6,
            (0, 255, 0),
            -1
        )

        cv2.line(
            frame,
            (centre_x, centre_y),
            (point_x, point_y),
            (0, 255, 0),
            2
        )

    # ----------------------------------
    # Informations
    # ----------------------------------

    if distance_pixels is not None:

        cv2.putText(
            frame,
            f"Distance : {distance_pixels}px",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Rayon : {pourcentage:.1f}%",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

    cv2.imshow(
        "Detection V3",
        frame
    )

    touche = cv2.waitKey(1) & 0xFF

    if touche == 27:
        break

    if touche == ord("r"):

        point_x = None
        point_y = None

        distance_pixels = None
        pourcentage = None

        print()
        print("=== REINITIALISATION ===")

cap.release()
cv2.destroyAllWindows()