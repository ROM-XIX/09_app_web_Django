

# LITReview - Installation et utilisation en local

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://www.python.org/)
![Django](https://img.shields.io/badge/django-5.2.3-darkgreen?logo=django)

Application web Django pour publier des billets de demande de critique, écrire des critiques, et gérer des abonnements entre utilisateurs.

## Prérequis

- Python `3.11` (ou version compatible avec Django 5.2)
- `pip`
- Un terminal (Linux/macOS/Windows)

## 1. Récupérer le projet

Si le projet est déjà sur votre machine, placez-vous dans son dossier racine (`P_09`).

## 2. Créer et activer un environnement virtuel

Depuis la racine du projet :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows (PowerShell) :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 3. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Initialiser le projet Django

Le fichier `manage.py` est dans le dossier `litrevu/`.

```bash
cd litrevu
python manage.py migrate
```

Optionnel (accès admin Django) :

```bash
python manage.py createsuperuser
```

## 5. Lancer le serveur local

Toujours depuis le dossier `litrevu/` :

```bash
python manage.py runserver
```

Le serveur démarre par défaut sur :

- `http://127.0.0.1:8000/`

## 6. Ouvrir l'application dans le navigateur

- Page d'accueil : `http://127.0.0.1:8000/`
- Connexion : `http://127.0.0.1:8000/login/`
- Inscription : `http://127.0.0.1:8000/signup/`
- Admin (si superuser) : `http://127.0.0.1:8000/admin/`

## Utilisation rapide

1. Créer un compte depuis `/signup/`.
2. Se connecter.
3. Accéder au flux (`/flux/`) pour consulter et interagir avec les billets/critique.
4. Utiliser l'onglet `Abonnements` pour suivre d'autres utilisateurs.

## Arborescence utile

- `litrevu/manage.py` : commandes Django
- `litrevu/litrevu/settings.py` : configuration projet
- `litrevu/authentification/` : inscription/connexion
- `litrevu/gestionlivre/` : billets, critiques, abonnements

## Commandes utiles

Depuis `litrevu/` :

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
```

## Arrêter le serveur

Dans le terminal où `runserver` tourne :

- `Ctrl + C`

## Remarques

- La base de données utilisée en local est SQLite (`db.sqlite3`).
- Les fichiers médias uploadés sont servis en développement via `/media/`.
