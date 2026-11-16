import cv2
import time
import os

os.environ["OPENCV_FFMPEG_LOGLEVEL"] = "0"

URL = "http://192.168.1.142:8080/video"

cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("Impossible d'ouvrir le flux vidéo.")
    quit()

print("Flux vidéo connecté.")

ancien_temps = time.time()

while True:

    ok, frame = cap.read()

    if not ok:
        print("Image non reçue.")
        break

    nouveau_temps = time.time()

    fps = 1 / (nouveau_temps - ancien_temps)

    ancien_temps = nouveau_temps

    cv2.putText(
        frame,
        f"FPS : {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Sarbacane V3 - Camera",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()