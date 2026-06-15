# Tables de decision

## Consultation d'un concert

| Cas | Statut | Date future | Stock disponible | Catalogue | Fiche | Action de reservation |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | Ouvert | Oui | Oui | Afficher | Afficher | Connexion proposee au visiteur |
| L2 | Ouvert | Oui | Non | Masquer | Afficher motif complet | Aucune |
| L3 | Annule | Oui | Oui ou non | Masquer | Afficher motif annulation | Aucune |
| L4 | Ouvert ou termine | Non | Oui ou non | Masquer | Afficher motif date passee | Aucune |
| L5 | Termine ou complet | Oui | Oui ou non | Masquer | Afficher motif adapte | Aucune |
| L6 | Brouillon | Oui ou non | Oui ou non | Masquer | Reponse `404` | Aucune |

Exigences : EF1, EF2, EM4, EM5, RG1, RG7.

## Reservation d'une categorie

| Cas | Utilisateur connecte | Panier mono-concert | Concert futur | Concert ouvert | Concert annule | Stock suffisant | Quantite totale concert 1..6 | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Oui | Oui | Oui | Oui | Non | Oui | Oui | Ajouter au panier |
| R2 | Non | Oui | Oui | Oui | Non | Oui | Oui | Rediriger vers la connexion |
| R3 | Oui | Oui | Non | Oui | Non | Oui | Oui | Refuser |
| R4 | Oui | Oui | Oui | Non | Non | Oui | Oui | Refuser |
| R5 | Oui | Oui | Oui | Oui | Oui | Oui | Oui | Refuser |
| R6 | Oui | Oui | Oui | Oui | Non | Non | Oui | Refuser |
| R7 | Oui | Oui | Oui | Oui | Non | Oui | Non | Refuser |
| R8 | Oui | Non | Oui | Oui | Non | Oui | Oui | Refuser |

Exigences : EF5, EM1, EM2, EM3, EM4, EM5, RG1, RG2, RG3.

## Validation du paiement

| Cas | Utilisateur connecte | Panier valide | Paiement accepte | Decrement conditionnel | Decision | Effet stock |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | Oui | Oui | Oui, carte `4242424242424242` | Reussi | Commande payee et confirmation affichee | Decremente |
| P2 | Oui | Oui | Non, autre carte | Non execute | Commande refusee et message explicite | Inchange |
| P3 | Non | Oui | Non applicable | Non execute | Acces bloque | Inchange |
| P4 | Oui | Non | Non applicable | Non execute | Validation refusee | Inchange |
| P5 | Oui | Oui | Oui, carte acceptee | Echec | Transaction annulee, aucune commande ni paiement persistant | Inchange |

Exigences : EF7, EF8, EF9, EF12, EM1, EM6, EM7, ENF4, RG2, RG4, RG5, RG6.

`P1` et `P2` sont couverts par le service de paiement et les vues. `P3` est
couvert par les vues `LoginRequiredMixin`. `P5` est couvert par
`tests/test_core_domain.py::test_failed_conditional_stock_update_rolls_back_payment`.

## Consultation des commandes

| Cas | Utilisateur connecte | Commande appartient a l'utilisateur | Decision |
| --- | --- | --- | --- |
| C1 | Oui | Oui | Afficher |
| C2 | Oui | Non | Masquer ou refuser l'acces |
| C3 | Non | Non applicable | Demander connexion |

Exigences : EF10, RG8.

`EF10` et `RG8` sont couverts par l'historique des commandes payees et le detail de commande filtre par proprietaire. Les commandes refusees restent non finales et sont exclues de l'historique des achats payes.
