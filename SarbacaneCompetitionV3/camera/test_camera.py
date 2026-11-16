from camera import ouvrir_camera
from camera import fermer_camera

print("=== TEST CAMERA V3 ===")

try:

    camera = ouvrir_camera()

    print("Caméra détectée avec succès.")

    fermer_camera(camera)

    print("Test terminé.")

except Exception as erreur:

    print("Erreur :", erreur)