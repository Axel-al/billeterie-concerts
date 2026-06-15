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

L'analyse Web des templates a conduit a deux corrections verifiees par
`tests/test_template_quality.py` :

- ajout des empreintes SRI et de `crossorigin="anonymous"` aux ressources
  Bootstrap 5.3.3 chargees depuis jsDelivr ;
- retrait de quatre roles `status` sur des messages rendus statiquement, sans
  changement de texte ni de comportement.

## Couverture

Coverage est configure dans `pyproject.toml`.

Commande verifiee :

```bash
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
```

Les applications sont declarees avec `source_pkgs` et `relative_files`. Le XML
conserve ainsi des chemins tels que `accounts/admin.py` au lieu de noms ambigus
comme `admin.py`. La CI verifie que chaque chemin est relatif et resolvable avant
de lancer SonarCloud.

Resultat local observe : 108 tests passent, la couverture applicative avec
branches atteint 99,6 % (813 instructions, 2 non couvertes, 102 branches), le
seuil de 90 % est respecte et les 35 chemins du XML sont valides. Le fichier
`coverage.xml` genere contient 37 553 octets.

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

Le commit fusionne `9bc8e69` a passe le job GitHub Actions `Django checks`, mais
le check externe SonarCloud `81334931351` a echoue avec 3,3 % de couverture du
nouveau code. Le log du scanner contenait :

```text
Cannot resolve the file path 'admin.py' of the coverage report, ambiguity,
the file exists in several 'source'.
Cannot resolve 7 file paths, ignoring coverage measures for those files
```

La pull request de correction est
`https://github.com/Axel-al/billeterie-concerts/pull/15`. Elle conserve la
definition distante `previous_version` et n'ajoute pas de
`sonar.projectVersion`; son objectif est uniquement de rendre le rapport de
couverture importable sans ambiguite et de corriger les constats Web observes.

`sonar.qualitygate.wait` n'est pas active. Les regles du depot imposent deja
`Django checks` et le check externe `SonarCloud Code Analysis`; ce dernier porte
le resultat du Quality Gate. Une PR de fork peut ne pas recevoir le secret et
rester bloquee jusqu'a une analyse depuis un contexte de confiance.

## Risques actuels

- Les tests de consultation de commandes couvrent l'historique paye et le detail filtre par proprietaire ; les tentatives refusees restent exclues de l'historique des achats.
- Le rollback en cas d'echec du decrement conditionnel est teste, mais les tests de concurrence multi-processus restent a approfondir.
- Le premier scenario Playwright couvre le parcours nominal seulement ; les parcours d'erreur e2e restent optionnels et sont couverts par les tests d'integration Django.
- `ENF2` reste non mesuree : aucun test de performance a deux secondes n'est revendique.
