import unittest

from utils import Stack

from ...unittest_random import UTRandom


class StackTests(unittest.TestCase):
    """Test de la structure de données Pile."""
    
    def test_push_pop(self) -> None:
        """Test des méthodes "pop" et "push"."""
        test_values: list[int] = [
            UTRandom.rnd.randint(-1000, 1000) for _ in range(100)
        ]
        s = Stack()
        
        for value in test_values:
            s.push(value)
        
        for value in reversed(test_values):
            self.assertEqual(s.pop(), value)
    
    def test_is_empty(self) -> None:
        """Test de l'accesseur "est_vide"."""
        self.assertTrue(Stack().is_empty)

        s = Stack()
        s._internal_list = [i for i in range(UTRandom.rnd.randint(1, 100))]
        self.assertFalse(s.is_empty)
    
    def test_len(self) -> None:
        """Test de la méthode "__len__"."""
        s = Stack()
        
        for _ in range(100):
            size = UTRandom.rnd.randint(0, 100)
            s._internal_list = [i for i in range(size)]
            self.assertEqual(len(s), size)
