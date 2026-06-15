# Règles métier

## Réservabilité

Un concert est réservable si toutes les conditions suivantes sont vraies :

- sa date est strictement future ;
- son statut est `open` ;
- au moins une catégorie possède du stock.

Les brouillons ne sont pas publiés. Les concerts passés, annulés, clôturés,
terminés ou complets peuvent conserver une fiche publique explicative, sans
action de réservation.

Exigences : `EF1`, `EF2`, `EM4`, `EM5`, `RG1`, `RG7`.

## Quantité

- La quantité doit être un entier.
- Le minimum est 1.
- Le maximum est 6 pour le total du concert dans le panier.
- Une catégorie doit posséder au moins la quantité demandée.
- Un panier actif est limité à un concert.

Ces règles sont appliquées par le formulaire Django, les validateurs de modèle
et les services métier. Les attributs HTML restent une aide à la saisie, pas
une frontière de sécurité.

Exigences : `EF5`, `EM1`, `EM2`, `EM3`, `ENF4`, `RG2`, `RG3`.

## Paiement

- La carte `4242424242424242`, espaces retirés, est acceptée.
- Toute autre valeur non vide et d'au plus 32 caractères est refusée.
- Le numéro de carte n'est jamais stocké.
- Une saisie vide ou trop longue est refusée par le formulaire en français.

Paiement accepté :

- création d'une commande `paid` ;
- création d'un paiement `accepted` ;
- prix figés ;
- décrément conditionnel du stock ;
- panier `checked_out`.

Paiement refusé :

- création d'une commande `refused` non finale ;
- création d'un paiement `refused` ;
- stock inchangé ;
- panier toujours `active`.

Si le panier ou le stock devient invalide, la transaction est annulée.

Exigences : `EF7`, `EF8`, `EF9`, `EF12`, `EM1`, `EM6`, `EM7`, `EM10`,
`RG4`, `RG5`, `RG6`.

## Commandes

- L'historique exige une authentification.
- Il affiche uniquement les commandes `paid` du client courant.
- Le détail est filtré par propriétaire et statut `paid`.
- Une commande d'un autre client ou une commande refusée renvoie `404`.
- Les prix affichés proviennent des lignes figées.

Exigences : `EF10`, `RG8`.

## Administration

- La synthèse des ventes exige `concerts.view_concert` et
  `orders.view_order`.
- Annuler ou clôturer exige `concerts.change_concert`.
- Un client standard reçoit `403`.
- L'annulation passe le statut à `cancelled`.
- La clôture passe le statut à `closed`.
- Les commandes payées existantes et le stock restant sont conservés.
- Seules les commandes payées contribuent aux ventes.

Exigences : `EF11`, `EM9`, `RG7`.

## Transitions non automatiques

L'application ne passe pas automatiquement un concert à `sold_out` lorsque le
stock atteint zéro, ni à `finished` lorsque sa date est passée. Les contrôles
de réservation utilisent directement le stock et la date, ce qui préserve les
règles même si le statut n'a pas été actualisé.
