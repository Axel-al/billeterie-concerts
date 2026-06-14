# Rapport qualite

Derniere mise a jour : 2026-06-14

## Etat actuel

Le depot contient une application Django executable avec comptes, catalogue, panier, checkout, paiement simule, tests automatises, un scenario Playwright nominal, Ruff, coverage, GitHub Actions et une configuration SonarCloud sans secret versionne.

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
| pytest-playwright | `requirements-dev.txt`, `e2e/test_nominal_booking_flow.py` | Scenario e2e nominal versionne |

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
pytest --cov=. --cov-report=term-missing --cov-report=xml
```

Resultat observe le plus recent : voir `docs/repository/current-state.md`.

Exclusions justifiees :

- `config/asgi.py`
- `config/wsgi.py`

Ces deux fichiers sont des entrypoints Django generes, sans logique applicative propre.

## Tests fonctionnels

Commande verifiee :

```bash
pytest e2e --tracing=retain-on-failure --output=test-results/playwright
```

Resultat observe : OK, 1 scenario Playwright passe. Le scenario cree ses donnees via `pytest-django` et `live_server` dans la base de test, sans dependance a `db.sqlite3`.

## CI

Le workflow `.github/workflows/ci.yml` est versionne. Il execute Ruff, les checks Django, pytest avec couverture, installe Chromium pour Playwright, lance `pytest e2e --tracing=retain-on-failure --output=test-results/playwright` et publie `test-results/` en artefact si un echec survient.

## SonarQube

SonarCloud est configure par `sonar-project.properties`. L'analyse CI s'execute seulement si le secret GitHub `SONAR_TOKEN` est disponible.

Le check externe SonarCloud du commit `4e68e25` a echoue car la couverture du nouveau code etait de 76,4 % pour un seuil de 80 %. La correction courante ajoute des tests et exclut seulement le boilerplate Django ASGI/WSGI de la couverture.

Le check externe SonarCloud du correctif est passe avec 100,0 % de couverture sur le nouveau code. La pull request #1 affiche des checks passants via `gh pr checks`.

## Risques actuels

- Les tests de consultation de commandes couvrent l'historique paye et le detail filtre par proprietaire ; les tentatives refusees restent exclues de l'historique des achats.
- Les tests de concurrence multi-processus sur le stock restent a approfondir.
- Le premier scenario Playwright couvre le parcours nominal seulement ; les parcours d'erreur e2e restent optionnels et sont couverts par les tests d'integration Django.

## Prochaines actions qualite

1. Verifier les checks distants de la pull request e2e.
2. Approfondir les tests de concurrence autour du stock.
