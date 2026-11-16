from core.score import score_depuis_distance

print("=== TEST SCORE V3 ===")

tests = [
    0,
    2,
    4.5,
    10,
    18,
    27,
    50,
    95
]

for distance in tests:

    score = score_depuis_distance(distance)

    print(
        f"Distance : {distance:5} mm"
        f" -> Score : {score}"
    )

print("\nTest terminé avec succès.")