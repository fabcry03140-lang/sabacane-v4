# =====================================================
# SARBACANE V3
# GESTION CAMERA
# =====================================================

import cv2


def ouvrir_camera(index=0):

    cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        raise RuntimeError(
            "Impossible d'ouvrir la caméra"
        )

    return cap


def fermer_camera(cap):

    if cap:
        cap.release()