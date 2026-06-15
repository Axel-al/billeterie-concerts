# Qualité et CI

## État actuel

La chaîne qualité couvre les exigences `ENF5`, `ENF6` et `ENF7` avec :

- Ruff pour l'analyse statique ;
- pytest et pytest-django pour les tests unitaires et d'intégration ;
- coverage.py avec couverture de branches ;
- pytest-playwright pour le scénario fonctionnel nominal et la mesure `ENF2` ;
- GitHub Actions pour l'exécution automatique ;
- SonarQube Cloud pour le Quality Gate externe.

## Couverture

Les packages applicatifs mesurés sont déclarés avec `source_pkgs` dans
`pyproject.toml` : `accounts`, `concerts`, `cart`, `orders`, `payments` et
`config`. Les tests ne font pas partie du dénominateur.

Configuration :

- couverture de branches activée ;
- chemins relatifs au dépôt avec le nom du package conservé ;
- précision à une décimale ;
- seuil global bloquant de 90 % ;
- rapport terminal avec lignes manquantes ;
- rapport XML `coverage.xml` pour SonarCloud.

Commande de référence :

```bash
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
```

Le validateur XML vérifie que chaque fichier mesuré utilise un chemin relatif
unique résolvable depuis la racine, par exemple `accounts/admin.py`. Il empêche
le retour de chemins ambigus tels que `admin.py`, que SonarCloud ne peut pas
associer à une application Django lorsque plusieurs packages possèdent ce nom.

Le seuil est un garde-fou, pas un objectif à maximiser artificiellement. Il ne
doit pas conduire à exclure du code applicatif ou à ajouter des tests sans valeur
fonctionnelle. Les règles de stock, quantité, paiement, isolation et permissions
restent prioritaires.

Exclusions justifiées :

- migrations Django générées ;
- `config/asgi.py` et `config/wsgi.py`, entrypoints générés sans logique métier ;
- `manage.py`, lanceur Django sans logique applicative.

## CI

Le job conserve le nom `Django checks`, requis par les règles du dépôt. Il
exécute, dans cet ordre :

1. checkout complet pour l'analyse Sonar ;
2. installation de Python 3.12 et des dépendances verrouillées ;
3. `ruff check .` ;
4. `python manage.py check` ;
5. `python manage.py makemigrations --check --dry-run` ;
6. pytest avec couverture terminale, XML et seuil de 90 % ;
7. validation des chemins de fichiers de `coverage.xml` ;
8. installation Chromium après les checks rapides ;
9. scénarios Playwright Chromium, dont la mesure `ENF2`, avec traces conservées en cas d'échec et diagnostics des tests passés ;
10. publication de `test-results/` si le job échoue ;
11. analyse SonarCloud si `SONAR_TOKEN` est disponible.

Les actions sont épinglées par SHA immuable, avec la version en commentaire :

- `actions/checkout` v6.0.3
- `actions/setup-python` v6.2.0
- `actions/upload-artifact` v4.6.2
- `SonarSource/sonarqube-scan-action` v8.2.0

`requirements-ci.txt`, généré avec `pip-compile`, verrouille les versions
directes et transitives du job Python 3.12 ainsi que les empreintes SHA-256 des
artefacts acceptés. L'installation utilise `--require-hashes` et
`--only-binary=:all:` pour vérifier les distributions téléchargées et éviter
l'exécution de scripts de construction issus de distributions source. Les
manifests `requirements.txt` et `requirements-dev.txt` conservent les plages de
versions supportées pour le développement ; le lock CI doit être régénéré et
validé délibérément lors de leur mise à jour.

Commande de régénération utilisée avec `pip-tools` 7.5.3 :

```bash
pip-compile --allow-unsafe --generate-hashes --no-emit-index-url \
  --output-file=requirements-ci.txt --strip-extras requirements-dev.txt
```

## SonarQube Cloud

Le projet `Axel-al_billeterie-concerts` analyse :

- les packages Python applicatifs ;
- les templates Django ;
- les workflows GitHub Actions ;
- les tests `tests/` et `e2e/` comme sources de test séparées ;
- `coverage.xml` comme rapport de couverture Python.

Les constats Web sont traités dans les templates : les ressources Bootstrap
chargées depuis jsDelivr utilisent SRI et les messages rendus statiquement ne
déclarent pas de zone live `status`. `tests/test_template_quality.py` protège
ces choix contre une régression.

Le Quality Gate distant conserve notamment le seuil de 80 % sur la couverture
du nouveau code. `sonar.qualitygate.wait` n'est pas activé : les règles du dépôt
exigent déjà les checks distincts `Django checks` et
`SonarCloud Code Analysis`. Le check Sonar externe est donc l'autorité pour le
Quality Gate sans bloquer inutilement le job Django en attente du traitement
serveur.

L'analyse CI reste conditionnelle à `SONAR_TOKEN`, qui n'est pas versionné. Les
secrets GitHub ne sont normalement pas transmis aux workflows de pull requests
issues de forks : le scanner peut alors être ignoré et le check Sonar requis
peut bloquer la fusion jusqu'à une exécution depuis une branche de confiance.

## Diagnostic

En cas d'échec :

```bash
gh run view --log-failed
gh checks <sha>
gh check-detail <check-run-id>
```

`gh check-detail` est la commande de référence pour lire le résultat du Quality
Gate SonarCloud.

## Mesure ENF2

La mesure `ENF2` est exécutée dans le même job que les autres tests Playwright :

```bash
pytest e2e --browser chromium --tracing=retain-on-failure --output=test-results/playwright -rP
```

Elle utilise `live_server`, une base de test créée par `pytest-django`, un
viewport desktop 1366x768, aucune limitation CPU/réseau et des fixtures locales
pour rejouer les vrais fichiers Bootstrap 5.3.3 normalement servis par jsDelivr.
Cette preuve valide le rendu sous conditions CI contrôlées ; elle ne remplace
pas une campagne de performance production multi-appareils ou multi-réseaux.
