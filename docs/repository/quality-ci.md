# Qualite et CI

## Etat actuel

La qualite et la CI sont configurees pour la fondation Django.

Elements deja presents :

- `requirements-dev.txt` declare Ruff, pytest, pytest-django, pytest-cov, coverage, factory-boy, freezegun et pytest-playwright.
- `pyproject.toml` configure Ruff, pytest et coverage.
- `.github/workflows/ci.yml` execute les checks sur les branches et les pull requests.
- `sonar-project.properties` configure le projet SonarCloud `Axel-al_billeterie-concerts`.

Etat distant observe :

- Le workflow GitHub Actions a ete execute avec succes sur la branche.
- Le check externe SonarCloud du commit `4e68e25` a echoue au Quality Gate avec 76,4 % de couverture sur le nouveau code, pour un seuil requis de 80 %.
- La correction courante augmente la couverture par des tests supplementaires et exclut seulement les entrypoints Django generes `config/asgi.py` et `config/wsgi.py` de la couverture.
- Le check externe SonarCloud du correctif est passe avec 100,0 % de couverture sur le nouveau code.
- La pull request #1 affiche des checks passants via `gh pr checks`.
- L'analyse SonarQube Cloud s'execute seulement si le secret GitHub `SONAR_TOKEN` est disponible.
- Les tests e2e ne sont pas encore versionnes ; la CI les ignore tant que `e2e/` n'existe pas.

## CI

Le pipeline GitHub Actions execute :

1. installation de Python ;
2. installation des dependances ;
3. installation de Chromium pour Playwright ;
4. `ruff check .` ;
5. `python manage.py check` ;
6. `pytest --cov=. --cov-report=xml` ;
7. tests e2e si le dossier `e2e/` existe ;
8. analyse SonarQube Cloud si `SONAR_TOKEN` est configure.

Versions d'actions utilisees :

- `actions/checkout@v6`
- `actions/setup-python@v6`
- `SonarSource/sonarqube-scan-action@v7.1.0`

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

SonarQube Cloud est configure sans secret versionne. Les sources declarees couvrent
tous les modules applicatifs existants : `config`, `accounts`, `concerts`, `cart`,
`orders` et `payments`. Les tests restent declares separement dans `tests`.

`config/asgi.py` et `config/wsgi.py` sont exclus uniquement de la couverture SonarCloud, car ce sont des fichiers Django generes et sans logique metier. Les verifier dans les tests n'apporterait pas de preuve fonctionnelle supplementaire.
