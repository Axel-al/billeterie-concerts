# Regles domaine

## Reservation

Un concert est reservable seulement si :

- sa date est strictement future ;
- son statut est `open` ;
- au moins une categorie possede du stock restant.

Une categorie est reservable pour une quantite donnee seulement si son stock restant couvre cette quantite.

## Quantites

La quantite doit etre un entier entre 1 et 6. Le plafond de 6 s'applique au total des lignes du panier ou de la commande pour un meme concert, pas seulement a chaque ligne.

Le modele courant limite volontairement un panier actif et une commande a un seul concert. Les paniers multi-concerts sont rejetes par les services.

## Paiement simule

Le service `process_simulated_payment` valide le panier dans une transaction.

- Paiement accepte : une commande `paid` et un paiement `accepted` sont crees, les prix sont snapshots et le stock est decremente.
- Paiement refuse : une commande `refused` et un paiement `refused` sont crees, aucun stock n'est decremente et le panier reste actif pour permettre une nouvelle tentative future.
- Si une regle de quantite, stock, date, statut ou concert unique echoue, aucune commande validee n'est creee.

## Portee actuelle

Ces regles sont couvertes au niveau domaine/service. Il n'existe pas encore de vue de panier, paiement, confirmation, refus explicite ou historique de commandes.
