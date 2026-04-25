# Rapport qualite

Derniere mise a jour : 2026-04-25

## Etat actuel

Le depot est en phase de baseline. Il contient les requirements et la documentation de validation, mais pas encore de code applicatif Django ni de tests automatises.

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

Ruff est declare mais aucun check n'a encore ete execute sur du code applicatif, car il n'existe pas de code applicatif.

## Couverture

Aucun rapport de couverture n'existe pour l'instant.

## CI

Aucun workflow GitHub Actions n'est versionne pour l'instant. La CI devra etre ajoutee dans une etape dediee.

## SonarQube

SonarQube Cloud est planifie. Le token local mentionne dans le contexte ne doit pas etre versionne. La configuration devra passer par les secrets GitHub.

## Risques actuels

- Les exigences ne sont pas encore prouvees par des tests.
- La CI n'empeche pas encore les regressions.
- Les choix de decoupage Django restent a confirmer lors de l'initialisation du projet.

## Prochaines actions qualite

1. Initialiser Django dans l'etape dediee.
2. Ajouter une configuration minimale Ruff si necessaire.
3. Ajouter les premiers tests unitaires des regles critiques.
4. Ajouter GitHub Actions.
5. Ajouter la configuration SonarQube Cloud sans secret versionne.
