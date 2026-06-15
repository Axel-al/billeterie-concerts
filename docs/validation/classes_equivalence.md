# Classes d'équivalence

## Quantité de billets par concert et commande

| Classe | Valeurs exemples | Résultat attendu | Exigences |
| --- | --- | --- | --- |
| Quantité trop basse | -1, 0 | Refus | EM2, RG3 |
| Quantité minimale valide | 1 | Acceptation si stock suffisant | EM2, RG3 |
| Quantité nominale valide | 2, 3, 4, 5 | Acceptation si stock suffisant | EM3, RG3 |
| Quantité maximale valide | 6 | Acceptation si stock suffisant | EM3, RG3 |
| Quantité trop haute | 7, 10 | Refus | EM3, RG3 |
| Quantité non entière | 1.5, texte, vide | Refus propre | ENF4, RG3 |

Le plafond de 6 est valide sur la quantité totale du concert dans le panier ou la commande, même si les billets sont répartis sur plusieurs catégories.

## Stock disponible

| Classe | Situation | Résultat attendu | Exigences |
| --- | --- | --- | --- |
| Stock supérieur à la demande | stock 10, demande 2 | Acceptation | EF5, RG2 |
| Stock égal à la demande | stock 2, demande 2 | Acceptation | EF5, RG2 |
| Stock inférieur à la demande | stock 1, demande 2 | Refus | EM1, RG2 |
| Stock nul | stock 0 | Refus | EM1, RG1, RG2 |
| Décrément conditionnel sans ligne modifiée | Stock valide au contrôle, échec de l'update atomique | Refus et rollback complet | EF12, EM1, EM6, ENF4, RG2, RG5 |

La contrainte de modèle interdit aussi un stock restant négatif. Le cas d'échec
conditionnel vérifie qu'aucune commande, aucun paiement et aucune transition du
panier ne subsistent après rollback.

## État du concert

| Classe | Situation | Résultat attendu dans le catalogue et la fiche | Exigences |
| --- | --- | --- | --- |
| Ouvert et futur | Concert réservable avec stock | Catalogue et fiche visibles, connexion proposée au visiteur | EF1, EF2, RG1 |
| Brouillon | Non ouvert à la vente | Absent du catalogue, fiche publique `404` | RG1 |
| Complet | Aucun stock disponible | Absent du catalogue, fiche avec motif et sans CTA | RG1 |
| Annulé | Statut annulé | Absent du catalogue, fiche avec motif et sans CTA | EM5, RG7 |
| Terminé ou passé | Date passée | Absent du catalogue, fiche avec motif et sans CTA | EM4, RG1 |

Dans l'implémentation courante, une date égale à l'instant courant est considérée comme non réservable ; le concert doit être strictement futur.

## Paiement

| Classe | Situation | Résultat attendu | Exigences |
| --- | --- | --- | --- |
| Paiement accepté | Carte `4242424242424242` | Commande payée, confirmation affichée, stock décrémenté | EF7, EF8, EF12, EM6, RG5 |
| Paiement refusé | Toute autre carte | Pas de commande validée, message explicite, stock inchangé | EF7, EF9, EM6, RG4 |
| Panier invalide | Panier vide, inactif ou devenu non réservable | Paiement bloqué proprement | ENF4, RG1, RG2, RG3, RG6 |

Le numéro de carte n'est pas stocké ; seule la décision acceptée/refusée est conservée dans `Payment`.

## Authentification et droits

| Classe | Situation | Résultat attendu | Exigences |
| --- | --- | --- | --- |
| Visiteur | Non connecté | Consultation autorisée, paiement bloqué | EF1, EF2, RG6 |
| Client | Connecté sans droits admin | Réservation, panier, checkout et paiement autorisés pour son propre panier | EF5, EF6, EF7, RG6 |
| Client tiers | Connecté avec un autre compte | Panier/checkout personnels uniquement ; pages résultat d'une autre commande inaccessibles | RG8 |
| Administrateur | Connecté avec droits admin | Gestion concerts autorisée | EF11, EM9 |
