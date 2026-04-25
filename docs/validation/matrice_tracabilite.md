# Matrice de tracabilite

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Etat de couverture actuel

Le depot ne contient pas encore de code applicatif Django ni de tests automatises. La couverture actuelle par du code et des tests est donc volontairement limitee :

- aucune exigence fonctionnelle `EF*` n'est implementee ;
- aucune exigence metier `EM*` n'est implementee ;
- aucune regle de gestion `RG*` n'est implementee ;
- aucun test automatise n'est versionne ;
- `ENF5` est partiellement preparee par la declaration de Ruff dans `requirements-dev.txt`, mais aucun check CI n'est encore implemente ;
- `ENF7` est partiellement preparee par le depot Git et le remote `origin`, mais aucun pipeline CI n'est encore versionne.

## Exigences fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Tests cibles |
| --- | --- | --- | --- | --- |
| EF1 | Aucune | Aucun | Non couvert | Integration liste concerts, e2e consultation |
| EF2 | Aucune | Aucun | Non couvert | Integration detail concert, e2e consultation |
| EF3 | Aucune | Aucun | Non couvert | Integration inscription, unicite email |
| EF4 | Aucune | Aucun | Non couvert | Integration login/logout |
| EF5 | Aucune | Aucun | Non couvert | Unitaire regles panier, integration ajout panier |
| EF6 | Aucune | Aucun | Non couvert | Unitaire calcul total panier |
| EF7 | Aucune | Aucun | Non couvert | Integration paiement simule |
| EF8 | Aucune | Aucun | Non couvert | Integration paiement accepte, e2e commande |
| EF9 | Aucune | Aucun | Non couvert | Integration paiement refuse |
| EF10 | Aucune | Aucun | Non couvert | Integration historique commandes |
| EF11 | Aucune | Aucun | Non couvert | Integration permissions admin concerts |
| EF12 | Aucune | Aucun | Non couvert | Unitaire et integration decrement stock |

## Exigences metier

| ID | Implementation actuelle | Tests actuels | Statut | Tests cibles |
| --- | --- | --- | --- | --- |
| EM1 | Aucune | Aucun | Non couvert | Stock insuffisant, concurrence a evaluer |
| EM2 | Aucune | Aucun | Non couvert | Quantite 0 refusee |
| EM3 | Aucune | Aucun | Non couvert | Quantite 7 refusee |
| EM4 | Aucune | Aucun | Non couvert | Concert passe non reservable |
| EM5 | Aucune | Aucun | Non couvert | Concert annule non reservable |
| EM6 | Aucune | Aucun | Non couvert | Paiement accepte/refuse |
| EM7 | Aucune | Aucun | Non couvert | Prix fige a la validation |
| EM8 | Aucune | Aucun | Non couvert | Email unique |
| EM9 | Aucune | Aucun | Non couvert | Droits administrateur |
| EM10 | Aucune | Aucun | Non couvert | Champs obligatoires commande |

## Exigences non fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Tests cibles |
| --- | --- | --- | --- | --- |
| ENF1 | Aucune interface | Aucun | Non couvert | Revue UX, e2e parcours nominal |
| ENF2 | Aucune application | Aucun | Non couvert | Mesure temps de reponse pages standard |
| ENF3 | Django prevu, pas initialise | Aucun | Non couvert | Test mot de passe hashe via auth Django |
| ENF4 | Aucune saisie applicative | Aucun | Non couvert | Tests formulaires invalides |
| ENF5 | `ruff` declare dans `requirements-dev.txt` | Aucun check versionne | Partiel tooling | `ruff check .` en local et CI |
| ENF6 | Tests prevus dans la documentation | Aucun | Non couvert | Tests unitaires et integration sur services isoles |
| ENF7 | Depot Git et remote `origin` presents | Aucun pipeline | Partiel versioning | Workflow GitHub Actions tests + qualite |

## Regles de gestion

| ID | Implementation actuelle | Tests actuels | Statut | Tests cibles |
| --- | --- | --- | --- | --- |
| RG1 | Aucune | Aucun | Non couvert | Concert reservable seulement si futur, ouvert et stock disponible |
| RG2 | Aucune | Aucun | Non couvert | Stock restant >= quantite demandee |
| RG3 | Aucune | Aucun | Non couvert | Quantite entiere entre 1 et 6 |
| RG4 | Aucune | Aucun | Non couvert | Paiement echoue, commande non validee |
| RG5 | Aucune | Aucun | Non couvert | Paiement reussi, commande payee et stock decremente |
| RG6 | Aucune | Aucun | Non couvert | Paiement bloque pour visiteur |
| RG7 | Aucune | Aucun | Non couvert | Annulation concert bloque nouvelles reservations |
| RG8 | Aucune | Aucun | Non couvert | Cloisonnement commandes par utilisateur |

## Regle de mise a jour

Chaque nouvelle implementation doit ajouter une preuve dans cette matrice :

- fichier ou module d'implementation ;
- fichier de test ;
- statut de couverture ;
- limite connue si la couverture est partielle.
