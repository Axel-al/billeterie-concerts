# Etat courant du depot

Derniere mise a jour : 2026-04-26

## Synthese

Le depot contient maintenant une fondation Django executable pour la billetterie de concerts.

Elements livres dans cette etape :

- projet Django `config` ;
- applications Django `accounts`, `concerts` et `orders` ;
- modele utilisateur personnalise `accounts.User` avec email unique comme identifiant ;
- page d'accueil francaise minimale sur `/` ;
- template de base Bootstrap via CDN ;
- configuration pytest, coverage et Ruff dans `pyproject.toml` ;
- workflow GitHub Actions `.github/workflows/ci.yml` ;
- configuration SonarCloud `sonar-project.properties` ;
- premiers tests automatises et matrice de tracabilite mise a jour.

Le cahier des charges officiel reste conserve dans `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Exigences couvertes dans cette etape

Couverture revendiquee :

- `EF3` : couverture partielle seulement, via la fondation du modele utilisateur email + mot de passe. Aucun formulaire d'inscription n'est encore implemente.
- `EM8` : email utilisateur unique, teste au niveau modele.
- `ENF3` : mot de passe hashe via l'authentification Django, teste.
- `ENF5` : Ruff configure et execute en local/CI.
- `ENF6` : premiers tests automatises pytest-django et couverture.
- `ENF7` : pipeline GitHub Actions versionne.

Non couvert volontairement :

- `EF1`, `EF2`, `EF5` a `EF12` ;
- `EM1` a `EM7`, `EM9`, `EM10` ;
- toutes les regles `RG*` ;
- `ENF1`, car la page d'accueil ne donne pas encore acces aux actions metier principales.

## Structure applicative

- `config/` : settings, URLs racines, ASGI et WSGI.
- `accounts/` : modele utilisateur personnalise, manager, admin Django et migration initiale.
- `concerts/` : application creee, domaine metier non implemente.
- `orders/` : application creee, domaine metier non implemente.
- `templates/` : layout de base et page d'accueil.
- `tests/` : tests de smoke homepage et tests du modele utilisateur.

## Configuration locale

- Python observe : 3.12.13.
- Django observe : 5.2.13.
- SQLite est utilise en developpement local.
- `DJANGO_SECRET_KEY` est lu depuis l'environnement ; une valeur de developpement/test non-production est fournie par defaut.
- `DJANGO_DEBUG` pilote `DEBUG`, avec `True` par defaut en local.
- `DJANGO_ALLOWED_HOSTS` peut surcharger les hosts autorises ; la valeur par defaut couvre `localhost`, `127.0.0.1`, `[::1]` et `testserver`.
- `AUTH_USER_MODEL = "accounts.User"` est defini avant les futurs modeles dependants de l'utilisateur.

## Qualite et CI

Le workflow CI :

- se declenche sur toutes les branches et les pull requests ;
- installe les dependances de developpement ;
- installe Chromium pour Playwright ;
- execute Ruff ;
- execute `python manage.py check` ;
- execute pytest avec generation `coverage.xml` ;
- saute les tests e2e tant que le dossier `e2e/` n'existe pas ;
- lance SonarCloud seulement si le secret `SONAR_TOKEN` est disponible.

Etat distant observe :

- le workflow GitHub Actions a ete declenche par le push de la branche ;
- le workflow GitHub Actions est passe ;
- le check externe SonarCloud du commit `4e68e25` a echoue au Quality Gate car la couverture du nouveau code etait de 76,4 %, sous le seuil de 80 % ;
- la correction courante ajoute des tests de fondation et exclut uniquement `config/asgi.py` et `config/wsgi.py` de la couverture, car ce sont des entrypoints Django generes ;
- le check externe SonarCloud du correctif est passe avec 100,0 % de couverture sur le nouveau code ;
- la pull request #1 a ete creee et ses checks sont passes selon `gh pr checks` ;
- l'analyse SonarCloud depend toujours du secret GitHub `SONAR_TOKEN` pour les futures executions ;
- aucun scenario Playwright n'est encore present.

## Verification locale

Commandes lancees avec succes :

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
pytest
pytest --cov=. --cov-report=term-missing --cov-report=xml
python manage.py runserver 127.0.0.1:8010
curl -fsS http://127.0.0.1:8010/ | rg "Bienvenue sur la billetterie de concerts"
```

Resultats observes :

- `python manage.py check` : OK.
- `python manage.py makemigrations --check --dry-run` : OK, aucune migration manquante.
- `ruff check .` : OK.
- `pytest` : OK, 16 tests passent.
- `pytest --cov=. --cov-report=term-missing --cov-report=xml` : OK, 100 % de couverture locale sur les chemins mesures, `coverage.xml` genere puis ignore par Git.
- demarrage local : OK, la page `/` repond HTTP 200 ; Django signale seulement que les migrations locales doivent etre appliquees avec `python manage.py migrate` avant une utilisation persistante.

## Statut Git observe

- Branche de travail : `feature/django-technical-foundation`.
- Branche distante cible : `origin/feature/django-technical-foundation` apres push.
- Remote Git : `https://github.com/Axel-al/billeterie-concerts.git`.
- `AGENTS.md` est present localement et ignore via `.git/info/exclude`.
- `docs/prompts/` n'a pas ete lu.
- `db.sqlite3`, `coverage.xml`, caches Python/Ruff/pytest et environnements virtuels restent non versionnes.

## Prochaine etape recommandee

Ajouter les premiers modeles et vues `concerts`, puis relier les tests aux exigences `EF1`, `EF2` et `RG1` sans introduire encore le panier ou le paiement.
