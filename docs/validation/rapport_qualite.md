# Rapport qualite

Derniere mise a jour : 2026-04-25

## Etat actuel

Le depot contient une fondation Django executable, des premiers tests automatises, Ruff, coverage, GitHub Actions et une configuration SonarCloud sans secret versionne.

## Outillage declare

| Outil | Declaration | Statut |
| --- | --- | --- |
| Django | `requirements.txt` | Dependence runtime declaree |
| python-dotenv | `requirements.txt` | Dependence runtime declaree |
| pytest | `requirements-dev.txt` | Tests prevus |
| pytest-django | `requirements-dev.txt` | Tests Django prevus |
| pytest-cov / coverage | `requirements-dev.txt` | Couverture prevue |
| Ruff | `requirements-dev.txt` | Analyse statique prevue |
| freezegun | `requirements-dev.txt` | Tests dates prevus |
| factory-boy | `requirements-dev.txt` | Donnees de test prevues |
| pytest-playwright | `requirements-dev.txt` | Tests e2e prevus |

## Analyse statique

Ruff est configure dans `pyproject.toml` et execute en local ainsi qu'en CI.

Commande verifiee :

```bash
ruff check .
```

Resultat observe : OK.

## Couverture

Coverage est configure dans `pyproject.toml`.

Commande verifiee :

```bash
pytest --cov=. --cov-report=xml
```

Resultat observe : OK, `coverage.xml` est genere et reste non versionne.

## CI

Le workflow `.github/workflows/ci.yml` est versionne et a ete execute avec succes sur la branche. Il execute Ruff, les checks Django, pytest avec couverture, installe Chromium pour Playwright et saute les tests e2e tant que le dossier `e2e/` n'existe pas.

## SonarQube

SonarCloud est configure par `sonar-project.properties`. L'analyse CI s'execute seulement si le secret GitHub `SONAR_TOKEN` est disponible.

## Risques actuels

- Les tests actuels couvrent seulement la fondation utilisateur et qualite.
- Les exigences metier de concerts, stock, panier, paiement et commandes restent a implementer et tester.

## Prochaines actions qualite

1. Ajouter les premiers tests des concerts (`EF1`, `EF2`, `RG1`).
2. Ajouter progressivement les tests metier critiques de stock, quantite et paiement.
3. Ajouter un premier scenario Playwright quand un parcours utilisateur existe.
