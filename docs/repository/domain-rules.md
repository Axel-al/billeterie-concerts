# Règles domaine

## Réservation

Un concert est réservable seulement si :

- sa date est strictement future ;
- son statut est `open` ;
- au moins une catégorie possède du stock restant.

Une catégorie est réservable pour une quantité donnée seulement si son stock restant couvre cette quantité.

Les statuts `cancelled` et `closed` bloquent toute nouvelle réservation. `cancelled` représente une annulation du concert ; `closed` représente une clôture manuelle des ventes.

## Consultation publique

Le catalogue public affiche uniquement les concerts ouverts, strictement futurs et avec au moins une catégorie en stock.

Une fiche détaillée publique peut rester consultable lorsqu'un concert est annulé, clôturé, passé, terminé ou complet afin d'expliquer son indisponibilité. Les brouillons ne sont pas publiés et renvoient une réponse `404`.

La fiche affiche toutes les catégories, y compris celles dont le stock est nul. Un visiteur voit un lien de connexion avec retour vers la fiche seulement si le concert est réservable. Un utilisateur connecté voit un formulaire catégorie/quantité permettant d'ajouter des billets au panier.

## Quantités

La quantité doit être un entier entre 1 et 6. Le plafond de 6 s'applique au total des lignes du panier ou de la commande pour un même concert, pas seulement à chaque ligne.

Le modèle courant limite volontairement un panier actif et une commande à un seul concert. Les paniers multi-concerts sont rejetés par les services.

## Paiement simulé

Le service `process_simulated_payment` valide le panier dans une transaction.

- La carte simulée `4242424242424242` est acceptée.
- Toute autre valeur de carte est refusée.
- Le numéro de carte n'est pas stocké.
- Paiement accepté : une commande `paid` et un paiement `accepted` sont créés, les prix sont figés et le stock est décrémenté.
- Paiement refusé : une commande `refused` et un paiement `refused` sont créés, aucun stock n'est décrémenté et le panier reste actif pour permettre une nouvelle tentative future.
- Si une règle de quantité, stock, date, statut ou concert unique échoue, aucune commande validée n'est créée.

## Consultation des commandes

Les pages `Mes commandes` et détail de commande sont réservées aux utilisateurs connectés.

- L'historique affiche uniquement les commandes `paid` du client courant.
- Le détail de commande est filtré par propriétaire et par statut `paid`.
- Un utilisateur ne peut pas consulter la commande payée d'un autre utilisateur.
- Une commande `refused` reste non finale et exclue de l'historique des achats payés.

## Administration

- Le suivi admin des ventes exige `concerts.view_concert` et `orders.view_order`.
- Les actions d'annulation et de clôture exigent `concerts.change_concert`.
- Les visiteurs anonymes sont redirigés vers la connexion ; les utilisateurs authentifiés sans permission reçoivent `403`.
- L'annulation met le concert en `cancelled` et empêche toute nouvelle réservation.
- La clôture met le concert en `closed` et empêche toute nouvelle réservation.
- Ces changements de statut ne modifient pas le stock restant et ne masquent pas les commandes payées déjà accessibles à leur propriétaire.
- La synthèse admin compte seulement les commandes `paid`; les commandes `refused` ne contribuent pas aux ventes.

## Portée actuelle

Les règles de date, statut et stock sont aussi appliquées par le catalogue, les fiches publiques, l'ajout au panier et la validation du paiement. Les vues de confirmation/refus filtrent les commandes par utilisateur connecté. `EF10` et `RG8` sont couverts par l'historique payé et le détail de commande filtré par propriétaire. Le suivi admin des ventes est une fonctionnalité privilégiée distincte et ne modifie pas la portée de `RG8`.
