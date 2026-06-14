# Etat courant du depot

Derniere mise a jour : 2026-06-14

## Synthese

Le depot contient une application Django executable avec :

- un modele utilisateur personnalise base sur l'email ;
- des pages francaises d'inscription, connexion, deconnexion et espace personnel ;
- un catalogue public de concerts et des fiches detaillees ;
- un noyau domaine teste pour la billetterie de concerts ;
- une documentation de validation et de tracabilite mise a jour.

Elements livres dans cette etape :

- routes `/concerts/` et `/concerts/<id>/` ;
- catalogue limite aux concerts ouverts, futurs et possedant du stock ;
- fiches avec titre, artiste, date, lieu, description, categories, prix et stock restant ;
- explications francaises pour les concerts annules, passes, complets ou fermes a la vente ;
- lien de connexion avec retour vers la fiche pour les visiteurs d'un concert reservable ;
- navigation et accueil orientes vers la consultation des concerts ;
- tests d'integration Django pour le filtrage, les affichages, les CTA, les motifs d'indisponibilite et les reponses HTTP ;
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

Couverture revendiquee pour le catalogue :

- `EF1` : liste des concerts ouverts, futurs et avec stock ;
- `EF2` : fiche detaillee avec informations, categories, prix et stock restant ;
- `EM4`, `EM5` et `RG1` : etats non reservables appliques dans les vues ;
- `RG7` : annulation visible sans nouvelle action de reservation, hors action admin ;
- `ENF1` : couverture partielle par la navigation accueil, catalogue et fiche.

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

Non couvert volontairement dans ce lot :

- `EF10` ;
- pages panier, paiement, confirmation et refus de paiement ;
- formulaire categorie/quantite, endpoint panier et ajout de billet dans les vues ;
- confirmation affichee de `EF8` et message explicite affiche de `EF9` ;
- `RG6` et `RG8` ;
- couverture fonctionnelle complete de `EF11` ;
- `EM9`, qui reste une fondation de role seulement via `is_staff` / `is_superuser`.

## Structure applicative

- `config/` : settings, URLs racines, redirections d'authentification, ASGI et WSGI.
- `accounts/` : modele utilisateur personnalise, manager, admin Django, formulaires, vues et URLs d'authentification.
- `concerts/` : concerts, categories de places, statuts, stock, vues publiques, admin et commande `seed_demo_data`.
- `cart/` : panier actif mono-concert, lignes de panier et services de validation/ajout.
- `orders/` : commandes, lignes de commandes et prix snapshots.
- `payments/` : paiement simule et service transactionnel.
- `templates/` : layout, accueil, catalogue, fiches concerts et templates de comptes.
- `tests/` : tests de smoke homepage, settings, utilisateur, authentification, vues concerts et domaine billetterie.

## Comportement catalogue

- Le catalogue public n'affiche que les concerts strictement futurs, `open` et avec au moins une categorie en stock.
- Les fiches annulees, passees, terminees ou completes restent consultables avec un motif explicite et sans CTA de reservation.
- Les fiches brouillon et les identifiants inconnus renvoient `404`.
- Toutes les categories sont affichees sur la fiche, y compris les categories epuisees.
- Un visiteur voit `Se connecter pour reserver` seulement pour un concert reservable ; le parametre `next` conserve l'URL de la fiche.
- Un utilisateur connecte ne voit aucun bouton sans destination. Aucun ajout panier n'est implemente ou revendique au titre de `EF5`.

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

La verification distante de la branche du catalogue est effectuee apres le push et documentee plus bas.

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
- `pytest` : OK, 69 tests passent.
- `python manage.py check` : OK.
- `python manage.py makemigrations --check --dry-run` : OK, aucune migration manquante.
- `pytest --cov=. --cov-report=xml` : OK, 69 tests passent et `coverage.xml` est genere puis ignore par Git.
- `coverage report` : couverture totale 99 %, avec `concerts/views.py`, `concerts/urls.py` et `tests/test_concert_views.py` a 100 %.
- `git diff --check` : OK.

Decision couverture : les lignes restantes non couvertes dans `payments/services.py` correspondent a des incoherences defensives apres validation ou a une course concurrente de stock difficile a declencher sans monkeypatch interne artificiel. Elles ne sont pas couvertes dans cette passe.

## Verification navigateur

Controle manuel execute avec `agent-browser` et les donnees de `seed_demo_data` :

- l'accueil expose `Concerts` et `Voir les concerts` ;
- le catalogue n'affiche que `Nuit Electrique`, seul concert demo reservable ;
- la fiche reservable affiche date, lieu, trois categories, prix, stocks et le lien de connexion avec `next=/concerts/1/` ;
- les fiches `Silence Annule` et `Hier Encore` affichent leur motif francais et aucun CTA de reservation ;
- une fiche de controle future avec stock nul affiche `Ce concert est complet. Il ne reste aucune place disponible.` et aucun CTA.

## Statut Git observe

- Branche de travail : `feature/public-concert-catalog`.
- Remote Git : `https://github.com/Axel-al/billeterie-concerts.git`.
- `AGENTS.md` est present localement et ignore via `.git/info/exclude`.
- `docs/prompts/` n'a pas ete lu.
- `db.sqlite3`, `coverage.xml`, caches Python/Ruff/pytest et environnements virtuels restent non versionnes.

## Prochaine etape recommandee

Ajouter le parcours panier/paiement UI (`EF5`, `EF7`, `EF8`, `EF9`) en reutilisant les services domaine existants.
