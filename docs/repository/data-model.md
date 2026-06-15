# Modèle de données

## Vue d'ensemble

Le modèle courant couvre le noyau domaine de la billetterie et le parcours panier/checkout/paiement simulé.

| Concept | Application | Rôle |
| --- | --- | --- |
| Concert | `concerts` | Événement réservé ou non selon date, statut et stock. |
| SeatCategory | `concerts` | Catégorie de place avec prix, stock initial et stock restant. |
| Cart | `cart` | Panier actif d'un utilisateur, limité à un seul concert. |
| CartLine | `cart` | Quantité demandée pour une catégorie de place. |
| Order | `orders` | Résultat d'une tentative de paiement, rattaché à un utilisateur, un concert, une date et un statut. |
| OrderLine | `orders` | Ligne de commande avec nom de catégorie et prix unitaire figés. |
| Payment | `payments` | Résultat accepté ou refusé du paiement simulé. |

`Concert.status` contient maintenant les états `draft`, `open`, `closed`, `sold_out`, `cancelled` et `finished`. Le statut `closed` représente une vente clôturée manuellement par l'administration : le concert reste consultable mais n'est plus réservable.

## Contraintes principales

- `SeatCategory` est unique par couple concert/nom et son stock restant ne peut pas être négatif.
- `CartLine` et `OrderLine` imposent une quantité ligne entre 1 et 6.
- Les services imposent en plus le plafond de 6 billets au total pour le concert du panier ou de la commande.
- Un utilisateur ne peut avoir qu'un seul panier actif. Les vues panier et checkout ne consultent que le panier actif de l'utilisateur connecté.
- Un panier actif ne peut contenir qu'un seul concert ; une commande référence aussi un seul concert.
- `Payment` est en relation un-a-un avec `Order`.
- Les pages de confirmation et de refus filtrent les commandes par utilisateur connecté.
- Les vues d'administration des ventes calculent les ventes à partir des commandes `paid` existantes ; aucun total de vente supplémentaire n'est stocké.

## Snapshots

Les prix affichés dans le panier restent les prix courants des catégories. Lors du paiement simulé, chaque `OrderLine` fige :

- le nom de la catégorie achetée ;
- le prix unitaire au moment de la validation ;
- la quantité.

Une modification ultérieure du prix d'une catégorie ne change donc pas les commandes déjà créées.

La synthèse admin des ventes utilise ces snapshots et les montants de commandes payées. Les commandes refusées restent tracées mais ne comptent ni dans le chiffre d'affaires ni dans les billets vendus.

## Paiement simulé

Le numéro de carte n'est pas stocké. La vue de paiement transmet seulement le résultat déterminé au service :

- `4242424242424242` après normalisation des espaces : paiement accepté ;
- toute autre valeur saisie : paiement refusé.
