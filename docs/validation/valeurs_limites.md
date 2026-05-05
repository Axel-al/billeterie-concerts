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
| Date passee | Reservation refusee | EM4, RG1 |
| Date actuelle | Reservation refusee | EM4, RG1 |
| Date future | Reservation possible si autres conditions valides | EM4, RG1 |

## Performance

| Mesure | Limite | Resultat attendu | Exigences |
| --- | --- | --- | --- |
| Temps d'affichage page standard | 2 secondes | Rester sous la limite en conditions normales | ENF2 |
