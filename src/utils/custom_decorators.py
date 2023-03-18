"""Décorateurs utilitaires."""

from typing import Any, Callable, Generic, TypeVar


T = TypeVar('T')


class ClassGetter(Generic[T]):
    """
    Décorateur pour transformer des méthodes de classes en assesseur.
    """

    def __init__(self, getter_class_method: Callable[[Any], T]) -> None:
        """
        Constructeur (appelé quand ClassGetter est utilisé en tant que
        décorateur).
        :param getter_class_method: La méthode de classe qui est décorée. Elle
            est appelée quand quelqu'un accède à la méthode comme si elle était
            un attribut de classe.
        """
        self._getter_function: Callable[[Any], T] = getter_class_method
    
    def __get__(self, _caller_instance: Any, owner_class: Any) -> T:
        """Appelle la méthode décorée."""
        return self._getter_function(owner_class)