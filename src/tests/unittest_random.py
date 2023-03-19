import random

from typing import Any


def _generate_random_seed() -> Any:
    return "".join(hex(random.randint(0, 16 - 1))[2] for _ in range(32))


class UTRandom:
    """Aléatoire pour les tests unitaires."""
    
    _seed: Any = _generate_random_seed()
    rnd: random.Random = random.Random(_seed)

    @classmethod
    def set_seed(cls, new_seed: Any = None) -> None:
        cls._seed = new_seed if new_seed != None else _generate_random_seed()
        cls.rnd = random.Random(cls._seed)
    
    @classmethod
    def get_seed(cls) -> Any:
        return cls._seed