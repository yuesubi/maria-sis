"""Tests des décorateurs customs."""

import unittest

from utils import ClassGetter

from ..unittest_random import UTRandom


class ClassGetterTests(unittest.TestCase):
    """Test du décorateur d'assesseur pour une classe statique"""
    
    def test_getting_constant_values(self) -> None:
        """
        Teste le décorateur avec des valeurs constantes qui sont retournées.
        """

        # Tests avec des chaînes d'octets
        for _ in range(100):
            test_bytes = UTRandom.rnd.randbytes(8)

            class Foo:
                @ClassGetter
                def b(cls) -> bytes:
                    return test_bytes
            
            self.assertEqual(Foo.b, test_bytes)
        
        # Test d'un assesseur vide
        class Foo:
            @ClassGetter
            def n(cls) -> None:
                pass
        self.assertIsNone(Foo.n)

    def test_access_class_attributes(self) -> None:
        """Test d'accès au attributs statiques de la classe."""

        class Foo:
            _b = None

            @ClassGetter
            def b(cls) -> bytes:
                return test_bytes

        for _ in range(100):
            test_bytes = UTRandom.rnd.randbytes(8)
            Foo._b = test_bytes
            self.assertEqual(Foo.b, test_bytes)
    
    def test_access_instance_attributes(self) -> None:
        """
        Test d'accès au attributs d'une instance la classe (ce qui ne doit pas
        marcher).
        """

        test_bytes = UTRandom.rnd.randbytes(8)
        
        class Foo:
            def __init__(self) -> None:
                self._b = test_bytes
            
            @ClassGetter
            def b(self) -> bytes:
                return self._b
        
        with self.assertRaises(AttributeError):
            self.assertEqual(Foo().b == test_bytes)