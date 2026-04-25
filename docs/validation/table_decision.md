# Tables de decision

## Reservation d'une categorie

| Cas | Utilisateur connecte | Concert futur | Concert ouvert | Concert annule | Stock suffisant | Quantite 1..6 | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Oui | Oui | Oui | Non | Oui | Oui | Ajouter au panier |
| R2 | Non | Oui | Oui | Non | Oui | Oui | Refuser et demander connexion pour reservation |
| R3 | Oui | Non | Oui | Non | Oui | Oui | Refuser |
| R4 | Oui | Oui | Non | Non | Oui | Oui | Refuser |
| R5 | Oui | Oui | Oui | Oui | Oui | Oui | Refuser |
| R6 | Oui | Oui | Oui | Non | Non | Oui | Refuser |
| R7 | Oui | Oui | Oui | Non | Oui | Non | Refuser |

Exigences : EF5, EM1, EM2, EM3, EM4, EM5, RG1, RG2, RG3.

## Validation du paiement

| Cas | Utilisateur connecte | Panier valide | Paiement accepte | Decision | Effet stock |
| --- | --- | --- | --- | --- | --- |
| P1 | Oui | Oui | Oui | Commande payee et confirmation | Decremente |
| P2 | Oui | Oui | Non | Message de refus, commande non payee | Inchange |
| P3 | Non | Oui | Non applicable | Acces bloque | Inchange |
| P4 | Oui | Non | Non applicable | Validation refusee | Inchange |

Exigences : EF7, EF8, EF9, EF12, EM6, EM7, RG4, RG5, RG6.

## Consultation des commandes

| Cas | Utilisateur connecte | Commande appartient a l'utilisateur | Decision |
| --- | --- | --- | --- |
| C1 | Oui | Oui | Afficher |
| C2 | Oui | Non | Masquer ou refuser l'acces |
| C3 | Non | Non applicable | Demander connexion |

Exigences : EF10, RG8.
