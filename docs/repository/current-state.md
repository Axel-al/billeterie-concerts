# Etat courant du depot

Derniere mise a jour : 2026-06-15

## Synthese

Le depot contient une application Django executable avec :

- un modele utilisateur personnalise base sur l'email ;
- des pages francaises d'inscription, connexion, deconnexion et espace personnel ;
- un catalogue public de concerts et des fiches detaillees ;
- un parcours panier, checkout, paiement simule, confirmation et refus ;
- un historique des commandes payees et un detail de commande filtres par utilisateur ;
- des vues d'administration protegees par permissions pour le suivi des ventes, l'annulation et la cloture des ventes ;
- un noyau domaine teste pour la billetterie de concerts ;
- une documentation de validation et de tracabilite mise a jour.

Elements livres dans cette etape :

- routes `/concerts/` et `/concerts/<id>/` ;
- catalogue limite aux concerts ouverts, futurs et possedant du stock ;
- fiches avec titre, artiste, date, lieu, description, categories, prix et stock restant ;
- explications francaises pour les concerts annules, passes, complets ou fermes a la vente ;
- lien de connexion avec retour vers la fiche pour les visiteurs d'un concert reservable ;
- formulaire categorie/quantite sur les fiches reservables pour les utilisateurs connectes ;
- route `/panier/` avec lignes, sous-totaux et total ;
- route `/panier/validation/` protegee par authentification et limitee au panier actif de l'utilisateur ;
- route `/paiement/` avec paiement simule ;
- carte `4242424242424242` acceptee et toute autre carte refusee, sans stockage du numero ;
- creation d'une commande `paid`, prix snapshots et decrement du stock apres paiement accepte ;
- creation d'une commande `refused` non finale et stock inchange apres paiement refuse ;
- pages de confirmation et refus filtrees par utilisateur connecte ;
- routes `/commandes/` et `/commandes/<id>/` protegees par authentification ;
- historique `Mes commandes` limite aux commandes payees du client connecte ;
- detail de commande affichant date, statut, total, concert, categorie, quantite et prix paye ;
- commandes refusees exclues de l'historique des achats payes ;
- navigation post-paiement vers le detail de commande et l'historique ;
- statut de concert `closed` pour les ventes cloturees ;
- route `/concerts/administration/ventes/` protegee par `concerts.view_concert` et `orders.view_order` ;
- actions POST d'administration pour annuler un concert ou cloturer ses ventes, protegees par `concerts.change_concert` ;
- synthese des ventes par concert limitee aux commandes payees : commandes, billets vendus, chiffre d'affaires, stock initial et stock restant ;
- lien de navigation `Administration ventes` visible seulement pour les utilisateurs ayant les permissions de consultation requises ;
- admin Django enrichi pour les concerts et categories, avec indicateurs de stock/ventes et actions d'annulation/cloture ;
- commandes et paiements consultables en admin comme surfaces de lecture plutot que de modification metier ;
- navigation et accueil orientes vers la consultation des concerts ;
- tests d'integration Django pour le filtrage, les affichages, les CTA, les motifs d'indisponibilite, les reponses HTTP, le parcours panier/paiement et l'historique de commandes ;
- tests d'integration Django pour les permissions d'administration, l'annulation, la cloture, le suivi des ventes et la creation/modification admin de concerts avec categories ;
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

Couverture revendiquee pour l'administration :

- `EF11` : creation, modification, annulation et cloture de concerts via administration ;
- `EM9` : les vues d'administration exigent les permissions Django adaptees ;
- `RG7` : l'annulation admin rend le concert non reservable.

Couverture existante conservee :

- `EF5` : ajout de billets au panier depuis une fiche concert reservable pour un utilisateur connecte ;
- `EF6` : total du panier affiche et calcule a partir des lignes ;
- `EF7` : validation du panier par paiement simule ;
- `EF8` : paiement accepte, commande payee et confirmation affichee ;
- `EF9` : paiement refuse, aucune commande validee et message explicite ;
- `EF12` : stock decremente apres paiement accepte ;
- `EM1` a `EM7` et `EM10` : regles couvertes au niveau domaine/service et parcours UI ;
- `RG1` a `RG6` : regles couvertes au niveau domaine/service et parcours UI ;
- `EF10` et `RG8` : historique des commandes payees et detail de commande filtres par proprietaire ;
- `ENF5`, `ENF6` et `ENF7` : Ruff, tests automatises, coverage et GitHub Actions versionnes.

Traceabilite de cette etape :

- `EF10` et `RG8` sont couverts par le nouvel historique paye et les pages detail filtrees par proprietaire.
- `EF11`, `EM9` et `RG7` sont couverts par les vues d'administration, les actions de statut et les tests de permissions.
- `EF8`, `EF9`, `EM6`, `EM7`, `EM10`, `RG4` et `RG5` sont maintenus ou etendus par les tests de navigation et d'affichage, mais leur comportement coeur etait deja implemente par le parcours checkout/paiement.

Non couvert volontairement dans ce lot :

- `RG8` ne couvre pas le suivi de ventes administrateur : il reste limite au cloisonnement des commandes des utilisateurs standards.

## Structure applicative

- `config/` : settings, URLs racines, redirections d'authentification, ASGI et WSGI.
- `accounts/` : modele utilisateur personnalise, manager, admin Django, formulaires, vues et URLs d'authentification.
- `concerts/` : concerts, categories de places, statuts, stock, vues publiques, vues d'administration, services de gestion, admin Django et commande `seed_demo_data`.
- `cart/` : panier actif mono-concert, lignes de panier, services de validation/ajout, vues panier et checkout.
- `orders/` : commandes, lignes de commandes et prix snapshots.
- `payments/` : paiement simule, regle de carte, service transactionnel et vues paiement/resultat.
- `templates/` : layout, accueil, catalogue, fiches concerts, comptes, panier, paiement, commandes et synthese admin des ventes.
- `tests/` : tests de smoke homepage, settings, utilisateur, authentification, vues concerts, domaine billetterie, parcours panier/paiement, historique de commandes et administration concerts/ventes.

## Comportement catalogue

- Le catalogue public n'affiche que les concerts strictement futurs, `open` et avec au moins une categorie en stock.
- Les fiches annulees, cloturees, passees, terminees ou completes restent consultables avec un motif explicite et sans CTA de reservation.
- Les fiches brouillon et les identifiants inconnus renvoient `404`.
- Toutes les categories sont affichees sur la fiche, y compris les categories epuisees.
- Un visiteur voit `Se connecter pour reserver` seulement pour un concert reservable ; le parametre `next` conserve l'URL de la fiche.
- Un utilisateur connecte voit un formulaire d'ajout au panier sur les fiches reservables.

## Comportement panier et paiement

- Un utilisateur connecte peut ajouter une categorie et une quantite de billets depuis la fiche d'un concert reservable.
- La quantite est rejetee si elle n'est pas comprise entre 1 et 6.
- Les concerts passes, annules, fermes a la vente ou sans stock ne peuvent pas etre ajoutes au panier.
- Le panier actif affiche les lignes, les sous-totaux et le total.
- Le checkout et le paiement exigent une session authentifiee et utilisent uniquement le panier actif de l'utilisateur courant.
- Le paiement simule accepte la carte `4242424242424242` et refuse toute autre valeur.
- En cas de paiement accepte, une commande `paid` est creee, les prix de lignes sont figes, le stock est decremente et le panier passe a `checked_out`.
- En cas de paiement refuse, une commande `refused` non finale est creee, le stock ne change pas et le panier reste actif.
- Les pages de confirmation et de refus ne sont accessibles qu'au proprietaire de la commande.
- La confirmation de paiement propose un acces au detail de commande et a `Mes commandes`.

## Comportement commandes

- `Mes commandes` exige une session authentifiee et redirige les visiteurs vers `/connexion/?next=/commandes/`.
- L'historique affiche uniquement les commandes `paid` du client connecte.
- Le detail `/commandes/<id>/` exige une session authentifiee, filtre par proprietaire et par statut `paid`, et renvoie `404` pour la commande payee d'un autre utilisateur ou une commande refusee.
- Le detail affiche la date, le statut, le montant total, le concert, la categorie achetee, la quantite, le prix paye et le total de ligne.
- Les commandes refusees restent tracees comme non finales, ne decrementent pas le stock et sont exclues de l'historique des achats payes.

## Comportement administration

- Le statut `closed` represente une vente cloturee manuellement par l'administration.
- La synthese `/concerts/administration/ventes/` exige `concerts.view_concert` et `orders.view_order`.
- Les actions POST d'annulation et de cloture exigent `concerts.change_concert`.
- Un visiteur anonyme est redirige vers `/connexion/` avec le parametre `next`.
- Un utilisateur authentifie sans permission recoit une reponse `403`.
- Un utilisateur ayant les permissions requises peut consulter les ventes et changer le statut d'un concert.
- L'annulation admin met le concert en `cancelled` et bloque toute nouvelle reservation.
- La cloture admin met le concert en `closed` et bloque toute nouvelle reservation.
- L'annulation ou la cloture ne modifie pas le stock restant et ne supprime pas les commandes payees existantes.
- La synthese des ventes compte uniquement les commandes `paid`; les commandes `refused` restent hors chiffre d'affaires et hors billets vendus.

## Comportement authentification

- Un visiteur peut creer un compte avec email, nom, prenom et mot de passe.
- Une inscription reussie connecte automatiquement l'utilisateur et redirige vers `Mon espace`.
- Un email deja utilise est refuse avec le message `Un compte existe déjà avec cette adresse email.`
- Un utilisateur peut se connecter avec son email et son mot de passe.
- Une erreur de connexion affiche un message francais explicite.
- La deconnexion utilise un formulaire POST dans la navigation.
- `Mon espace` exige une session authentifiee et redirige les visiteurs vers `/connexion/?next=/mon-espace/`.
- `Mon espace` et la navigation authentifiee donnent acces a `Mes commandes`.
- Un utilisateur standard cree par le parcours public n'a pas les droits `is_staff` ni `is_superuser`.

## Regles domaine implementees

- Un concert est reservable seulement s'il est strictement futur, `open` et avec au moins une categorie en stock.
- Les concerts passes, annules ou clotures ne sont pas reservables.
- Une quantite doit etre un entier entre 1 et 6.
- Le plafond de 6 billets est applique au total du panier/commande pour un seul concert, pas seulement par ligne.
- Un panier actif et une commande sont limites a un seul concert.
- Le stock restant ne peut pas devenir negatif.
- Un paiement accepte cree une commande `paid`, cree un paiement `accepted`, snapshot les prix et decremente le stock.
- Un paiement refuse cree une commande `refused`, cree un paiement `refused`, ne decremente pas le stock et laisse le panier actif.
- Un utilisateur ne peut consulter que ses propres commandes payees dans l'historique et le detail de commande.

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

Etat distant de la branche courante :

- le compte GitHub actif dispose de droits d'ecriture sur `Axel-al/billeterie-concerts` ;
- la branche `feature/admin-concert-management` est poussee directement sur le depot amont ;
- la pull request #12 `Implement admin concert management` est ouverte vers `main` ;
- le workflow distant `CI` declenche par push a reussi ;
- `gh checks HEAD` signale `Django checks` et `SonarCloud Code Analysis` en succes.

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

Resultats observes pour la derniere implementation complete :

- `ruff check .` : OK.
- `pytest` : OK, 105 tests passent.
- `python manage.py check` : OK.
- `python manage.py makemigrations --check --dry-run` : OK, aucune migration manquante.
- `pytest --cov=. --cov-report=xml` : OK, 105 tests passent et `coverage.xml` est genere puis ignore par Git.
- `coverage report` : couverture totale 99 %, avec `cart/services.py`, `cart/views.py`, `concerts/admin.py`, `concerts/services.py`, `concerts/views.py`, `orders/admin.py`, `orders/views.py`, `payments/admin.py`, `payments/views.py`, `tests/test_admin_concert_management.py`, `tests/test_booking_flow.py` et `tests/test_order_history.py` a 100 %.
- `git diff --check` : OK.

Decision couverture : les lignes restantes non couvertes concernent uniquement des incoherences defensives dans `payments/services.py` : categorie de panier incoherente apres validation, stock devenu insuffisant entre validation et snapshot, ou echec concurrent de l'update conditionnel. Les couvrir demanderait des donnees volontairement incoherentes ou du monkeypatch interne, donc elles ne sont pas ajoutees a cette passe. Les regles critiques demandees et les branches significatives des vues panier/paiement/commandes/administration sont couvertes par `tests/test_core_domain.py`, `tests/test_booking_flow.py`, `tests/test_order_history.py` et `tests/test_admin_concert_management.py`.

## Verification navigateur

Aucun nouveau controle navigateur manuel n'a ete execute pour l'administration concerts/ventes dans cette passe ; la verification repose sur les tests d'integration Django.

Controle manuel execute avec `agent-browser` et les donnees de `seed_demo_data` :

- l'accueil expose `Concerts` et `Voir les concerts` ;
- le catalogue n'affiche que `Nuit Electrique`, seul concert demo reservable ;
- la fiche reservable affiche date, lieu, trois categories, prix, stocks et le lien de connexion avec `next=/concerts/1/` ;
- les fiches `Silence Annule` et `Hier Encore` affichent leur motif francais et aucun CTA de reservation ;
- une fiche de controle future avec stock nul affiche `Ce concert est complet. Il ne reste aucune place disponible.` et aucun CTA.

## Statut Git observe

- Branche de travail : `feature/admin-concert-management`.
- Remote de suivi et de push : `https://github.com/Axel-al/billeterie-concerts.git`.
- Pull request : `https://github.com/Axel-al/billeterie-concerts/pull/12`.
- `AGENTS.md` est present localement et ignore via `.git/info/exclude`.
- `docs/prompts/` n'a pas ete lu.
- `db.sqlite3`, `coverage.xml`, caches Python/Ruff/pytest et environnements virtuels restent non versionnes.

## Prochaine etape recommandee

Ajouter un premier scenario Playwright couvrant consultation, panier, paiement accepte et historique de commandes.
