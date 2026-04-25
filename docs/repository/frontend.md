# Frontend

## Etat actuel

Aucun frontend applicatif n'est present. Il n'existe pas encore de templates Django, de vues, de fichiers CSS ou de JavaScript versionnes.

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
- Panier.
- Paiement simule.
- Confirmation ou refus de paiement.
- Historique des commandes.
- Administration des concerts et ventes.

## Contraintes

Aucune application frontend separee n'est prevue. Tout changement de direction devra etre justifie dans `docs/repository/decisions.md`.
