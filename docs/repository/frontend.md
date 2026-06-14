# Frontend

## Etat actuel

Le frontend applicatif minimal est initialise avec Django templates.

- `templates/base.html` fournit le layout HTML, la navigation minimale et Bootstrap via CDN.
- `templates/pages/home.html` fournit une page d'accueil francaise avec un acces direct au catalogue.
- `templates/concerts/concert_list.html` affiche les concerts ouverts, futurs et disponibles.
- `templates/concerts/concert_detail.html` affiche les informations du concert, les categories, prix, stocks et l'etat de reservation.
- `templates/accounts/signup.html` fournit le formulaire d'inscription en francais.
- `templates/accounts/login.html` fournit le formulaire de connexion en francais.
- `templates/accounts/personal_area.html` fournit la page protegee `Mon espace`.
- La route `/` affiche la page d'accueil via `TemplateView`.
- Les routes `/concerts/` et `/concerts/<id>/` fournissent le catalogue et les fiches publiques.
- La navigation fournit un lien `Concerts`, puis affiche `Inscription` et `Connexion` aux visiteurs ou `Mon espace` et un bouton POST `Deconnexion` aux utilisateurs connectes.

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

## Ecrans cibles restants

- Panier.
- Paiement simule.
- Confirmation ou refus de paiement.
- Historique des commandes.
- Administration des concerts et ventes.

## Non couvert dans cette etape

Le catalogue et les fiches couvrent `EF1` et `EF2`. La navigation directe depuis l'accueil et entre liste et detail apporte une couverture partielle de `ENF1`.

Le lien `Se connecter pour reserver` est affiche seulement au visiteur lorsqu'un concert est reservable et conserve la fiche dans le parametre `next`. Il ne constitue pas une implementation de `EF5` : aucun formulaire de categorie ou quantite, endpoint panier ou ajout de billet n'est expose.

Les concerts non reservables affichent un motif explicite en francais et aucune action de reservation. Les brouillons ne sont pas accessibles publiquement.

`Mon espace` est une page de compte de base. Elle ne constitue pas encore l'historique de commandes attendu par `EF10` et ne revendique pas `RG8`.

## Contraintes

Aucune application frontend separee n'est prevue. Tout changement de direction devra etre justifie dans `docs/repository/decisions.md`.
