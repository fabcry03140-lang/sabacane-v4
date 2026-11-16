import math

from config.settings import (
    RAYON_10_MM,
    LARGEUR_ZONE_MM
)

def score_depuis_distance(distance_mm):

    if distance_mm <= RAYON_10_MM:
        return 10

    zones = math.ceil(
        (distance_mm - RAYON_10_MM)
        / LARGEUR_ZONE_MM
    )

    return max(10 - zones, 0)