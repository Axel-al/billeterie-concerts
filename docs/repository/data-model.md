# Modèle de données

## Entités

| Modèle | Application | Rôle |
| --- | --- | --- |
| `User` | `accounts` | Compte identifié par une adresse e-mail unique. |
| `Concert` | `concerts` | Événement, date, lieu et statut de vente. |
| `SeatCategory` | `concerts` | Prix et stocks d'une catégorie pour un concert. |
| `Cart` | `cart` | Panier actif, validé ou abandonné d'un utilisateur. |
| `CartLine` | `cart` | Catégorie et quantité demandées. |
| `Order` | `orders` | Résultat payé ou refusé d'une tentative. |
| `OrderLine` | `orders` | Quantité, catégorie et prix figés. |
| `Payment` | `payments` | Résultat accepté ou refusé associé à une commande. |

## Relations

```text
User 1 ── n Cart
User 1 ── n Order
Concert 1 ── n SeatCategory
Concert 1 ── n Cart
Concert 1 ── n Order
Cart 1 ── n CartLine
SeatCategory 1 ── n CartLine
Order 1 ── n OrderLine
SeatCategory 1 ── n OrderLine
Order 1 ── 1 Payment
```

## Statuts

Concert :

- `draft` : brouillon non publié ;
- `open` : ouvert à la vente ;
- `closed` : ventes clôturées ;
- `sold_out` : complet ;
- `cancelled` : annulé ;
- `finished` : terminé.

Panier :

- `active` ;
- `checked_out` ;
- `abandoned`.

Commande :

- `pending` ;
- `paid` ;
- `refused` ;
- `cancelled`.

Paiement :

- `accepted` ;
- `refused`.

Le parcours simulé crée directement une commande `paid` ou `refused`. Les
statuts `pending`, `cancelled` et `abandoned` existent dans le modèle, mais ne
sont pas exposés par le parcours actuel.

## Contraintes

- `User.email` est unique.
- Une catégorie est unique par couple concert/nom.
- Les stocks initial et restant ne peuvent pas être négatifs.
- Une ligne de panier ou de commande contient entre 1 et 6 billets.
- Les services appliquent aussi la limite de 6 au total des lignes du concert.
- Un utilisateur ne peut avoir qu'un panier `active`.
- Un panier actif et une commande ne concernent qu'un concert.
- Un paiement est lié en un-à-un à une commande.

## Prix figés

Le panier calcule son total avec les prix courants. Au paiement,
`OrderLine` enregistre :

- `category_name_snapshot` ;
- `unit_price` ;
- `quantity`.

Une modification ultérieure de la catégorie n'altère donc pas une commande
payée existante.

## Stock

Le stock n'est décrémenté qu'après acceptation du paiement. Le service utilise
une transaction, des verrous ORM et une mise à jour conditionnelle. Un échec
annule l'ensemble de la transaction.

Une commande `refused` et son paiement sont conservés comme trace non finale,
mais le panier reste actif et le stock ne change pas.
