from ....constants import EPSILON
from ....utils import Vec2


class RectCollider:
    """Détecteur de collision rectangulaire."""

    def __init__(self, position: Vec2, size: Vec2) -> None:
        """
        Constructeur.
        :param position: La position du centre du rectangle.
        :param size: La taille du rectangle.
        """
        # Le centre du rectangle
        self.position: Vec2 = position
        self.size: Vec2 = size

    @property
    def x(self) -> float:
        return self.position.x
    
    @x.setter
    def x(self, new_x: float) -> None:
        self.position.x = new_x

    @property
    def y(self) -> float:
        return self.position.y
    
    @y.setter
    def y(self, new_y: float) -> None:
        self.position.y = new_y

    @property
    def width(self) -> float:
        return self.size.x
    
    @width.setter
    def width(self, new_width: float) -> None:
        self.size.x = new_width
    
    @property
    def height(self) -> float:
        return self.size.y
    
    @height.setter
    def height(self, new_height: float) -> None:
        self.size.y = new_height
    
    def is_colliding_rect(self, other: 'RectCollider') -> bool:
        """
        Méthode qui permet de savoir si le rectangle est en collision avec un
        autre.
        :param other: L'autre rectangle avec lequel faire la vérification.
        :return: Vrai si les deux rectangles sont en collision, False sinon.
        """
        return abs(self.x - other.x) < (self.width + other.width) / 2 and \
            abs(self.y - other.y) < (self.height + other.height) / 2
    
    def resolve_collision_x_rewind(self, other: 'RectCollider',
            other_previous_pos: Vec2) -> float:
        """
        Trouver la part du mouvement effectué qui peut être conservée pour que
        la collision soit résolue avec l'axe x.
        :param other: Le rectangle de collision qui doit être déplacé.
        :param other_previous_pos: La position avant le mouvement.
        :return: Part qui doit être faite en marche arrière.
        """
        double_size_x = (self.size.x + other.size.x) / 2.0
        delta_pos = other.position - other_previous_pos

        t_x = 0.0
        if delta_pos.x != 0.0:
            t_x = min(
                (self.x - other_previous_pos.x + double_size_x) / delta_pos.x,
                (self.x - other_previous_pos.x - double_size_x) / delta_pos.x
            )
        
        return t_x
        
    def resolve_collision_y_rewind(self, other: 'RectCollider',
            other_previous_pos: Vec2) -> float:
        """
        Trouver la part du mouvement effectué qui peut être conservée pour que
        la collision soit résolue avec l'axe y.
        :param other: Le rectangle de collision qui doit être déplacé.
        :param other_previous_pos: La position avant le mouvement.
        :return: Part qui doit être faite en marche arrière.
        """
        double_size_y = (self.size.y + other.size.y) / 2.0
        delta_pos = other.position - other_previous_pos

        t_y = 0.0
        if delta_pos.y != 0.0:
            t_y = min(
                (self.y - other_previous_pos.y + double_size_y) / delta_pos.y,
                (self.y - other_previous_pos.y - double_size_y) / delta_pos.y
            )
        
        return t_y