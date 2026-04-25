# Qualite et CI

## Etat actuel

La qualite et la CI sont planifiees mais pas encore implementees dans le depot.

Elements deja presents :

- `requirements-dev.txt` declare Ruff, pytest, pytest-django, pytest-cov, coverage, factory-boy, freezegun et pytest-playwright.
- Le depot Git existe et suit `origin/main`.
- Le token SonarQube est disponible localement selon le contexte fourni, mais aucun secret ni token n'est versionne.

Elements non presents :

- aucun workflow GitHub Actions ;
- aucun fichier de configuration SonarQube versionne ;
- aucun rapport de couverture ;
- aucun test automatise ;
- aucun code applicatif Django.

## CI cible

Le pipeline GitHub Actions devra executer au minimum :

1. installation de Python ;
2. installation des dependances ;
3. installation de Chromium pour Playwright si les tests e2e sont actifs ;
4. `ruff check .` ;
5. `pytest` ;
6. `pytest --cov=. --cov-report=xml` ;
7. analyse SonarQube Cloud si configuree.

Commande Chromium cible pour CI :

```bash
python -m playwright install --with-deps chromium
```

## Objectifs qualite initiaux

- Aucun secret versionne.
- Pas de mot de passe stocke en clair.
- Tests automatises relies aux exigences.
- Couverture mesuree avant toute revendication de qualite.
- Ruff sans erreur bloquante dans CI.

## Statut SonarQube

SonarQube Cloud est prevu. La configuration devra etre ajoutee dans une etape dediee, avec les secrets geres par GitHub et jamais dans le depot.
