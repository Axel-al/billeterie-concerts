# Tables de décision

## Consultation d'un concert

| Cas | Statut | Date future | Stock disponible | Catalogue | Fiche | Action de réservation |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | Ouvert | Oui | Oui | Afficher | Afficher | Connexion proposée au visiteur |
| L2 | Ouvert | Oui | Non | Masquer | Afficher motif complet | Aucune |
| L3 | Annulé | Oui | Oui ou non | Masquer | Afficher motif annulation | Aucune |
| L4 | Ouvert ou terminé | Non | Oui ou non | Masquer | Afficher motif date passée | Aucune |
| L5 | Terminé ou complet | Oui | Oui ou non | Masquer | Afficher motif adapté | Aucune |
| L6 | Brouillon | Oui ou non | Oui ou non | Masquer | Réponse `404` | Aucune |

Exigences : EF1, EF2, EM4, EM5, RG1, RG7.

## Réservation d'une catégorie

| Cas | Utilisateur connecté | Panier mono-concert | Concert futur | Concert ouvert | Concert annulé | Stock suffisant | Quantité totale concert 1..6 | Décision |
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

| Cas | Utilisateur connecté | Panier valide | Paiement accepté | Décrément conditionnel | Décision | Effet stock |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | Oui | Oui | Oui, carte `4242424242424242` | Réussi | Commande payée et confirmation affichée | Décrémente |
| P2 | Oui | Oui | Non, autre carte | Non exécuté | Commande refusée et message explicite | Inchangé |
| P3 | Non | Oui | Non applicable | Non exécuté | Accès bloqué | Inchangé |
| P4 | Oui | Non | Non applicable | Non exécuté | Validation refusée | Inchangé |
| P5 | Oui | Oui | Oui, carte acceptée | Échec | Transaction annulée, aucune commande ni paiement persistant | Inchangé |
| P6 | Oui | Oui | Saisie vide ou supérieure à 32 caractères | Non exécuté | Formulaire refusé avec message français | Inchangé |

Exigences : EF7, EF8, EF9, EF12, EM1, EM6, EM7, ENF4, RG2, RG4, RG5, RG6.

`P1` et `P2` sont couverts par le service de paiement et les vues. `P3` est
couvert par les vues `LoginRequiredMixin`. `P5` est couvert par
`tests/test_core_domain.py::test_failed_conditional_stock_update_rolls_back_payment`.
`P6` est couvert par
`tests/test_booking_flow.py::test_payment_form_keeps_html_constraints_and_displays_french_errors`.

## Consultation des commandes

| Cas | Utilisateur connecté | Commande appartient à l'utilisateur | Décision |
| --- | --- | --- | --- |
| C1 | Oui | Oui | Afficher |
| C2 | Oui | Non | Masquer ou refuser l'accès |
| C3 | Non | Non applicable | Demander connexion |

Exigences : EF10, RG8.

`EF10` et `RG8` sont couverts par l'historique des commandes payées et le détail de commande filtré par propriétaire. Les commandes refusées restent non finales et sont exclues de l'historique des achats payés.
