import pygame


class Input:
    """Classe statique qui gère les entrées du jeu."""

    ############################################################################
    # VARIABLES DE LA CLASSE
    
    # L'état des touches du clavier
    _keys_pressed: set[int] = set()
    _keys_released: set[int] = set()
    _keys_down: set[int] = set()

    # L'état des boutons de la souris
    _buttons_pressed: set[int] = set()
    _buttons_released: set[int] = set()
    _buttons_down: set[int] = set()

    # Position de la souris
    _mouse_position: pygame.Vector2 = pygame.Vector2(0, 0)
    _delta_mouse_position: pygame.Vector2 = pygame.Vector2(0, 0)

    # Savoir si l'application doit être quittée
    _is_quitting: bool = False

    ############################################################################
    # ASSESSEURS
    
    @property
    @classmethod
    def is_quitting(cls) -> bool:
        """
        Assesseur pour savoir si l'application doit être quittée.
        :return: Vrai si l'application doit être quittée. 
        """
        return cls._is_quitting

    @property
    @classmethod
    def mouse_position(cls) -> pygame.Vector2:
        """
        Assesseur pour récupérer la position de la souris.
        :return: La position de la souris. 
        """
        return cls._mouse_position

    @property
    @classmethod
    def delta_mouse_position(cls) -> pygame.Vector2:
        """
        Assesseur pour récupérer la difference de position de la souris avec le
        dernier appel de la méthode actualiser.
        :return: la difference de position de la souris avec le dernier appel de
            la méthode actualiser. 
        """
        return cls._delta_mouse_position
    
    @classmethod
    def is_key_pressed(cls, key: int) -> bool:
        """
        Savoir si une touche vient d'être pressée.
        :param key: L'identifiant de la touche.
        :return: Vrai si la touche vient d'être pressée.
        """
        return key in cls._keys_pressed
 
    @classmethod
    def is_key_released(cls, key: int) -> bool:
        """
        Savoir si une touche vient d'être relâchée.
        :param key: L'identifiant de la touche.
        :return: Vrai si la touche vient d'être relâchée.
        """
        return key in cls._keys_released
    
    @classmethod
    def is_key_down(cls, key: int) -> bool:
        """
        Savoir si une touche est enfoncée.
        :param key: L'identifiant de la touche.
        :return: Vrai si la touche est enfoncée.
        """
        return key in cls._keys_down
    
    @classmethod
    def is_button_pressed(cls, button: int) -> bool:
        """
        Savoir si un bouton vient d'être pressé.
        :param button: L'identifiant du bouton.
        :return: Vrai si le bouton vient d'être pressé.
        """
        return button in cls._buttons_pressed

    @classmethod
    def is_button_released(cls, button: int) -> bool:
        """
        Savoir si un bouton vient d'être relâché.
        :param button: L'identifiant du bouton.
        :return: Vrai si le bouton vient d'être relâché.
        """
        return button in cls._buttons_released
    
    @classmethod
    def is_button_down(cls, button: int) -> bool:
        """
        Savoir si un bouton est enfoncé.
        :param button: L'identifiant du bouton.
        :return: Vrai si le bouton est enfoncé.
        """
        return button in cls._buttons_down

    ############################################################################
    # MÉTHODES DE RÉCUPÉRATION DES ÉVÈNEMENTS

    @classmethod
    def update(cls) -> None:
        """
        Actualiser les entrées en prenant compte des nouveaux évènements
        arrivées depuis le dernier appel de cette méthode.
        (!) Cette méthode doit être appelée une seule fois par itération de la
        boucle principale.
        """

        # Retirer les évènements précédents
        cls._keys_pressed.clear()
        cls._keys_released.clear()

        cls._buttons_pressed.clear()
        cls._buttons_released.clear()

        cls._is_quitting = False
        
        # Calcul de la position de la souris
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        cls._delta_mouse_position = mouse_position - cls._mouse_position
        cls._mouse_position = mouse_position

        # Récupérer les évènements
        for event in pygame.event.get():
            # Détection de touches
            if event.type == pygame.KEYDOWN:
                cls._keys_pressed.add(event.key)
                cls._keys_down.add(event.key)
            elif event.type == pygame.KEYUP:
                cls._keys_released.add(event.key)
                if event.key in cls._keys_down:
                    cls._keys_down.remove(event.key)

            # Détection de boutons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cls._buttons_pressed.add(event.button)
                cls._buttons_down.add(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                cls._buttons_released.add(event.button)
                if event.button in cls._buttons_down:
                    cls._buttons_down.remove(event.button)

            # Demande de fermeture de la fenêtre
            elif event.type == pygame.QUIT:
                cls._is_quitting = True
