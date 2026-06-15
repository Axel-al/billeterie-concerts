# Billetterie de concerts

Application web Django de billetterie réalisée dans le cadre d'un projet de
validation logicielle. Le dépôt fournit l'application, les tests automatisés,
la traçabilité des exigences, la couverture, l'analyse statique, une CI GitHub
Actions et une configuration SonarQube Cloud.

## Fonctionnalités

- catalogue public des concerts ouverts, futurs et disponibles ;
- fiche détaillée avec catégories, prix et stocks ;
- inscription et authentification par adresse e-mail ;
- panier mono-concert avec quantité totale comprise entre 1 et 6 ;
- paiement simulé accepté ou refusé ;
- décrément transactionnel du stock après paiement accepté uniquement ;
- historique et détail des commandes payées, isolés par utilisateur ;
- administration des concerts, catégories, ventes, annulations et clôtures ;
- interface et messages de validation en français.

Le cahier des charges officiel se trouve dans
[`docs/brief/projet-validation-logiciel-e4a-2026.md`](docs/brief/projet-validation-logiciel-e4a-2026.md).
Le guide de soutenance se trouve dans
[`docs/validation/demo_soutenance.md`](docs/validation/demo_soutenance.md).

## Stack technique

- Python 3.12 ;
- Django 5.2 ;
- SQLite en développement ;
- templates Django et Bootstrap 5.3.3 via CDN ;
- pytest, pytest-django et pytest-playwright ;
- coverage.py et pytest-cov ;
- Ruff ;
- GitHub Actions ;
- SonarQube Cloud.

## Installation

Cloner le dépôt et créer un environnement virtuel :

```bash
git clone https://github.com/Axel-al/billeterie-concerts.git
cd billeterie-concerts
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Sous Windows PowerShell, activer l'environnement avec :

```powershell
.venv\Scripts\Activate.ps1
```

`requirements.txt` suffit pour lancer l'application. `requirements-dev.txt`
ajoute les outils de test et de qualité. La CI utilise le verrou
`requirements-ci.txt` avec Python 3.12.

## Configuration de l'environnement

Le développement local fonctionne sans fichier `.env`. Pour remplacer les
valeurs par défaut, créer un fichier `.env` non versionné :

```dotenv
DJANGO_SECRET_KEY=change-me-for-local-development
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
```

Variables disponibles :

| Variable | Rôle | Valeur locale par défaut |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Clé secrète Django | Clé de développement non destinée à la production |
| `DJANGO_DEBUG` | Active ou désactive le mode debug | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hôtes séparés par des virgules | `localhost,127.0.0.1,[::1],testserver` |

Ne jamais utiliser la clé locale par défaut en production.

## Base de données et migrations

Créer ou mettre à jour la base SQLite locale :

```bash
python manage.py migrate
```

Vérifier qu'aucune migration ne manque :

```bash
python manage.py makemigrations --check --dry-run
```

Le fichier `db.sqlite3` est local et ignoré par Git.

## Données de démonstration

Créer ou actualiser le jeu de données :

```bash
python manage.py seed_demo_data
```

La commande est idempotente. Elle crée un concert ouvert, un concert annulé,
un concert passé et leurs catégories de places.

## Compte administrateur

Créer un superutilisateur :

```bash
python manage.py createsuperuser
```

Aucun identifiant ni mot de passe de démonstration n'est versionné.

## Lancement local

```bash
python manage.py runserver
```

Ouvrir :

- application : `http://127.0.0.1:8000/` ;
- administration Django : `http://127.0.0.1:8000/admin/`.

## Tests Django

```bash
pytest
```

La suite contient 111 tests unitaires et d'intégration lors de la vérification
finale du 15 juin 2026.

## Tests Playwright

Installer Chromium une seule fois si le navigateur n'est pas déjà disponible :

```bash
python -m playwright install chromium
```

Lancer les scénarios :

```bash
pytest e2e --browser chromium \
  --tracing=retain-on-failure \
  --output=test-results/playwright \
  -rP
```

La CI installe Chromium avec ses dépendances système :

```bash
python -m playwright install --with-deps chromium
```

## Couverture

```bash
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
```

Le seuil global bloquant est de 90 %. La couverture applicative observée lors
de la vérification finale est de 99,6 %. `coverage.xml` est généré localement et
ignoré par Git.

## Ruff

```bash
ruff check .
```

Ruff vérifie les erreurs Python, les imports, les modernisations et plusieurs
familles de défauts courants configurées dans `pyproject.toml`.

## GitHub Actions

Le workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) exécute :

1. Ruff ;
2. les checks Django ;
3. le contrôle des migrations ;
4. pytest avec couverture ;
5. la validation de `coverage.xml` ;
6. Playwright Chromium ;
7. l'analyse SonarQube Cloud si `SONAR_TOKEN` est disponible.

Le job principal est nommé `Django checks`.

## SonarQube Cloud

La configuration se trouve dans `sonar-project.properties`. SonarQube Cloud
analyse le Python, les templates Django et le workflow GitHub Actions, puis
importe `coverage.xml`.

Le secret `SONAR_TOKEN` doit être configuré dans GitHub et ne doit jamais être
versionné. Le check distant attendu est `SonarCloud Code Analysis`.

## Documentation

- état technique : [`docs/repository/current-state.md`](docs/repository/current-state.md) ;
- architecture : [`docs/repository/architecture.md`](docs/repository/architecture.md) ;
- stratégie de test : [`docs/repository/testing.md`](docs/repository/testing.md) ;
- exigences : [`docs/validation/exigences.md`](docs/validation/exigences.md) ;
- matrice de traçabilité :
  [`docs/validation/matrice_tracabilite.md`](docs/validation/matrice_tracabilite.md) ;
- rapport qualité :
  [`docs/validation/rapport_qualite.md`](docs/validation/rapport_qualite.md).

## Limites connues

- Le paiement est simulé ; aucun numéro de carte n'est stocké.
- Un panier actif est limité à un seul concert.
- SQLite est adapté à la démonstration locale, mais ne constitue pas une preuve
  de concurrence multi-processus en production.
- Les statuts `sold_out` et `finished` ne sont pas appliqués automatiquement ;
  la réservabilité contrôle directement le stock, la date et le statut.
- Les commandes refusées sont exclues de l'historique des achats payés.
- Bootstrap dépend de jsDelivr en usage normal.
- La performance est mesurée dans un environnement Chromium contrôlé.
- Aucun déploiement ou durcissement de production n'est fourni.
