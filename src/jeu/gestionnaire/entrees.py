import pygame


class Entrees:
    """Classe statique qui gère les entrées du jeu."""

    ############################################################################
    # VARIABLES DE LA CLASSE
    
    # L'état des touches du clavier
    _touches_pressees: set[int] = set()
    _touches_relachees: set[int] = set()
    _touches_enfoncees: set[int] = set()

    # L'état des boutons de la souris
    _boutons_presses: set[int] = set()
    _boutons_relaches: set[int] = set()
    _boutons_enfonces: set[int] = set()

    # Position de la souris
    _position_souris: pygame.Vector2 = pygame.Vector2(0, 0)
    _delta_position_souris: pygame.Vector2 = pygame.Vector2(0, 0)

    # Savoir si l'application doit être quittée
    _est_quitte: bool = False

    ############################################################################
    # ASSESSEURS
    
    @property
    @classmethod
    def est_quitte(cls) -> bool:
        """
        Assesseur pour savoir si l'application doit être quittée.
        :return: Vrai si l'application doit être quittée. 
        """
        return cls._est_quitte

    @property
    @classmethod
    def position_souris(cls) -> pygame.Vector2:
        """
        Assesseur pour récupérer la position de la souris.
        :return: La position de la souris. 
        """
        return cls._position_souris

    @property
    @classmethod
    def delta_position_souris(cls) -> pygame.Vector2:
        """
        Assesseur pour récupérer la difference de position de la souris avec le
        dernier appel de la méthode actualiser.
        :return: la difference de position de la souris avec le dernier appel de
            la méthode actualiser. 
        """
        return cls._delta_position_souris
    
    @classmethod
    def est_touche_pressee(cls, touche: int) -> bool:
        """
        Savoir si une touche vient d'être pressée.
        :param touche: L'identifiant de la touche.
        :return: Vrai si la touche vient d'être pressée.
        """
        return touche in _touches_pressees
 
    @classmethod
    def est_touche_relachee(cls, touche: int) -> bool:
        """
        Savoir si une touche vient d'être relâchée.
        :param touche: L'identifiant de la touche.
        :return: Vrai si la touche vient d'être relâchée.
        """
        return touche in cls._touches_relachees
    
    @classmethod
    def est_touche_enfoncee(cls, touche: int) -> bool:
        """
        Savoir si une touche est enfoncée.
        :param touche: L'identifiant de la touche.
        :return: Vrai si la touche est enfoncée.
        """
        return touche in cls._touches_enfoncees
    
    @classmethod
    def est_bouton_presse(cls, bouton: int) -> bool:
        """
        Savoir si un bouton vient d'être pressé.
        :param bouton: L'identifiant du bouton.
        :return: Vrai si le bouton vient d'être pressé.
        """
        return bouton in cls._boutons_presses

    @classmethod
    def est_bouton_relache(cls, bouton: int) -> bool:
        """
        Savoir si un bouton vient d'être relâché.
        :param bouton: L'identifiant du bouton.
        :return: Vrai si le bouton vient d'être relâché.
        """
        return bouton in cls._boutons_relaches
    
    @classmethod
    def est_bouton_enfonce(cls, bouton: int) -> bool:
        """
        Savoir si un bouton est enfoncé.
        :param bouton: L'identifiant du bouton.
        :return: Vrai si le bouton est enfoncé.
        """
        return bouton in cls._boutons_enfoncees

    ############################################################################
    # MÉTHODES DE RÉCUPÉRATION DES ÉVÈNEMENTS

    @classmethod
    def actualiser(cls) -> None:
        """
        Actualiser les entrées en prenant compte des nouveaux évènements
        arrivées depuis le dernier appel de cette méthode.
        (!) Cette méthode doit être appelée une seule fois par itération de la
        boucle principale.
        """

        # Retirer les évènements précédents
        cls._touches_pressees.clear()
        cls._touches_relachees.clear()

        cls._boutons_presses.clear()
        cls._boutons_relaches.clear()

        cls._est_quitte = False
        
        # Calcul de la position de la souris
        position_souris = pygame.Vector2(pygame.mouse.get_pos())
        cls._delta_position_souris = position_souris - cls._position_souris
        cls._position_souris = position_souris

        # Récupérer les évènements
        for evenement in pygame.event.get():
            # Détection de touches
            if evenement.type == pygame.KEYDOWN:
                cls._touches_pressees.add(evenement.key)
                cls._touches_enfoncees.add(evenement.key)
            elif evenement.type == pygame.KEYUP:
                cls._touches_relachees.add(evenement.key)
                if evenement.key in cls._touches_enfoncees:
                    cls._touches_enfoncees.remove(evenement.key)

            # Détection de boutons
            elif evenement.type == pygame.MOUSEBUTTONDOWN:
                cls._boutons_presses.add(evenement.button)
                cls._boutons_enfonces.add(evenement.button)
            elif evenement.type == pygame.MOUSEBUTTONUP:
                cls._boutons_relaches.add(evenement.button)
                if evenement.button in cls._boutons_enfonces:
                    cls._boutons_enfonces.remove(evenement.button)

            # Demande de fermeture de la fenêtre
            elif evenement.type == pygame.QUIT:
                cls._est_quitte = True
