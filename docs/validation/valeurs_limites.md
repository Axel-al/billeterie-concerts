# Valeurs limites

## Quantite de billets par concert et commande

| Valeur | Classe | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| -1 | Sous la limite | Refus | EM2, RG3 |
| 0 | Juste sous le minimum | Refus | EM2, RG3 |
| 1 | Minimum valide | Acceptation si stock suffisant | EM2, RG3 |
| 6 | Maximum valide | Acceptation si stock suffisant | EM3, RG3 |
| 7 | Juste au-dessus du maximum | Refus | EM3, RG3 |

Cas agreges couverts : `3 + 3 = 6` accepte, `3 + 4 = 7` refuse pour un meme concert, meme avec deux categories.

Les valeurs `0`, `1`, `6` et `7` sont aussi verifiees dans le flux d'ajout au panier depuis la fiche concert.

## Stock

| Stock | Quantite | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| 0 | 1 | Refus | EM1, RG2 |
| 1 | 1 | Acceptation | EM1, RG2 |
| 1 | 2 | Refus | EM1, RG2 |
| 6 | 6 | Acceptation | EM1, RG2 |
| 6 | 7 | Refus | EM1, RG2 |

## Date du concert

| Situation | Resultat attendu | Exigences |
| --- | --- | --- |
| Date passee | Absente du catalogue, fiche avec refus explique | EM4, RG1 |
| Date actuelle | Absente du catalogue, fiche avec refus explique | EM4, RG1 |
| Date future | Catalogue possible si statut ouvert et stock disponible | EF1, EM4, RG1 |

## Performance

| Mesure | Limite | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Temps d'affichage page standard | 2 secondes | Rester sous la limite en conditions normales | ENF2 |

## Paiement simule

| Valeur | Resultat attendu | Exigences |
| --- | --- | --- |
| `4242424242424242` | Paiement accepte, commande payee, stock decremente | EF7, EF8, EF12, RG5 |
| Toute autre valeur non vide | Paiement refuse, aucune commande payee, stock inchange | EF7, EF9, RG4 |
