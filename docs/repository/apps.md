# Applications Django

## Etat actuel

Le depot contient cinq applications Django metier :

| Application | Etat actuel | Exigences liees |
| --- | --- | --- |
| `accounts` | Modele `User` personnalise avec email unique, manager, admin Django, inscription, connexion, deconnexion POST et espace personnel protege. | EF3, EF4, EM8, ENF3, ENF4 |
| `concerts` | Modeles `Concert` et `SeatCategory`, catalogue public, fiches detaillees, admin avec categories inline, commande `seed_demo_data`. | EF1, EF2, EF5 partiel, EF11 fondation admin, EF12, EM1, EM4, EM5, RG1, RG2, RG7 |
| `cart` | Modeles `Cart` et `CartLine`, services d'ajout/validation de panier, vues panier et checkout. | EF5, EF6, EM1, EM2, EM3, RG2, RG3, RG6 |
| `orders` | Modeles `Order` et `OrderLine`, statuts, prix snapshots et pages resultat filtrees par utilisateur. | EF8, EF9, EM6, EM7, EM10, RG4, RG5, RG8 partiel |
| `payments` | Modele `Payment`, regle de carte simulee, service de paiement et vues paiement/confirmation/refus. | EF7, EF8, EF9, EF12, EM6, RG4, RG5, RG6 |

Le module `config` porte les reglages, les URLs racines, le rendu de la page d'accueil et les redirections d'authentification. Le catalogue est disponible sur `/concerts/`, les fiches sur `/concerts/<id>/`, le panier sur `/panier/`, le checkout sur `/panier/validation/` et le paiement simule sur `/paiement/`. L'historique complet des commandes n'est pas encore implemente.

## Decoupage retenu

| Application | Responsabilite |
| --- | --- |
| `accounts` | Identite utilisateur, inscription, authentification et espace personnel de base. |
| `concerts` | Donnees de concerts, categories de places, stock, statut de reservation et consultation publique. |
| `cart` | Panier actif utilisateur, lignes de panier, quantites et total courant. |
| `orders` | Commandes issues d'une tentative de paiement, lignes figeant prix et categorie. |
| `payments` | Resultat du paiement simule et orchestration transactionnelle du paiement. |

## Decisions appliquees

- `cart` et `payments` sont des applications separees pour correspondre a l'architecture cible.
- Un panier actif et une commande ne portent qu'un seul concert. Cette limite simplifie la couverture de `EM10` et permet d'appliquer clairement le plafond de 6 billets par concert/commande.
- `EF5`, `EF6`, `EF7`, `EF8` et `EF9` sont couverts par les services et par les vues panier, checkout, paiement, confirmation et refus.
- `EF1` et `EF2` sont couvertes par les vues publiques et leurs tests d'integration.
- Les pages de confirmation et refus de paiement filtrent les commandes par utilisateur. Cette protection apporte une couverture partielle de `RG8` sans constituer l'historique de commandes complet de `EF10`.
- Les fiches brouillon ne sont pas publiees. Les concerts annules, passes, termines ou complets restent consultables avec une explication francaise et sans action de reservation.
- Le role administrateur repose pour l'instant sur l'admin Django et les champs `is_staff` / `is_superuser`. Cette fondation ne revendique pas la couverture de `EM9`, car les permissions de gestion des concerts restent hors de cette etape.

## Non fait dans cette etape

- Pas d'historique de commandes dans `Mon espace`.
- Pas de test de cloisonnement d'historique de commandes complet (`RG8`) ; seuls les acces aux pages resultat de paiement sont filtres par proprietaire.
