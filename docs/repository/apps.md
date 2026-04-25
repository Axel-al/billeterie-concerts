# Applications Django prevues

## Etat actuel

Aucune application Django n'existe encore dans le depot. Cette page decrit le decoupage cible a valider lors de l'initialisation du projet.

## Decoupage cible

| Application | Responsabilite | Exigences principales |
| --- | --- | --- |
| `concerts` | Concerts, lieux, categories de places, statut et stock affiche. | EF1, EF2, EF11, EF12, EM1, EM4, EM5, EM9, RG1, RG2, RG7 |
| `accounts` | Creation de compte, connexion, deconnexion, espace personnel et roles. | EF3, EF4, EM8, ENF3, RG6 |
| `cart` | Panier, lignes de panier, quantites et total. | EF5, EF6, EM2, EM3, RG2, RG3 |
| `orders` | Commandes, billets achetes, historique et statuts. | EF8, EF9, EF10, EM6, EM10, RG4, RG5, RG8 |
| `payments` | Paiement simule et resultat de paiement. | EF7, EF8, EF9, EM6, RG4, RG5 |

## Alternative possible

Pour un projet d'ecole de taille limitee, le decoupage pourra etre reduit a moins d'applications si cela simplifie la maintenance et les tests. Toute reduction devra etre documentee dans `docs/repository/decisions.md`.

## Non fait dans cette etape

- Pas de `django-admin startproject`.
- Pas de `python manage.py startapp`.
- Pas de modeles, vues, formulaires, URLs ou migrations.
