# Frontend

## Etat actuel

Le frontend applicatif minimal est initialise avec Django templates.

- `templates/base.html` fournit le layout HTML, la navigation minimale et Bootstrap via CDN.
- `templates/pages/home.html` fournit une page d'accueil francaise avec un acces direct au catalogue.
- `templates/concerts/concert_list.html` affiche les concerts ouverts, futurs et disponibles.
- `templates/concerts/concert_detail.html` affiche les informations du concert, les categories, prix, stocks, l'etat de reservation et le formulaire d'ajout au panier pour les utilisateurs connectes.
- `templates/cart/detail.html` affiche le panier actif, les lignes, les sous-totaux et le total.
- `templates/cart/checkout.html` affiche le recapitulatif de validation avant paiement.
- `templates/payments/payment_form.html` affiche le formulaire de paiement simule.
- `templates/payments/confirmation.html` affiche une commande payee avec les prix snapshots.
- `templates/payments/refused.html` affiche le refus explicite et permet de retenter le paiement.
- `templates/orders/list.html` affiche l'historique des commandes payees du client connecte.
- `templates/orders/detail.html` affiche le detail d'une commande payee du client connecte avec les prix snapshots.
- `templates/accounts/signup.html` fournit le formulaire d'inscription en francais.
- `templates/accounts/login.html` fournit le formulaire de connexion en francais.
- `templates/accounts/personal_area.html` fournit la page protegee `Mon espace` avec un acces a `Mes commandes`.
- La route `/` affiche la page d'accueil via `TemplateView`.
- Les routes `/concerts/` et `/concerts/<id>/` fournissent le catalogue et les fiches publiques.
- La navigation fournit un lien `Concerts`, puis affiche `Inscription` et `Connexion` aux visiteurs ou `Panier`, `Mes commandes`, `Mon espace` et un bouton POST `Deconnexion` aux utilisateurs connectes.

## Direction cible

Le frontend cible repose sur :

- Django templates ;
- Bootstrap via CDN ;
- HTML semantique ;
- JavaScript leger seulement lorsque cela ameliore clairement l'ergonomie ;
- eventuellement HTMX via CDN pour des interactions simples, si justifie.

## Principes d'interface

- Rendre visibles les actions principales : consulter un concert, ajouter au panier, payer.
- Afficher clairement les erreurs de saisie, de stock, d'authentification et de paiement.
- Eviter une navigation excessive pour les parcours principaux.
- Garder les pages lisibles sur mobile et desktop.
- Afficher les prix, quantites, stocks et statuts de facon explicite avant validation.

## Ecrans disponibles

- Liste des concerts ouverts a la vente.
- Detail d'un concert avec categories, prix et stock restant.
- Creation de compte et connexion.
- Espace personnel protege.
- Historique des commandes.

## Ecrans cibles restants

- Administration des concerts et ventes.

## Non couvert dans cette etape

Le catalogue et les fiches couvrent `EF1` et `EF2`. La navigation directe depuis l'accueil et entre liste et detail apporte une couverture partielle de `ENF1`.

Le lien `Se connecter pour reserver` est affiche seulement au visiteur lorsqu'un concert est reservable et conserve la fiche dans le parametre `next`. Pour un utilisateur connecte, la fiche reservable expose le formulaire categorie/quantite permettant d'ajouter au panier.

Les concerts non reservables affichent un motif explicite en francais et aucune action de reservation. Les brouillons ne sont pas accessibles publiquement.

Le parcours panier/paiement couvre maintenant l'ajout au panier, le total, le checkout, la confirmation et le refus explicite. Les pages de resultat de paiement sont filtrees par utilisateur connecte.

`EF10` et `RG8` sont couverts par les pages `Mes commandes` et detail de commande, limitees aux commandes payees du client connecte. Les commandes refusees restent tracees comme non finales et sont exclues de l'historique des achats payes.

## Contraintes

Aucune application frontend separee n'est prevue. Tout changement de direction devra etre justifie dans `docs/repository/decisions.md`.
