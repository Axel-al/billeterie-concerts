# Regles domaine

## Reservation

Un concert est reservable seulement si :

- sa date est strictement future ;
- son statut est `open` ;
- au moins une categorie possede du stock restant.

Une categorie est reservable pour une quantite donnee seulement si son stock restant couvre cette quantite.

## Consultation publique

Le catalogue public affiche uniquement les concerts ouverts, strictement futurs et avec au moins une categorie en stock.

Une fiche detaillee publique peut rester consultable lorsqu'un concert est annule, passe, termine ou complet afin d'expliquer son indisponibilite. Les brouillons ne sont pas publies et renvoient une reponse `404`.

La fiche affiche toutes les categories, y compris celles dont le stock est nul. Un visiteur voit un lien de connexion avec retour vers la fiche seulement si le concert est reservable. Aucun formulaire panier ni ajout de billet n'est expose dans cette etape.

## Quantites

La quantite doit etre un entier entre 1 et 6. Le plafond de 6 s'applique au total des lignes du panier ou de la commande pour un meme concert, pas seulement a chaque ligne.

Le modele courant limite volontairement un panier actif et une commande a un seul concert. Les paniers multi-concerts sont rejetes par les services.

## Paiement simule

Le service `process_simulated_payment` valide le panier dans une transaction.

- Paiement accepte : une commande `paid` et un paiement `accepted` sont crees, les prix sont snapshots et le stock est decremente.
- Paiement refuse : une commande `refused` et un paiement `refused` sont crees, aucun stock n'est decremente et le panier reste actif pour permettre une nouvelle tentative future.
- Si une regle de quantite, stock, date, statut ou concert unique echoue, aucune commande validee n'est creee.

## Portee actuelle

Les regles de date, statut et stock sont aussi appliquees par le catalogue et les fiches publiques. Il n'existe pas encore de vue de panier, paiement, confirmation, refus explicite ou historique de commandes.
