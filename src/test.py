"""Lancer ce fichier pour exécuter tous les tests."""

import unittest

# Importation de tout les tests
from tests import *


# Point d'entrée des tests
if __name__ == "__main__":
    UTRandom.set_seed()
    print(f"Unit test random seed : {UTRandom.get_seed()}")

    # Exécution de tous les tests
    unittest.main()