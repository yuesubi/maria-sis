# Maria Sis
Le Mario Bros féministe. **(Ne le prenez pas sérieusement svp)**

## Navigation
* For the **english version** see -> [README.md (en)](/README.md)
* Pour **contribuer** voir ->
    [CONTRIBUTING.md (fr)](/res/docs/fr/CONTRIBUTING.md)


## Lancement

### Dépendances
Pour exécuter le jeu il faut avoir `python` (**une version assez récente**),
`raylib` (`pip install raylib`) et `netifaces` (`pip install netifaces2`).

### Cloner le repo
Téléchargez le [zip](https://github.com/yuesubi/maria-sis/archive/refs/heads/main.zip)
ou clonez le repo avec:
```bash
git clone https://github.com/yuesubi/maria-sis.git
```

### Exécution
```bash
cd maria-sis
python maria-sis.py
```


## Arborescence
```txt
-assets/                            Les ressources pour le projet
-maps/                              Les cartes des niveaux de maria sis
-src/                               Le code source
    -game/                          Le code de maria sis
        -assets/                    Les constantes des chemins vers les ressources
            -characters/            Pour les personnage
                -maria.py           Pour maria
            -tile_sets/             Pour le décorations
                -over_world.py      Pour le monde normal
        -level/                     La scène de niveau du jeu
            -block/                 Les blocks
                -block.py           La classe abstraite d'un block
                -decorative.py      Un block décoratif
            -collider/              Les détecteur/solveurs de collision
                -rect_collider.py   Pour un rectangle
            -entity/                Les entités
                -entity.py          La classe abstraite d'une entité
                -player.py          Le joueur
            -level_map/             ...
            -camera.py              La camera
            -level.py               La scène de niveau
        -managers/                  Les gestionnaires
            -scene.py               ...
            -time_manager.py        De temps
        -menus/                     ...
        -game.py                    L'application principale du jeu
    -tests/                         ...
    -utils/                         Du code utilitaire qui n'est pas spécifique au projet
        -data_structures/           ...
        -math/                      Outils mathématiques
            -vec2.py                Un vecteur du plan (2D)
        -custom_decorators.py       ...
    -constants.py                   Les constantes du jeu
    -tests.py                       ...
```


## Schémas

### Modules
![Schéma des modules](/res/schemas/modules.svg)

### Classes
![Schéma des classes](/res/schemas/classes.svg)


## A faire

- [ ] Créer des ennemis :
    * Les ennemis sont des `Entity` (ie: ils hérite de cette classe)
        * La classe d'un ennemi doit avoir :
            - Une méthode `def update(self) -> None: ...`. Les entrées doivent
                être gérées dans cette méthode. Pour consulter les entrées de
                l'utilisateur il faut utiliser `pyray`. (voir
                `/src/game/level/entity/player.py:43` pour un exemple)
            - Une méthode `def fixed_update(self) -> None: ...`. Tout les
                mouvements doivent êtres faits dedans. Chaque quantité de
                mouvement doit être multipliée par `Time.fixed_delta_time`.
                (voir `/src/game/level/entity/player.py:36` pour un exemple)
            - Une méthode `def draw(self, camera: Camera) -> None: ...` pour le
                rendu à l'écran. Il faut utiliser la camera passée en paramètre
                pour le rendu. (voir `/src/game/level/entity/player.py:52` pour
                un exemple et `/src/game/level/camera.py` pour les méthodes de
                rendu disponibles)
        * La classe d'un ennemi peut utiliser `self.position` qui est hérité de
            `Entity` pas besoin de le définir soi-même. 
    * Pour tester une entité, il faut ajouter une instance de l'ennemi dans la
        liste `self.entities` dans `LevelScene.__init__()`


## Progression

### Orgoutte8Pitoulechat
* date durée tâche

### Yuesubi
* 2023/03/11 2h00 Créations de diagrammes UML pour les classes et les modules.
* 2023/03/12 0h30 Création du README.md avec les instructions de lancement,
    ajout de la LICENCE et de CONTRIBUTING.md avec les commandes de base de git.
* 2023/03/12 0h15 Création de l'arborescence de base du projet.
* 2023/03/15 0h30 Ajout d'un gestionnaire de temps et d'entrées.
* 2023/03/18 0h30 Ajout de décorateurs utilitaires.
* 2023/03/19 0h45 Ajout de plus de tests.
* 2023/03/19 0h15 création de la boucle principale.
* 2023/03/19 0h30 Ajout de la structure de données pile et de tests pour
    celle-ci.
* 2023/03/19 1h00 Ajout de méthodes à Time et création d'un gestionnaire de
    scène.
* 2023/03/19 0h15 Intégration du gestionnaire de scène et d'une scène de niveau
    dans la boucle principale.
* 2023/03/22 1h10 Création de la classe abstraite Entity, création d'un exemple
    de joueur et intégration dans le niveau.
* 2023/03/22 0h30 Ajout d'un block décoratif d'exemple et création de la classe
    abstraite Block.
* 2023/03/23 1h15 Création de la LevelMap et de Chunk pour stocker les blocks et
    les entités du niveau.
* 2023/03/23 0h45 Implémentation de la méthode pour charger une carte depuis une
    image.
* 2023/03/23 0h10 Ajout d'un point d'apparition sur la carte.
* 2023/03/23 0h30 Ajout de la détection de collision.
* 2023/03/23 0h30 Ajout d'images dans le jeu pour Maria et DecorativeBlock.
* 2023/03/23 0h10 Petits changements.
* 2023/03/29 2h00 Ajout des collisions.
* 2023/04/02 3h00 Correction des bugs des collisions.
* 2023/04/12 1h00 Création d'une classe de vecteur 2D.
* 2023/04/16 0h30 Ajout du menu principal et des widgets.
* 2023/04/26 1h00 Passage de toutes le utilisation de pygame à pyray.
* 2023/04/27 0h30 Correction des erreurs de typage.
* 2023/05/06 1h00 Ajout de la partie réseau pour le multijoueur.
* 2023/05/11 1h00 Finition du menu de scan.
* 2023/05/13 1h00 Ajout d'une méthode on_collision pour les entités & correction
    de bugs de collision.
* 2023/05/14 1h00 Separation de la Scène de niveau et du niveau, pour faciliter
    la création de niveaux multijoueurs.