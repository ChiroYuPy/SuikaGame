MOMENT_OF_INERTIA = {
    "ball": lambda mass, radius: (1/2) * mass * (radius ** 2),                      # Ball 🟢   : (1/2) * mass * radius²
    "box": lambda mass, width, height: (1/12) * mass * (width ** 2 + height ** 2),  # Box 🟩    : (1/12) * mass * (width² + height²)
}