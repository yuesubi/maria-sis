import enum


class Anchor(enum.Enum):
    """Énumération qui représente l'encrage des éléments de l'IHM à l'écran."""

    C = 0  # Centre
    N = 1  # Nord
    E = 2  # Est
    S = 3  # Sud
    W = 4  # Ouest

    NE = 5  # Nord-Est
    SE = 6  # Sud-Est
    SW = 7  # Sud-Ouest
    NW = 8  # Nord-Ouest