import enum


class Fit(enum.Enum):
    """
    Énumération qui représente comment les éléments doivent adapter leur taille
    au parent.
    """

    NONE = 0    # Pas de changement de taille
    WIDTH = 1   # Adaptation de la largeur
    HEIGHT = 2  # Adaptation de la hauteur
    BOTH = 3    # Adaptation de la largeur et de la hauteur