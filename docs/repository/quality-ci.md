# Qualite et CI

## Etat actuel

La chaine qualite couvre les exigences `ENF5`, `ENF6` et `ENF7` avec :

- Ruff pour l'analyse statique ;
- pytest et pytest-django pour les tests unitaires et d'integration ;
- coverage.py avec couverture de branches ;
- pytest-playwright pour le scenario fonctionnel nominal ;
- GitHub Actions pour l'execution automatique ;
- SonarQube Cloud pour le Quality Gate externe.

## Couverture

Les packages applicatifs mesures sont declares avec `source_pkgs` dans
`pyproject.toml` : `accounts`, `concerts`, `cart`, `orders`, `payments` et
`config`. Les tests ne font pas partie du denominateur.

Configuration :

- couverture de branches activee ;
- chemins relatifs au depot avec le nom du package conserve ;
- precision a une decimale ;
- seuil global bloquant de 90 % ;
- rapport terminal avec lignes manquantes ;
- rapport XML `coverage.xml` pour SonarCloud.

Commande de reference :

```bash
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
```

Le validateur XML verifie que chaque fichier mesure utilise un chemin relatif
unique resolvable depuis la racine, par exemple `accounts/admin.py`. Il empeche
le retour de chemins ambigus tels que `admin.py`, que SonarCloud ne peut pas
associer a une application Django lorsque plusieurs packages possedent ce nom.

Le seuil est un garde-fou, pas un objectif a maximiser artificiellement. Il ne
doit pas conduire a exclure du code applicatif ou a ajouter des tests sans valeur
fonctionnelle. Les regles de stock, quantite, paiement, isolation et permissions
restent prioritaires.

Exclusions justifiees :

- migrations Django generees ;
- `config/asgi.py` et `config/wsgi.py`, entrypoints generes sans logique metier ;
- `manage.py`, lanceur Django sans logique applicative.

## CI

Le job conserve le nom `Django checks`, requis par les regles du depot. Il
execute, dans cet ordre :

1. checkout complet pour l'analyse Sonar ;
2. installation de Python 3.12 et des dependances verrouillees ;
3. `ruff check .` ;
4. `python manage.py check` ;
5. `python manage.py makemigrations --check --dry-run` ;
6. pytest avec couverture terminale, XML et seuil de 90 % ;
7. validation des chemins de fichiers de `coverage.xml` ;
8. installation Chromium apres les checks rapides ;
9. scenario Playwright avec trace conservee en cas d'echec ;
10. publication de `test-results/` si le job echoue ;
11. analyse SonarCloud si `SONAR_TOKEN` est disponible.

Les actions sont epinglees par SHA immuable, avec la version en commentaire :

- `actions/checkout` v6.0.3
- `actions/setup-python` v6.2.0
- `actions/upload-artifact` v4.6.2
- `SonarSource/sonarqube-scan-action` v8.2.0

`requirements-ci.txt`, genere avec `pip-compile`, verrouille les versions
directes et transitives du job Python 3.12 ainsi que les empreintes SHA-256 des
artefacts acceptes. L'installation utilise `--require-hashes` et
`--only-binary=:all:` pour verifier les distributions telechargees et eviter
l'execution de scripts de construction issus de distributions source. Les
manifests `requirements.txt` et `requirements-dev.txt` conservent les plages de
versions supportees pour le developpement ; le lock CI doit etre regenere et
valide deliberement lors de leur mise a jour.

Commande de regeneration utilisee avec `pip-tools` 7.5.3 :

```bash
pip-compile --allow-unsafe --generate-hashes --no-emit-index-url \
  --output-file=requirements-ci.txt --strip-extras requirements-dev.txt
```

## SonarQube Cloud

Le projet `Axel-al_billeterie-concerts` analyse :

- les packages Python applicatifs ;
- les templates Django ;
- les workflows GitHub Actions ;
- les tests `tests/` et `e2e/` comme sources de test separees ;
- `coverage.xml` comme rapport de couverture Python.

Les constats Web sont traites dans les templates : les ressources Bootstrap
chargees depuis jsDelivr utilisent SRI et les messages rendus statiquement ne
declarent pas de zone live `status`. `tests/test_template_quality.py` protege
ces choix contre une regression.

Le Quality Gate distant conserve notamment le seuil de 80 % sur la couverture
du nouveau code. `sonar.qualitygate.wait` n'est pas active : les regles du depot
exigent deja les checks distincts `Django checks` et
`SonarCloud Code Analysis`. Le check Sonar externe est donc l'autorite pour le
Quality Gate sans bloquer inutilement le job Django en attente du traitement
serveur.

L'analyse CI reste conditionnelle a `SONAR_TOKEN`, qui n'est pas versionne. Les
secrets GitHub ne sont normalement pas transmis aux workflows de pull requests
issues de forks : le scanner peut alors etre ignore et le check Sonar requis
peut bloquer la fusion jusqu'a une execution depuis une branche de confiance.

## Diagnostic

En cas d'echec :

```bash
gh run view --log-failed
gh checks <sha>
gh check-detail <check-run-id>
```

`gh check-detail` est la commande de reference pour lire le resultat du Quality
Gate SonarCloud.
