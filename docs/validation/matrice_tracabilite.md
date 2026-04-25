# Matrice de tracabilite

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Etat de couverture actuel

Le depot contient une fondation Django minimale, des tests automatises, Ruff, coverage, GitHub Actions et une configuration SonarCloud.

- `EF3` est partiellement preparee par le modele utilisateur email + mot de passe, sans interface d'inscription ;
- `EM8` est couverte au niveau modele par l'email unique ;
- `ENF3` est couverte par le hachage des mots de passe via Django ;
- `ENF5`, `ENF6` et `ENF7` sont couvertes par Ruff, tests, coverage et CI ;
- aucune exigence de consultation de concerts, panier, paiement, stock ou commandes n'est implementee ;
- aucune regle de gestion `RG*` n'est implementee ;
- `ENF1` n'est pas revendiquee malgre la page d'accueil, car les actions principales du parcours metier ne sont pas encore presentes.

## Exigences fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Tests cibles |
| --- | --- | --- | --- | --- |
| EF1 | Aucune | Aucun | Non couvert | Integration liste concerts, e2e consultation |
| EF2 | Aucune | Aucun | Non couvert | Integration detail concert, e2e consultation |
| EF3 | `accounts.User` avec email et mot de passe Django | `tests/test_accounts.py` | Partiel fondation modele | Integration inscription |
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
| EM8 | `accounts.User.email` unique | `tests/test_accounts.py::test_user_email_must_be_unique` | Couvert modele | Formulaire inscription email deja utilise |
| EM9 | Aucune | Aucun | Non couvert | Droits administrateur |
| EM10 | Aucune | Aucun | Non couvert | Champs obligatoires commande |

## Exigences non fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Tests cibles |
| --- | --- | --- | --- | --- |
| ENF1 | Page d'accueil minimale seulement | Aucun | Non couvert | Revue UX, e2e parcours nominal |
| ENF2 | Aucune application | Aucun | Non couvert | Mesure temps de reponse pages standard |
| ENF3 | Mot de passe gere par Django auth | `tests/test_accounts.py::test_user_password_is_hashed` | Couvert fondation | Tests inscription et connexion |
| ENF4 | Aucune saisie applicative | Aucun | Non couvert | Tests formulaires invalides |
| ENF5 | Ruff configure dans `pyproject.toml` et CI | `ruff check .` local et CI | Couvert fondation | Suivi des futurs problemes Ruff/Sonar |
| ENF6 | Tests pytest-django isoles pour accueil et compte | `pytest`, `pytest --cov=. --cov-report=xml` | Couvert fondation | Tests metier a ajouter |
| ENF7 | Workflow GitHub Actions versionne | `.github/workflows/ci.yml` | Couvert fondation, CI distante a confirmer apres push | Suivi CI sur PR |

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
