# Rapport qualite

Derniere mise a jour : 2026-06-15

## Etat actuel

Le depot contient une application Django executable avec tests automatises,
scenario Playwright nominal, Ruff, couverture de branches, seuil local de 90 %,
GitHub Actions et configuration SonarCloud sans secret versionne.

## Outillage declare

| Outil | Declaration | Statut |
| --- | --- | --- |
| Django | `requirements.txt` | Dependence runtime declaree |
| python-dotenv | `requirements.txt` | Dependence runtime declaree |
| pytest | `requirements-dev.txt` | Tests executes localement et en CI |
| pytest-django | `requirements-dev.txt` | Integration Django executee |
| pytest-cov / coverage | `requirements-dev.txt`, `pyproject.toml` | Branches, XML et seuil global 90 % |
| Ruff | `requirements-dev.txt`, `pyproject.toml` | Analyse statique bloquante |
| freezegun | `requirements-dev.txt` | Dates stabilisees dans les tests concernes |
| factory-boy | `requirements-dev.txt` | Disponible ; non requis par les fixtures actuelles |
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
pytest --cov --cov-report=term-missing --cov-report=xml
```

Resultat final observe : 106 tests passent, la couverture applicative avec
branches atteint 99,6 % (813 instructions, 2 non couvertes, 102 branches), le
seuil de 90 % est respecte et `coverage.xml` est genere avec 11 063 octets.

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

Le workflow `.github/workflows/ci.yml` est versionne. Il execute Ruff, les
checks Django, le controle de migrations, pytest avec couverture, puis installe
Chromium et lance Playwright. Les traces sont publiees si le job echoue. La
couverture terminale rend les logs directement exploitables.

L'analyse Sonar du workflow a detecte des references d'actions non immuables et
une installation Python non verrouillee. Les actions sont maintenant epinglees
par SHA, `requirements-ci.txt` fixe les versions directes et transitives avec
leurs empreintes SHA-256, `--require-hashes` verifie les artefacts telecharges et
`--only-binary=:all:` interdit les distributions source en CI.

Le lock a ete valide dans un environnement Python 3.12 vierge avec :

```bash
python -m pip install --only-binary=:all: --require-hashes -r requirements-ci.txt
python -m pip check
```

Resultat : installation reussie et aucune dependance incompatible.

## SonarQube

SonarCloud est configure par `sonar-project.properties`. Les sources incluent les
packages applicatifs, les templates Django et les workflows GitHub Actions. Les
tests `tests/` et `e2e/` restent declares separement. L'analyse CI utilise la
version 8.2.0 de `SonarSource/sonarqube-scan-action`, epinglee par SHA, seulement
si `SONAR_TOKEN` est disponible.

Le commit de configuration `086e7fa` a passe les deux runs GitHub Actions :

- push `27519339493`, job `Django checks` `81334046774` ;
- pull request `27519340500`, job `Django checks` `81334049790`.

Le check externe SonarCloud `81334229776` a passe avec 0 nouvelle issue et
0 Security Hotspot. Il affiche 0,0 % de couverture du nouveau code, ce qui est
coherent avec l'absence de nouvelle ligne executable dans les packages
applicatifs ; la branche ajoute un test et de la configuration. La couverture
applicative locale globale mesuree reste 99,6 %.

Commandes de diagnostic executees :

```bash
gh pr checks 14 --watch --interval 10
gh checks 086e7fa966d083658ab655fbf9c6d213da0c22f3
gh check-detail 81334229776
gh run view 27519340500 --log-failed
```

Les trois checks sont passes. La derniere commande n'a produit aucun log
d'echec, le run etant reussi.

Les appels sans authentification aux API publiques de mesures et de Quality
Gate SonarCloud ont retourne HTTP 403. Le detail disponible via
`gh check-detail 81334229776` et le tableau de bord lie constituent donc la
preuve distante retenue.

`sonar.qualitygate.wait` n'est pas active. Les regles du depot imposent deja
`Django checks` et le check externe `SonarCloud Code Analysis`; ce dernier porte
le resultat du Quality Gate. Une PR de fork peut ne pas recevoir le secret et
rester bloquee jusqu'a une analyse depuis un contexte de confiance.

## Risques actuels

- Les tests de consultation de commandes couvrent l'historique paye et le detail filtre par proprietaire ; les tentatives refusees restent exclues de l'historique des achats.
- Le rollback en cas d'echec du decrement conditionnel est teste, mais les tests de concurrence multi-processus restent a approfondir.
- Le premier scenario Playwright couvre le parcours nominal seulement ; les parcours d'erreur e2e restent optionnels et sont couverts par les tests d'integration Django.
- `ENF2` reste non mesuree : aucun test de performance a deux secondes n'est revendique.
