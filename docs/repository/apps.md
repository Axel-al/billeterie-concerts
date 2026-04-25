# Applications Django

## Etat actuel

Trois applications Django sont initialisees :

| Application | Etat actuel | Exigences liees |
| --- | --- | --- |
| `accounts` | Modele `User` personnalise avec email unique, manager et admin Django. | EF3 partiel, EM8, ENF3 |
| `concerts` | Application creee, sans modele ni vue metier. | Non couvert dans cette etape |
| `orders` | Application creee, sans modele ni vue metier. | Non couvert dans cette etape |

Le module `config` porte les reglages, les URLs racines et le rendu de la page d'accueil.

## Decoupage cible

| Application | Responsabilite | Exigences principales |
| --- | --- | --- |
| `concerts` | Concerts, lieux, categories de places, statut et stock affiche. | EF1, EF2, EF11, EF12, EM1, EM4, EM5, EM9, RG1, RG2, RG7 |
| `accounts` | Creation de compte, connexion, deconnexion, espace personnel et roles. | EF3, EF4, EM8, ENF3, RG6 |
| `cart` | Panier, lignes de panier, quantites et total. | EF5, EF6, EM2, EM3, RG2, RG3 |
| `orders` | Commandes, billets achetes, historique et statuts. | EF8, EF9, EF10, EM6, EM10, RG4, RG5, RG8 |
| `payments` | Paiement simule et resultat de paiement. | EF7, EF8, EF9, EM6, RG4, RG5 |

## Decisions appliquees

- `cart` et `payments` ne sont pas crees dans cette etape, car la demande porte seulement sur la fondation technique.
- Le role administrateur repose pour l'instant sur les champs Django `is_staff` et `is_superuser`.
- Toute reduction ou extension du decoupage cible devra etre documentee dans `docs/repository/decisions.md`.

## Non fait dans cette etape

- Pas de liste ou detail de concerts.
- Pas de panier, paiement, historique de commandes ou regle de stock.
- Pas de formulaire d'inscription ou connexion utilisateur.
