# Rapport qualité

Dernière mise à jour : 2026-06-15

## État actuel

Le dépôt contient une application Django exécutable avec tests automatisés,
scénario Playwright nominal, mesure Playwright `ENF2`, Ruff, couverture de
branches, seuil local de 90 %, GitHub Actions et configuration SonarCloud sans
secret versionné.

## Outillage déclaré

| Outil | Déclaration | Statut |
| --- | --- | --- |
| Django | `requirements.txt` | Dépendance runtime déclarée |
| python-dotenv | `requirements.txt` | Dépendance runtime déclarée |
| pytest | `requirements-dev.txt` | Tests exécutés localement et en CI |
| pytest-django | `requirements-dev.txt` | Intégration Django exécutée |
| pytest-cov / coverage | `requirements-dev.txt`, `pyproject.toml` | Branches, XML et seuil global 90 % |
| Ruff | `requirements-dev.txt`, `pyproject.toml` | Analyse statique bloquante |
| freezegun | `requirements-dev.txt` | Dates stabilisées dans les tests concernés |
| factory-boy | `requirements-dev.txt` | Disponible ; non requis par les fixtures actuelles |
| pytest-playwright | `requirements-dev.txt`, `e2e/` | Scénario e2e nominal et mesure `ENF2` versionnés |

## Analyse statique

Ruff est configuré dans `pyproject.toml` et exécuté en local ainsi qu'en CI.

Commande vérifiée :

```bash
ruff check .
```

Résultat observé : OK.

L'analyse Web des templates a conduit à deux corrections vérifiées par
`tests/test_template_quality.py` :

- ajout des empreintes SRI et de `crossorigin="anonymous"` aux ressources
  Bootstrap 5.3.3 chargées depuis jsDelivr ;
- retrait de quatre rôles `status` sur des messages rendus statiquement, sans
  changement de texte ni de comportement.

## Couverture

Coverage est configuré dans `pyproject.toml`.

Commande vérifiée :

```bash
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
```

Les applications sont déclarées avec `source_pkgs` et `relative_files`. Le XML
conserve ainsi des chemins tels que `accounts/admin.py` au lieu de noms ambigus
comme `admin.py`. La CI vérifie que chaque chemin est relatif et résolvable avant
de lancer SonarCloud.

Résultat local observé : 108 tests passent, la couverture applicative avec
branches atteint 99,6 % (813 instructions, 2 non couvertes, 102 branches), le
seuil de 90 % est respecté et les 35 chemins du XML sont valides. Le fichier
`coverage.xml` généré contient 37 553 octets.

Exclusions justifiées :

- `config/asgi.py`
- `config/wsgi.py`

Ces deux fichiers sont des entrypoints Django générés, sans logique applicative propre.

## Tests fonctionnels

Commande vérifiée :

```bash
pytest e2e --browser chromium --tracing=retain-on-failure --output=test-results/playwright -rP
```

Résultat observé : OK, le scénario nominal et les 4 mesures `ENF2` passent. Les scénarios créent leurs données via `pytest-django` et `live_server` dans la base de test, sans dépendance à `db.sqlite3`.

Mesure `ENF2` locale observée sous Chromium, viewport 1366x768, contexte froid
par page, sans throttling CPU/réseau, Bootstrap 5.3.3 rejoué depuis fixtures
locales conformes SRI :

| Page | LCP observé | Durée load observée |
| --- | ---: | ---: |
| Accueil `/` | 72 ms | 67,6 ms |
| Catalogue `/concerts/` | 60 ms | 57,4 ms |
| Fiche concert `/concerts/<id>/` | 48 ms | 45,6 ms |
| Historique authentifié `/commandes/` | 44 ms | 40,1 ms |

Le seuil `ENF2` reste 2 000 ms. Cette mesure valide le rendu navigateur sous
conditions CI contrôlées ; elle ne prouve pas la performance production sur tous
les appareils, états CDN ou réseaux.

## CI

Le workflow `.github/workflows/ci.yml` est versionné. Il exécute Ruff, les
checks Django, le contrôle de migrations, pytest avec couverture, puis installé
Chromium et lance Playwright en ciblant explicitement Chromium avec les
diagnostics des tests passés. Les traces sont publiées si le job échoue. La
couverture terminale rend les logs directement exploitables.

L'analyse Sonar du workflow a détecté des références d'actions non immuables et
une installation Python non verrouillée. Les actions sont maintenant épinglées
par SHA, `requirements-ci.txt` fixe les versions directes et transitives avec
leurs empreintes SHA-256, `--require-hashes` vérifie les artefacts téléchargés et
`--only-binary=:all:` interdit les distributions source en CI.

Le lock a été validé dans un environnement Python 3.12 vierge avec :

```bash
python -m pip install --only-binary=:all: --require-hashes -r requirements-ci.txt
python -m pip check
```

Résultat : installation réussie et aucune dépendance incompatible.

## SonarQube

SonarCloud est configuré par `sonar-project.properties`. Les sources incluent les
packages applicatifs, les templates Django et les workflows GitHub Actions. Les
tests `tests/` et `e2e/` restent déclarés séparément. L'analyse CI utilise la
version 8.2.0 de `SonarSource/sonarqube-scan-action`, épinglée par SHA, seulement
si `SONAR_TOKEN` est disponible.

Le commit fusionne `9bc8e69` a passé le job GitHub Actions `Django checks`, mais
le check externe SonarCloud `81334931351` a échoue avec 3,3 % de couverture du
nouveau code. Le log du scanner contenait :

```text
Cannot resolve the file path 'admin.py' of the coverage report, ambiguity,
the file exists in several 'source'.
Cannot resolve 7 file paths, ignoring coverage measures for those files
```

La pull request de correction est
`https://github.com/Axel-al/billeterie-concerts/pull/15`. Elle conserve la
définition distante `previous_version` et n'ajoute pas de
`sonar.projectVersion`; son objectif est uniquement de rendre le rapport de
couverture importable sans ambiguïté et de corriger les constats Web observés.

`sonar.qualitygate.wait` n'est pas activé. Les règles du dépôt imposent déjà
`Django checks` et le check externe `SonarCloud Code Analysis`; ce dernier porte
le résultat du Quality Gate. Une PR de fork peut ne pas recevoir le secret et
rester bloquée jusqu'à une analyse depuis un contexte de confiance.

## Risques actuels

- Les tests de consultation de commandes couvrent l'historique payé et le détail filtré par propriétaire ; les tentatives refusées restent exclues de l'historique des achats.
- Le rollback en cas d'échec du décrément conditionnel est testé, mais les tests de concurrence multi-processus restent à approfondir.
- Le premier scénario Playwright couvre le parcours nominal seulement ; les parcours d'erreur e2e restent optionnels et sont couverts par les tests d'intégration Django.
- `ENF2` est mesurée en laboratoire CI contrôlé : la preuve ne couvre pas toutes les conditions de production, appareils, états CDN ou réseaux.
