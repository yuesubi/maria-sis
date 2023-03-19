import unittest

from utils import Stack

from ...unittest_random import UTRandom


class StackTests(unittest.TestCase):
    """Test de la structure de données Pile."""

    def test_peak(self) -> None:
        """Test de la méthode "peak"."""
        s = Stack()

        with self.assertRaises(IndexError):
            s.peak()
        
        for _ in range(100):
            number = UTRandom.rnd.randint(-1000, 1000)
            s._internal_list.append(number)
            self.assertEqual(s.peak(), number)

    
    def test_push(self) -> None:
        """Test des méthodes "push"."""
        s = Stack()
        
        for _ in range(100):
            value = UTRandom.rnd.randint(-1000, 1000)
            s.push(value)
            self.assertEqual(s._internal_list[-1], value)

    def test_pop(self) -> None:
        """Test des méthodes "pop"."""
        test_values = [
            UTRandom.rnd.randint(-1000, 1000) for _ in range(100)
        ]
        s = Stack()

        with self.assertRaises(IndexError):
            s.pop()
        
        s._internal_list = test_values.copy()
        for value in reversed(test_values):
            self.assertEqual(s.pop(), value)
        
    def test_is_empty(self) -> None:
        """Test de l'accesseur "est_vide"."""
        self.assertTrue(Stack().is_empty)

        s = Stack()
        s._internal_list = [i for i in range(UTRandom.rnd.randint(1, 50))]
        self.assertFalse(s.is_empty)
    
    def test_len(self) -> None:
        """Test de la méthode "__len__"."""
        s = Stack()
        
        for _ in range(100):
            size = UTRandom.rnd.randint(0, 50)
            s._internal_list = [i for i in range(size)]
            self.assertEqual(len(s), size)