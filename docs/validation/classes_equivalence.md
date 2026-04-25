# Classes d'equivalence

## Quantite de billets

| Classe | Valeurs exemples | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Quantite trop basse | -1, 0 | Refus | EM2, RG3 |
| Quantite minimale valide | 1 | Acceptation si stock suffisant | EM2, RG3 |
| Quantite nominale valide | 2, 3, 4, 5 | Acceptation si stock suffisant | EM3, RG3 |
| Quantite maximale valide | 6 | Acceptation si stock suffisant | EM3, RG3 |
| Quantite trop haute | 7, 10 | Refus | EM3, RG3 |
| Quantite non entiere | 1.5, texte, vide | Refus propre | ENF4, RG3 |

## Stock disponible

| Classe | Situation | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Stock superieur a la demande | stock 10, demande 2 | Acceptation | EF5, RG2 |
| Stock egal a la demande | stock 2, demande 2 | Acceptation | EF5, RG2 |
| Stock inferieur a la demande | stock 1, demande 2 | Refus | EM1, RG2 |
| Stock nul | stock 0 | Refus | EM1, RG1, RG2 |

## Etat du concert

| Classe | Situation | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Ouvert et futur | Concert reservable avec stock | Reservation possible | RG1 |
| Brouillon | Non ouvert a la vente | Reservation impossible | RG1 |
| Complet | Aucun stock disponible | Reservation impossible | RG1 |
| Annule | Statut annule | Reservation impossible | EM5, RG7 |
| Termine ou passe | Date passee | Reservation impossible | EM4, RG1 |

## Paiement

| Classe | Situation | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Paiement accepte | Simulateur renvoie succes | Commande payee, stock decremente | EF8, EM6, RG5 |
| Paiement refuse | Simulateur renvoie refus | Pas de commande validee, stock inchange | EF9, RG4 |

## Authentification et droits

| Classe | Situation | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Visiteur | Non connecte | Consultation autorisee, paiement bloque | EF1, EF2, RG6 |
| Client | Connecte sans droits admin | Reservation autorisee, administration bloquee | EF5, EM9 |
| Administrateur | Connecte avec droits admin | Gestion concerts autorisee | EF11, EM9 |
