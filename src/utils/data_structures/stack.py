import typing


T = typing.TypeVar("T")


class Stack(typing.Generic[T]):
    """Classe représentant la structure de données pile."""
    
    def __init__(self) -> None:
        """Constructeur."""
        self._internal_list: list[T] = list()
    
    @property
    def is_empty(self) -> bool:
        """
        Savoir si la pile est vide ou non.
        :return: Vrai si la pile est vide, Faux sinon.
        """
        return len(self._internal_list) == 0
    
    def __len__(self) -> int:
        """
        Récupérer la taille de la pile.
        :return: La taille.
        """
        return len(self._internal_list)

    def push(self, value: T) -> None:
        """
        Empiler une valeur.
        :param value: La valeur à empiler.
        """
        self._internal_list.append(value)
    
    def pop(self) -> T:
        """
        Dépiler la valeur en haut de la pile. [!] Lance IndexError si la pile
        est vide.
        :return: La valeur dépilée.
        """
        if self.is_empty:
            raise IndexError("can't pop a value from an empty stack")
        return self._internal_list.pop()
    
    def peak(self) -> T:
        """
        Consulter la valeur en haut de la pile. [!] Lance IndexError si la pile
        est vide.
        :return: La valeur en haut de la pile.
        """
        if self.is_empty:
            raise IndexError("can't peak on an empty stack")
        return self._internal_list[-1]