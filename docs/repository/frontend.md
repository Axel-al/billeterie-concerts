# Frontend

## Etat actuel

Le frontend applicatif minimal est initialise avec Django templates.

- `templates/base.html` fournit le layout HTML, la navigation minimale et Bootstrap via CDN.
- `templates/pages/home.html` fournit une page d'accueil francaise minimale.
- `templates/accounts/signup.html` fournit le formulaire d'inscription en francais.
- `templates/accounts/login.html` fournit le formulaire de connexion en francais.
- `templates/accounts/personal_area.html` fournit la page protegee `Mon espace`.
- La route `/` affiche cette page via `TemplateView`.
- La navigation affiche `Inscription` et `Connexion` aux visiteurs, puis `Mon espace` et un bouton POST `Deconnexion` aux utilisateurs connectes.

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

## Ecrans cibles

- Liste des concerts ouverts a la vente.
- Detail d'un concert avec categories, prix et stock restant.
- Creation de compte et connexion.
- Espace personnel protege.
- Panier.
- Paiement simule.
- Confirmation ou refus de paiement.
- Historique des commandes.
- Administration des concerts et ventes.

## Non couvert dans cette etape

La page d'accueil ne constitue pas une implementation de la liste des concerts, du panier ou du paiement. Aucune couverture frontend `EF1`, `EF2`, `EF5` a `EF12` ou `ENF1` n'est revendiquee, hors couvertures domaine/service deja documentees pour le panier, le paiement et le stock.

`Mon espace` est une page de compte de base. Elle ne constitue pas encore l'historique de commandes attendu par `EF10` et ne revendique pas `RG8`.

## Contraintes

Aucune application frontend separee n'est prevue. Tout changement de direction devra etre justifie dans `docs/repository/decisions.md`.
