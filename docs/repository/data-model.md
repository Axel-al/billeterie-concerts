# Modele de donnees

## Vue d'ensemble

Le modele courant couvre le noyau domaine de la billetterie sans interface de checkout.

| Concept | Application | Role |
| --- | --- | --- |
| Concert | `concerts` | Evenement reserve ou non selon date, statut et stock. |
| SeatCategory | `concerts` | Categorie de place avec prix, stock initial et stock restant. |
| Cart | `cart` | Panier actif d'un utilisateur, limite a un seul concert. |
| CartLine | `cart` | Quantite demandee pour une categorie de place. |
| Order | `orders` | Resultat d'une tentative de paiement, rattache a un utilisateur, un concert, une date et un statut. |
| OrderLine | `orders` | Ligne de commande avec nom de categorie et prix unitaire figes. |
| Payment | `payments` | Resultat accepte ou refuse du paiement simule. |

## Contraintes principales

- `SeatCategory` est unique par couple concert/nom et son stock restant ne peut pas etre negatif.
- `CartLine` et `OrderLine` imposent une quantite ligne entre 1 et 6.
- Les services imposent en plus le plafond de 6 billets au total pour le concert du panier ou de la commande.
- Un utilisateur ne peut avoir qu'un seul panier actif.
- Un panier actif ne peut contenir qu'un seul concert ; une commande reference aussi un seul concert.
- `Payment` est en relation un-a-un avec `Order`.

## Snapshots

Les prix affiches dans le panier restent les prix courants des categories. Lors du paiement simule, chaque `OrderLine` fige :

- le nom de la categorie achetee ;
- le prix unitaire au moment de la validation ;
- la quantite.

Une modification ulterieure du prix d'une categorie ne change donc pas les commandes deja creees.
