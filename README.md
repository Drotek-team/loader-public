# Python Template Demo

The generated project from Drotek Python template.

## Utilisation du precommit

### Installation des outils Python

- [pyenv & poetry](https://drotek.atlassian.net/wiki/spaces/DRONE/pages/36143105/Python+Tools+Tutorial)

### Installation du projet

1. Ouvrez _Visual Studio Code_
1. Utilisez Python 3.8.2

   ```shell
   pyenv shell 3.8.2
   ```

1. Initialisez l'environnement _Poetry_

   ```shell
   poetry shell
   ```

1. Installez les dépendances du projet

   ```shell
   poetry install
   ```

1. Initialisez _git_

   ```shell
   git init
   ```

1. Installez `pre-commit`

   ```shell
   pre-commit install
   ```

1. Faisez votre premier commit

   ```shell
   git add .
   SKIP=no-commit-to-branch git commit -m "Initial commit"
   ```

Vous êtes maintenant prêt à programmer ! 🙂
