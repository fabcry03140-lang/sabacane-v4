#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lance la capture des images puis leur annotation dans le même dossier."""

import os
import subprocess
import sys
from tkinter import Tk
from tkinter.filedialog import askdirectory


def main():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    dossier_images = askdirectory(title="Choisir le dossier des images")
    root.destroy()

    if not dossier_images:
        print("Aucun dossier sélectionné")
        return 1

    dossier_script = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()
    env["SARBACANE_IMAGES_DIR"] = dossier_images

    capture = os.path.join(dossier_script, "capture_datasetaros.py")
    annotation = os.path.join(dossier_script, "annotation_pointe.py")

    print("Étape 1/2 : capture. Appuyez sur Q pour terminer la capture.")
    resultat = subprocess.run([sys.executable, capture], env=env)
    if resultat.returncode != 0:
        print("La capture a échoué ; l'annotation n'a pas été lancée.")
        return resultat.returncode

    print("Étape 2/2 : annotation des images capturées.")
    resultat = subprocess.run([sys.executable, annotation], env=env)
    return resultat.returncode


if __name__ == "__main__":
    raise SystemExit(main())
