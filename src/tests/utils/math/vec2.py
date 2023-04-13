"""Test de Vec2."""

import unittest

from utils import Vec2
from ...unittest_random import UTRandom


class Vec2Tests(unittest.TestCase):
    """Suite de tests unitaires pour le Vec2."""

    def test___init__(self) -> None:
        """Test du constructeur __init__."""
        for _ in range(100):
            x = UTRandom.rnd.random()
            y = UTRandom.rnd.random()
            v = Vec2(x, y)
            self.assertAlmostEqual(v.x, x)
            self.assertAlmostEqual(v.y, y)

    def test_from_xy(self) -> None:
        """Test du constructeur from_xy."""
        for _ in range(100):
            x = UTRandom.rnd.random()
            y = UTRandom.rnd.random()
            v = Vec2.from_xy((x, y))
            self.assertAlmostEqual(v.x, x)
            self.assertAlmostEqual(v.y, y)
    
    def test_from_yx(self) -> None:
        """Test du constructeur from_yx."""
        for _ in range(100):
            x = UTRandom.rnd.random()
            y = UTRandom.rnd.random()
            v = Vec2.from_yx((y, x))
            self.assertAlmostEqual(v.x, x)
            self.assertAlmostEqual(v.y, y)

    def test_null(self) -> None:
        """Test du constructeur null."""
        v = Vec2.null
        self.assertAlmostEqual(v.x, 0.0)
        self.assertAlmostEqual(v.y, 0.0)
    
    def test_is_null(self) -> None:
        """Test de la propriété is_null."""
        self.assertTrue(Vec2.null.is_null)
        for _ in range(100):
            x = UTRandom.rnd.random()
            self.assertFalse(Vec2(x, 1.0).is_null)
    
    def test___eq____ne__(self) -> None:
        """Test des opérations == et !=."""
        for _ in range(100):
            x = UTRandom.rnd.random()
            y = UTRandom.rnd.random()
            self.assertTrue(Vec2(x, y) == Vec2(x, y))
            self.assertFalse(Vec2(x, y) != Vec2(x, y))
            self.assertFalse(Vec2(x, y) == Vec2(x - 2.0, y - 2.0))
            self.assertTrue(Vec2(x, y) != Vec2(x - 2.0, y - 2.0))
    
    def test_copy(self) -> None:
        """Test de la propriété copy."""
        for _ in range(100):
            x = UTRandom.rnd.random()
            y = UTRandom.rnd.random()
            v = Vec2(x, y)
            c = v.copy
            v.x -= 2.0
            v.y += 2.0
            self.assertTrue(v != c)
            v = c.copy
            self.assertTrue(v == c)