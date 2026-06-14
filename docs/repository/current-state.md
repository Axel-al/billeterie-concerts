# Etat courant du depot

Derniere mise a jour : 2026-06-14

## Synthese

Le depot contient une application Django executable avec :

- un modele utilisateur personnalise base sur l'email ;
- des pages francaises d'inscription, connexion, deconnexion et espace personnel ;
- un noyau domaine teste pour la billetterie de concerts ;
- une documentation de validation et de tracabilite mise a jour.

Elements livres dans cette etape :

- routes `/inscription/`, `/connexion/`, `/deconnexion/` et `/mon-espace/` ;
- formulaire d'inscription avec email unique, mot de passe Django et rejet explicite des doublons ;
- formulaire de connexion en francais et deconnexion par requete POST ;
- navigation differenciee entre visiteurs et utilisateurs connectes ;
- page protegee `Mon espace` ;
- tests d'integration Django pour labels francais, inscription, connexion, echec de connexion, deconnexion POST, protection d'acces et role utilisateur standard ;
- mise a jour des documents `docs/repository/` et `docs/validation/`.

Le cahier des charges officiel reste conserve dans `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Exigences couvertes dans cette etape

Couverture revendiquee pour le perimetre comptes :

- `EF3` : creation de compte avec email unique et mot de passe ;
- `EF4` : connexion, deconnexion et acces a un espace personnel protege ;
- `EM8` : deux comptes ne peuvent pas partager le meme email ;
- `ENF3` : mots de passe geres par le hachage Django ;
- `ENF4` : rejet propre des emails deja utilises et des identifiants invalides.

Couverture existante conservee :

- `EF5` : couverture partielle domaine/service pour l'ajout de billets au panier, sans formulaire ni UI ;
- `EF6` : couverture partielle domaine pour le total de panier, sans affichage ;
- `EF7` : couverture partielle domaine/service pour le paiement simule, sans page paiement ;
- `EF8` : couverture partielle domaine/service pour la commande payee, sans confirmation affichee ;
- `EF9` : couverture partielle domaine/service pour la commande refusee et le stock inchange, sans message explicite affiche ;
- `EF12` : stock decremente apres paiement accepte au niveau service ;
- `EM1` a `EM7` et `EM10` : regles couvertes au niveau domaine/service ;
- `RG1` a `RG5` : regles couvertes au niveau domaine/service ;
- `RG7` : couverture partielle domaine par refus des concerts annules ;
- `ENF5`, `ENF6` et `ENF7` : Ruff, tests automatises, coverage et GitHub Actions versionnes.

Non couvert volontairement :

- `EF1`, `EF2`, `EF10` ;
- pages panier, paiement, confirmation et refus de paiement ;
- confirmation affichee de `EF8` et message explicite affiche de `EF9` ;
- `RG6` et `RG8` ;
- couverture fonctionnelle complete de `EF11` ;
- `EM9`, qui reste une fondation de role seulement via `is_staff` / `is_superuser`.

## Structure applicative

- `config/` : settings, URLs racines, redirections d'authentification, ASGI et WSGI.
- `accounts/` : modele utilisateur personnalise, manager, admin Django, formulaires, vues et URLs d'authentification.
- `concerts/` : concerts, categories de places, statuts, stock, admin et commande `seed_demo_data`.
- `cart/` : panier actif mono-concert, lignes de panier et services de validation/ajout.
- `orders/` : commandes, lignes de commandes et prix snapshots.
- `payments/` : paiement simule et service transactionnel.
- `templates/` : layout, page d'accueil et templates de comptes.
- `tests/` : tests de smoke homepage, settings, utilisateur, authentification et domaine billetterie.

## Comportement authentification

- Un visiteur peut creer un compte avec email, nom, prenom et mot de passe.
- Une inscription reussie connecte automatiquement l'utilisateur et redirige vers `Mon espace`.
- Un email deja utilise est refuse avec le message `Un compte existe déjà avec cette adresse email.`
- Un utilisateur peut se connecter avec son email et son mot de passe.
- Une erreur de connexion affiche un message francais explicite.
- La deconnexion utilise un formulaire POST dans la navigation.
- `Mon espace` exige une session authentifiee et redirige les visiteurs vers `/connexion/?next=/mon-espace/`.
- Un utilisateur standard cree par le parcours public n'a pas les droits `is_staff` ni `is_superuser`.

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

La configuration SonarCloud analyse tous les modules applicatifs existants :
`config`, `accounts`, `concerts`, `cart`, `orders` et `payments`. Les tests restent
declares separement dans `tests`.

Etat distant observe :

- la branche `feature/user-authentication` a ete poussee sur `origin` ;
- la draft pull request #5 a ete creee vers `main` ;
- `gh pr checks 5 --watch` et `gh checks HEAD` ont ete utilises pour surveiller les checks distants ;
- les deux jobs GitHub Actions `Django checks` ont reussi ;
- le check externe `SonarCloud Code Analysis` a reussi.

## Verification locale

Commandes lancees avec succes :

```bash
ruff check .
pytest
python manage.py check
python manage.py makemigrations --check --dry-run
pytest --cov=. --cov-report=xml
coverage report
```

Resultats observes :

- `ruff check .` : OK.
- `pytest` : OK, 58 tests passent.
- `python manage.py check` : OK.
- `python manage.py makemigrations --check --dry-run` : OK, aucune migration manquante.
- `pytest --cov=. --cov-report=xml` : OK, 58 tests passent et `coverage.xml` est genere puis ignore par Git.
- `coverage report` : couverture totale 99 %, avec `accounts/forms.py`, `accounts/urls.py` et `accounts/views.py` a 100 %.

Decision couverture : les lignes restantes non couvertes dans `payments/services.py` correspondent a des incoherences defensives apres validation ou a une course concurrente de stock difficile a declencher sans monkeypatch interne artificiel. Elles ne sont pas couvertes dans cette passe.

Aucun controle navigateur manuel n'a ete execute dans cette etape, car les parcours comptes ajoutes sont couverts par des tests d'integration Django automatises.

### Verification locale de la configuration SonarCloud

Commandes lancees le 2026-06-14 :

```bash
python manage.py check
ruff check .
pytest --cov=. --cov-report=xml
git diff --check
```

Resultats observes :

- `python manage.py check` : OK, aucun probleme detecte.
- `ruff check .` : OK, tous les controles passent.
- `pytest --cov=. --cov-report=xml` : OK, 58 tests passent en 8,34 secondes et
  `coverage.xml` est genere.
- `git diff --check` : OK, aucune erreur d'espacement detectee.

## Statut Git observe

- Branche de travail : `fix/sonar-source-directories`.
- Remote Git : `https://github.com/Axel-al/billeterie-concerts.git`.
- `AGENTS.md` est present localement et ignore via `.git/info/exclude`.
- `docs/prompts/` n'a pas ete lu.
- `db.sqlite3`, `coverage.xml`, caches Python/Ruff/pytest et environnements virtuels restent non versionnes.

## Prochaine etape recommandee

Ajouter les vues de consultation des concerts (`EF1`, `EF2`) ou le parcours panier/paiement UI (`EF5`, `EF7`, `EF8`, `EF9`) en reutilisant les services domaine existants.
