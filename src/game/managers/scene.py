import enum
from typing import Any, Protocol

from ...utils import ClassGetter, Stack


class SceneId(enum.Enum):
    LEVEL: int = 0
    MAIN_MENU: int = 1
    HOST_CLIENT_MENU: int  = 2
    CONNECT_METHOD_MENU: int  = 3


class CreateSceneCallBack(Protocol):
    """
    Type de la fonction de création de scène. (Juste pour indiquer le type)
    """

    def __call__(self, new_scene_id: SceneId, *scene_args: Any,
            **scene_kwds: Any) -> 'Scene':
        """
        :param new_scene_id: L'identifiant de la scène à créer.
        :param *scene_args: Les argument à donner au constructeur de la scène.
        :param *scene_kwargs: Les argument clés à donner au constructeur de la
            scène.
        """


class Scene:
    class SceneStackEmpty(BaseException): ...

    _scene_stack: Stack['Scene'] = Stack()
    _create_scene_callback: CreateSceneCallBack = lambda _, *arg, **kw: Scene()
    
    @classmethod
    def set_create_scene_callback(cls, create_callback: CreateSceneCallBack
            ) -> None:
        """
        Changer la fonction utilisée pour créer une scène.
        :param create_callback: La fonction utilisée pour créer une nouvelle
            scène.
        """
        cls._create_scene_callback = create_callback
    
    @classmethod
    def pop_scene(cls) -> None:
        """
        Dépiler une scène de la pile de scènes. Celle d'en dessous devient la
        scène actuelle.
        """
        if cls._scene_stack.is_empty:
            raise Scene.SceneStackEmpty("can't pop a scene from an empty stack")
        # Dépiler la scène et appeler la méthode de fin dessus
        cls._scene_stack.pop().quit()

    @classmethod
    def push_scene(cls, new_scene_id: SceneId, *scene_args: Any,
            **scene_kwargs: Any) -> None:
        """
        Empiler une scène. Elle devient la scène actuelle.
        :param new_scene_id: L'identifiant de la scène à créer.
        :param *scene_args: Les argument à donner au constructeur de la scène.
        :param *scene_kwargs: Les argument clés à donner au constructeur de la
            scène.
        """
        cls._scene_stack.push(
            cls._create_scene_callback(
                new_scene_id,
                *scene_args, **scene_kwargs
            )
        )
    
    @classmethod
    def switch_scene(cls, new_scene_id: SceneId, *scene_args: Any,
            **scene_kwargs: Any) -> None:
        """
        Passer à une nouvelle scène.
        :param new_scene_id: L'identifiant de la scène à créer.
        :param *scene_args: Les argument à donner au constructeur de la scène.
        :param *scene_kwargs: Les argument clés à donner au constructeur de la
            scène.
        """
        cls.pop_scene()
        cls.push_scene(new_scene_id, *scene_args, **scene_kwargs)
    
    @ClassGetter
    def current_scene(cls) -> 'Scene':
        """Assesseur de la scène actuelle."""
        if cls._scene_stack.is_empty:
            raise Scene.SceneStackEmpty("their is no current scene")
        return cls._scene_stack.peak()

    ############################################################################
    # MÉTHODES POUR LES HÉRITIERS

    def update(self) -> None:
        """
        Méthode appelée à chaque frame. La gestion des entrées doit se faire
        ici. (Pour cela, il faut l'implémenter dans une sous classe)
        """

    def fixed_update(self) -> None:
        """
        Méthode appelée à intervale régulier et un nombre de fois fixe par
        seconde. Les mouvements et la gestion de collision doit se faire ici.
        (Pour cela, il faut l'implémenter dans une sous classe)
        """
    
    def render(self) -> None:
        """
        Méthode appelée pour faire le rendu de la scène. (Doit être implémentée
        dans une sous classe)
        """
    
    def quit(self) -> None:
        """
        Méthode appelée quand la scène est quittée. (Peut être implémentée dans
        une sous classe)
        """