# Projet Arachnida

Ce projet contient deux scripts Python, `scorpion.py` et `spider.py`, qui permettent respectivement d'afficher les métadonnées EXIF d'une image et de télécharger des images à partir d'une URL de manière récursive. Les deux scripts peuvent être exécutés dans un conteneur Docker.

## Fonctionnalités

### `scorpion.py`
- Affiche les métadonnées EXIF d'une image.
- Utilise une interface graphique pour afficher les informations EXIF et un aperçu de l'image.
- Vérifie que le fichier est une image valide avant de traiter les données.

### `spider.py`
- Télécharge des images à partir d'une URL donnée.
- Fonctionne de manière récursive pour explorer les liens et télécharger toutes les images accessibles.
- Enregistre les images dans un répertoire local.

## Prérequis

- Docker
- Docker Compose

## Installation et Exécution

1. Clonez ce dépôt sur votre machine locale :
   ```sh
   git clone <URL_DU_DEPOT>
   cd arachnida
   ```

2. Construisez et démarrez le conteneur Docker :
   ```sh
   docker compose up --build
   ```

3. Accédez au conteneur Docker :
   ```sh
   docker exec -it python bash
   ```

4. Exécutez les scripts selon vos besoins :

   - Pour afficher les métadonnées EXIF d'une image avec `scorpion.py` :
     ```sh
     python scorpion.py <CHEMIN_VERS_L_IMAGE>
     ```

   - Pour télécharger des images à partir d'une URL avec `spider.py` :
     ```sh
     python spider.py <URL>
     ```

## Structure du Projet

```
arachnida/
├── docker-compose.yaml
├── dockerfile
├── README.md
└── file/
    ├── scorpion.py
    └── spider.py
```

- **`docker-compose.yaml`** : Fichier de configuration Docker Compose.
- **`dockerfile`** : Fichier Docker pour construire l'image Python.
- **`scorpion.py`** : Script pour afficher les métadonnées EXIF d'une image.
- **`spider.py`** : Script pour télécharger des images de manière récursive.

## Notes

- Assurez-vous que les images à analyser avec `scorpion.py` sont accessibles depuis le conteneur Docker.
- Les images téléchargées par `spider.py` seront enregistrées dans le répertoire local du conteneur.

