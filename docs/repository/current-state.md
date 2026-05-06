# Etat courant du depot

Derniere mise a jour : 2026-05-06

## Synthese

Le depot contient maintenant une fondation Django executable et un noyau domaine teste pour la billetterie de concerts.

Elements livres dans cette etape :

- applications Django `cart` et `payments` ajoutees a cote de `accounts`, `concerts` et `orders` ;
- modeles `Concert`, `SeatCategory`, `Cart`, `CartLine`, `Order`, `OrderLine` et `Payment` ;
- migrations initiales pour `concerts`, `cart`, `orders` et `payments` ;
- services domaine pour l'ajout panier, l'eligibilite de reservation, la validation de quantite, la validation de stock, le paiement simule et le prix snapshot ;
- administration Django pour les nouveaux modeles ;
- commande idempotente `python manage.py seed_demo_data` ;
- tests automatises des regles critiques ;
- passe de couverture complementaire sur les branches utiles signalees par `coverage.xml` ;
- documentation de donnees, regles domaine, validation et tracabilite mise a jour.

Le cahier des charges officiel reste conserve dans `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Exigences couvertes dans cette etape

Couverture revendiquee :

- `EF5` : couverture partielle domaine/service pour l'ajout de billets au panier, sans formulaire ni UI.
- `EF6` : couverture partielle domaine pour le total de panier, sans affichage.
- `EF7` : couverture partielle domaine/service pour le paiement simule, sans page paiement.
- `EF8` : couverture partielle domaine/service pour la commande payee, sans confirmation affichee.
- `EF9` : couverture partielle domaine/service pour la commande refusee et le stock inchange, sans message explicite affiche.
- `EF12` : stock decremente apres paiement accepte au niveau service.
- `EM1` a `EM7` et `EM10` : regles couvertes au niveau domaine/service.
- `RG1` a `RG5` : regles couvertes au niveau domaine/service.
- `RG7` : couverture partielle domaine par refus des concerts annules.
- `ENF4` et `ENF6` : saisies invalides rejetees proprement par les services et tests automatises.

Couverture existante conservee :

- `EF3` : couverture partielle modele/auth via utilisateur email + mot de passe.
- `EM8` : email utilisateur unique.
- `ENF3` : mot de passe hashe via Django.
- `ENF5` et `ENF7` : Ruff, coverage et GitHub Actions versionnes.

Non couvert volontairement :

- `EF1`, `EF2`, `EF4`, `EF10` ;
- confirmation affichee de `EF8` et message explicite affiche de `EF9` ;
- `RG6` et `RG8` ;
- couverture fonctionnelle complete de `EF11`/`EM9` au-dela de la fondation admin Django.

## Structure applicative

- `config/` : settings, URLs racines, ASGI et WSGI.
- `accounts/` : modele utilisateur personnalise, manager, admin Django et migration initiale.
- `concerts/` : concerts, categories de places, statuts, stock, admin et commande `seed_demo_data`.
- `cart/` : panier actif mono-concert, lignes de panier et services de validation/ajout.
- `orders/` : commandes, lignes de commandes et prix snapshots.
- `payments/` : paiement simule et service transactionnel.
- `templates/` : layout de base et page d'accueil.
- `tests/` : tests de smoke homepage, settings, utilisateur et domaine billetterie.

## Regles domaine implementees

- Un concert est reservable seulement s'il est strictement futur, `open` et avec au moins une categorie en stock.
- Les concerts passes ou annules ne sont pas reservables.
- Une quantite doit etre un entier entre 1 et 6.
- Le plafond de 6 billets est applique au total du panier/commande pour un seul concert, pas seulement par ligne.
- Un panier actif et une commande sont limites a un seul concert.
- Le stock restant ne peut pas devenir negatif.
- Un paiement accepte cree une commande `paid`, cree un paiement `accepted`, snapshot les prix et decremente le stock.
- Un paiement refuse cree une commande `refused`, cree un paiement `refused`, ne decremente pas le stock et laisse le panier actif.

## Donnees demo

La commande `python manage.py seed_demo_data` cree ou met a jour :

- un concert futur ouvert ;
- un concert futur annule ;
- un concert passe/termine ;
- plusieurs categories de places avec prix et stocks differents.

## Qualite et CI

Le workflow CI existant reste configure pour :

- installer les dependances de developpement ;
- installer Chromium pour Playwright ;
- executer Ruff ;
- executer `python manage.py check` ;
- executer pytest avec generation `coverage.xml` ;
- sauter les tests e2e tant que le dossier `e2e/` n'existe pas ;
- lancer SonarCloud seulement si le secret `SONAR_TOKEN` est disponible.

Etat distant observe :

- la branche `feature/core-domain-model` a ete poussee sur `origin` ;
- la draft pull request #3 a ete creee vers `main` ;
- `gh pr checks` a ete utilise pour surveiller les checks distants ;
- les deux jobs GitHub Actions `Django checks` ont reussi ;
- le check externe `SonarCloud Code Analysis` a reussi.

## Verification locale

Commandes lancees avec succes :

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate --plan
ruff check .
pytest
pytest --cov=. --cov-report=term-missing --cov-report=xml
```

Resultats observes :

- `python manage.py check` : OK.
- `python manage.py makemigrations --check --dry-run` : OK, aucune migration manquante.
- `python manage.py migrate --plan` : OK, plan de migrations affiche.
- `ruff check .` : OK.
- `pytest` : OK, 47 tests passent.
- `pytest --cov=. --cov-report=term-missing --cov-report=xml` : OK, 47 tests passent, couverture totale 99 %, `cart/models.py`, `cart/services.py`, `concerts/models.py`, `orders/models.py` et `payments/models.py` a 100 %, `coverage.xml` genere puis ignore par Git.

Decision couverture : les lignes restantes non couvertes dans `payments/services.py` correspondent a des incoherences defensives apres validation ou a une course concurrente de stock difficile a declencher sans monkeypatch interne artificiel. Elles ne sont pas couvertes dans cette passe.

Aucun controle navigateur manuel n'a ete execute dans cette etape, car aucune interface panier, paiement ou historique n'a ete ajoutee.

## Statut Git observe

- Branche de travail : `feature/domain-coverage-followup`.
- Remote Git : `https://github.com/Axel-al/billeterie-concerts.git`.
- `AGENTS.md` est present localement et ignore via `.git/info/exclude`.
- `docs/prompts/` n'a pas ete lu.
- `db.sqlite3`, `coverage.xml`, caches Python/Ruff/pytest et environnements virtuels restent non versionnes.

## Prochaine etape recommandee

Ajouter les vues de consultation des concerts (`EF1`, `EF2`) ou le parcours panier/paiement UI (`EF5`, `EF7`, `EF8`, `EF9`) en reutilisant les services domaine existants.
