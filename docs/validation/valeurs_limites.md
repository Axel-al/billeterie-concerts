# Valeurs limites

## Quantité de billets par concert et commande

| Valeur | Classe | Résultat attendu | Exigences |
| --- | --- | --- | --- |
| -1 | Sous la limite | Refus | EM2, RG3 |
| 0 | Juste sous le minimum | Refus | EM2, RG3 |
| 1 | Minimum valide | Acceptation si stock suffisant | EM2, RG3 |
| 6 | Maximum valide | Acceptation si stock suffisant | EM3, RG3 |
| 7 | Juste au-dessus du maximum | Refus | EM3, RG3 |

Cas agrégés couverts : `3 + 3 = 6` accepté, `3 + 4 = 7` refusé pour un même concert, même avec deux catégories.

Les valeurs `0`, `1`, `6` et `7` sont aussi vérifiées dans le flux d'ajout au panier depuis la fiche concert.

## Stock

| Stock | Quantité | Résultat attendu | Exigences |
| --- | --- | --- | --- |
| 0 | 1 | Refus | EM1, RG2 |
| 1 | 1 | Acceptation | EM1, RG2 |
| 1 | 2 | Refus | EM1, RG2 |
| 6 | 6 | Acceptation | EM1, RG2 |
| 6 | 7 | Refus | EM1, RG2 |

Cas atomique complémentaire : pour un stock initial de 8 et une demande de 2,
un échec simulé de l'update conditionnel final doit laisser le stock à 8, le
panier actif et aucune commande ou paiement persistant (`EF12`, `EM1`, `EM6`,
`ENF4`, `RG2`, `RG5`).

## Date du concert

| Situation | Résultat attendu | Exigences |
| --- | --- | --- |
| Date passée | Absente du catalogue, fiche avec refus expliqué | EM4, RG1 |
| Date actuelle | Absente du catalogue, fiche avec refus expliqué | EM4, RG1 |
| Date future | Catalogue possible si statut ouvert et stock disponible | EF1, EM4, RG1 |

## Performance

| Mesure | Limite | Résultat attendu | Exigences |
| --- | --- | --- | --- |
| Temps d'affichage page standard | 2 secondes | Rester sous la limite en conditions normales | ENF2 |

## Numéro de carte simulé

| Longueur | Résultat attendu | Exigences |
| --- | --- | --- |
| 0 caractère | Refus du formulaire avec message français | ENF4 |
| 1 à 32 caractères | Paiement accepté uniquement pour la carte prévue, sinon refusé | EF7, EF8, EF9, RG4, RG5 |
| 33 caractères | Refus du formulaire avec message français | ENF4 |

## Paiement simulé

| Valeur | Résultat attendu | Exigences |
| --- | --- | --- |
| `4242424242424242` | Paiement accepté, commande payée, stock décrémenté | EF7, EF8, EF12, RG5 |
| Toute autre valeur non vide | Paiement refusé, aucune commande payée, stock inchangé | EF7, EF9, RG4 |
