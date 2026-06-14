# Classes d'equivalence

## Quantite de billets par concert et commande

| Classe | Valeurs exemples | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Quantite trop basse | -1, 0 | Refus | EM2, RG3 |
| Quantite minimale valide | 1 | Acceptation si stock suffisant | EM2, RG3 |
| Quantite nominale valide | 2, 3, 4, 5 | Acceptation si stock suffisant | EM3, RG3 |
| Quantite maximale valide | 6 | Acceptation si stock suffisant | EM3, RG3 |
| Quantite trop haute | 7, 10 | Refus | EM3, RG3 |
| Quantite non entiere | 1.5, texte, vide | Refus propre | ENF4, RG3 |

Le plafond de 6 est valide sur la quantite totale du concert dans le panier ou la commande, meme si les billets sont repartis sur plusieurs categories.

## Stock disponible

| Classe | Situation | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Stock superieur a la demande | stock 10, demande 2 | Acceptation | EF5, RG2 |
| Stock egal a la demande | stock 2, demande 2 | Acceptation | EF5, RG2 |
| Stock inferieur a la demande | stock 1, demande 2 | Refus | EM1, RG2 |
| Stock nul | stock 0 | Refus | EM1, RG1, RG2 |

La contrainte de modele interdit aussi un stock restant negatif.

## Etat du concert

| Classe | Situation | Resultat attendu dans le catalogue et la fiche | Exigences |
| --- | --- | --- | --- |
| Ouvert et futur | Concert reservable avec stock | Catalogue et fiche visibles, connexion proposee au visiteur | EF1, EF2, RG1 |
| Brouillon | Non ouvert a la vente | Absent du catalogue, fiche publique `404` | RG1 |
| Complet | Aucun stock disponible | Absent du catalogue, fiche avec motif et sans CTA | RG1 |
| Annule | Statut annule | Absent du catalogue, fiche avec motif et sans CTA | EM5, RG7 |
| Termine ou passe | Date passee | Absent du catalogue, fiche avec motif et sans CTA | EM4, RG1 |

Dans l'implementation courante, une date egale a l'instant courant est consideree comme non reservable ; le concert doit etre strictement futur.

## Paiement

| Classe | Situation | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Paiement accepte | Simulateur renvoie succes | Commande payee, stock decremente | EF8, EM6, RG5 |
| Paiement refuse | Simulateur renvoie refus | Pas de commande validee, stock inchange | EF9, RG4 |

La couverture actuelle est domaine/service : aucune page de confirmation ni message visible de refus n'est encore implemente.

## Authentification et droits

| Classe | Situation | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Visiteur | Non connecte | Consultation autorisee, paiement bloque | EF1, EF2, RG6 |
| Client | Connecte sans droits admin | Reservation autorisee, administration bloquee | EF5, EM9 |
| Administrateur | Connecte avec droits admin | Gestion concerts autorisee | EF11, EM9 |
