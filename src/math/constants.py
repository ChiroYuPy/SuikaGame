MOMENT_OF_INERTIA = {
    "ball": lambda mass, radius: (1/2) * mass * (radius ** 2),                      # Ball 🟢   : (1/2) * mass * radius²
    "box": lambda mass, width, height: (1/12) * mass * (width ** 2 + height ** 2),  # Box 🟩    : (1/12) * mass * (width² + height²)
}

GRAVITY = 9.81

AIR_DENSITY = 1.225

DRAG_COEFFICIENTS = {
    "sphere": 0.47,
    "cube": 1.05,
    "cylinder": 0.82,
    "streamlined_body": 0.04,  # Exemple : Forme de goutte d'eau
}