# Qualité et CI

## Objectifs

La chaîne qualité couvre `ENF5`, `ENF6` et `ENF7` avec :

- Ruff ;
- pytest et pytest-django ;
- coverage.py avec branches ;
- Playwright Chromium ;
- GitHub Actions ;
- SonarQube Cloud.

## Analyse statique

Commande locale :

```bash
ruff check .
```

Ruff utilise Python 3.12, une longueur de ligne de 88 caractères et les familles
`E`, `F`, `I`, `UP` et `B`. Les migrations générées sont exclues.

## Couverture

Commande :

```bash
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
```

Configuration :

- couverture de branches ;
- packages applicatifs explicites ;
- chemins relatifs ;
- précision à une décimale ;
- seuil bloquant de 90 % ;
- XML destiné à SonarQube Cloud.

Résultat final local : 99,6 % sur 838 instructions et 102 branches.

Le validateur XML vérifie que chaque chemin est relatif, résolvable et non
ambigu. Il évite que SonarQube ignore des fichiers portant le même nom dans
plusieurs applications Django.

## Workflow GitHub Actions

Le fichier `.github/workflows/ci.yml` déclenche le job `Django checks` sur les
pushes et les pull requests.

Étapes :

1. checkout avec historique complet ;
2. Python 3.12 ;
3. installation verrouillée de `requirements-ci.txt` ;
4. Ruff ;
5. `python manage.py check` ;
6. contrôle des migrations ;
7. pytest, couverture terminale et XML ;
8. validation des chemins de couverture ;
9. installation Chromium avec ses dépendances ;
10. tests Playwright et diagnostics ;
11. traces Playwright publiées en cas d'échec ;
12. analyse SonarQube Cloud si le secret est disponible.

## Sécurité de la chaîne d'approvisionnement

- Les actions GitHub sont épinglées par SHA immuable.
- `requirements-ci.txt` verrouille les versions et empreintes SHA-256.
- La CI impose `--require-hashes`.
- La CI impose `--only-binary=:all:`.
- Aucun secret n'est écrit dans le dépôt.

Pour régénérer le lock avec `pip-tools` :

```bash
pip-compile --allow-unsafe --generate-hashes --no-emit-index-url \
  --output-file=requirements-ci.txt --strip-extras requirements-dev.txt
```

Une régénération doit être revue et testée sous Python 3.12.

## SonarQube Cloud

Le projet `Axel-al_billeterie-concerts` analyse :

- les packages Python ;
- les templates Django ;
- `.github/workflows` ;
- les tests comme sources de test ;
- `coverage.xml`.

Le Quality Gate externe reste distinct du job `Django checks`.
`sonar.qualitygate.wait` n'est pas activé, car GitHub reçoit déjà le check
`SonarCloud Code Analysis`.

Le check de référence sur `main`, commit `946ad8c`, a réussi le 15 juin 2026
avec 0 nouvelle anomalie, 0 hotspot, 99,5 % de couverture du nouveau code et
0,0 % de duplication du nouveau code.

L'analyse dépend de `SONAR_TOKEN`. Une pull request issue d'un fork peut ne pas
recevoir ce secret et rester sans analyse.

## Diagnostic distant

```bash
gh run list
gh run view --log-failed
gh checks <sha>
gh check-detail <check-run-id>
gh pr checks
```

`gh check-detail` doit être utilisé pour examiner un résultat SonarQube Cloud.

## Performance

La CI exécute :

```bash
pytest e2e --browser chromium \
  --tracing=retain-on-failure \
  --output=test-results/playwright \
  -rP
```

La mesure `ENF2` utilise un environnement local contrôlé, sans limitation
CPU/réseau. Elle valide le seuil de 2 000 ms dans ces conditions uniquement.

## Artefacts ignorés

Ne sont pas versionnés :

- `coverage.xml`, `.coverage` et `htmlcov/` ;
- `test-results/` et `playwright-report/` ;
- `db.sqlite3` ;
- `.env` ;
- caches Python, pytest et Ruff ;
- environnements virtuels.
