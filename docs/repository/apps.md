# Applications Django

## Etat actuel

Le depot contient cinq applications Django metier :

| Application | Etat actuel | Exigences liees |
| --- | --- | --- |
| `accounts` | Modele `User` personnalise avec email unique, manager, admin Django, inscription, connexion, deconnexion POST et espace personnel protege. | EF3, EF4, EM8, ENF3, ENF4 |
| `concerts` | Modeles `Concert` et `SeatCategory`, admin avec categories inline, commande `seed_demo_data`. | EF5 partiel, EF11 fondation admin, EF12, EM1, EM4, EM5, RG1, RG2, RG7 |
| `cart` | Modeles `Cart` et `CartLine`, services d'ajout et validation de panier. | EF5 partiel service, EF6 partiel service, EM1, EM2, EM3, RG2, RG3 |
| `orders` | Modeles `Order` et `OrderLine`, statuts et prix snapshots. | EF8/EF9 partiels service, EM6, EM7, EM10, RG4, RG5 |
| `payments` | Modele `Payment` et service de paiement simule accepte/refuse. | EF7 partiel service, EF8/EF9 partiels service, EF12, EM6, RG4, RG5 |

Le module `config` porte les reglages, les URLs racines, le rendu de la page d'accueil et les redirections d'authentification. Aucune vue panier, paiement, confirmation ou historique n'est encore implementee.

## Decoupage retenu

| Application | Responsabilite |
| --- | --- |
| `accounts` | Identite utilisateur, inscription, authentification et espace personnel de base. |
| `concerts` | Donnees de concerts, categories de places, stock et statut de reservation. |
| `cart` | Panier actif utilisateur, lignes de panier, quantites et total courant. |
| `orders` | Commandes issues d'une tentative de paiement, lignes figeant prix et categorie. |
| `payments` | Resultat du paiement simule et orchestration transactionnelle du paiement. |

## Decisions appliquees

- `cart` et `payments` sont des applications separees pour correspondre a l'architecture cible.
- Un panier actif et une commande ne portent qu'un seul concert. Cette limite simplifie la couverture de `EM10` et permet d'appliquer clairement le plafond de 6 billets par concert/commande.
- `EF5`, `EF7`, `EF8` et `EF9` sont couvertes seulement au niveau domaine/service dans cette etape. Les pages, confirmations et messages utilisateur restent a implementer.
- Le role administrateur repose pour l'instant sur l'admin Django et les champs `is_staff` / `is_superuser`. Cette fondation ne revendique pas la couverture de `EM9`, car les permissions de gestion des concerts restent hors de cette etape.

## Non fait dans cette etape

- Pas de liste ou detail de concerts.
- Pas de pages panier, paiement, confirmation, refus de paiement ou historique.
- Pas d'historique de commandes dans `Mon espace`.
- Pas de test de cloisonnement d'historique de commandes (`RG8`) ni de blocage paiement visiteur (`RG6`).
