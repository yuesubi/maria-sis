# Contribuer


## Préparation
Installer [git](https://git-scm.com/).

Créez une clef ssh et ajoutez la à votre compte (voir tutoriel
[ici](https://docs.github.com/fr/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
)

## Cloner le rep
**Attention**: il faut que le compte ai la clef ssh utilisée sur la machine (
voir [préparation](#préparation))
```bash
git clone git@github.com:yuesubi/maria-bros.git
```

## Récupérez le code le plus récent de GitHub
Récupérez le code le plus récent. `main` doit être remplacé par le nom de la
branche sur laquelle faire les changements.
```bash
git pull origin main
```

## Commit des changements localement
**Attention**: ne faites un commit sur la branche `main` que si le code
fonctionne et ne casse pas d'autres parties du code. Vous pouvez créer une
autre branche si le code de fonctionne pas (void [ici](#les-branches)).
Récupérez le code le plus récent (instructions
[ici](#récupérez-le-code-le-plus-récent-de-github)) puis utilisez les commandes
suivantes:
(Remplacez `.` par un nom de dossier ou de fichier si vous ne voulez pas tout
commit d'un coup.)
```bash
git add .
git commit -m "Message décrivant le commit"
```

## Les branches

### Lister les banches existantes
```bash
git branch
```

### Créer une branche
```bash
git branch nom-de-nouvelle-branche
```

### Visiter une branche
```bash
git checkout nom-de-la-branche
```