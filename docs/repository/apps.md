# Applications Django

## Etat actuel

Le depot contient cinq applications Django metier :

| Application | Etat actuel | Exigences liees |
| --- | --- | --- |
| `accounts` | Modele `User` personnalise avec email unique, manager, admin Django, inscription, connexion, deconnexion POST et espace personnel protege. | EF3, EF4, EM8, ENF3, ENF4 |
| `concerts` | Modeles `Concert` et `SeatCategory`, catalogue public, fiches detaillees, services et vues d'administration, admin avec categories inline, commande `seed_demo_data`. | EF1, EF2, EF5 partiel, EF11, EF12, EM1, EM4, EM5, EM9, RG1, RG2, RG7 |
| `cart` | Modeles `Cart` et `CartLine`, services d'ajout/validation de panier, vues panier et checkout. | EF5, EF6, EM1, EM2, EM3, RG2, RG3, RG6 |
| `orders` | Modeles `Order` et `OrderLine`, statuts, prix snapshots, historique paye et detail de commande filtres par utilisateur. | EF8, EF9, EF10, EM6, EM7, EM10, RG4, RG5, RG8 |
| `payments` | Modele `Payment`, regle de carte simulee, service de paiement et vues paiement/confirmation/refus. | EF7, EF8, EF9, EF12, EM6, RG4, RG5, RG6 |

Le module `config` porte les reglages, les URLs racines, le rendu de la page d'accueil et les redirections d'authentification. Le catalogue est disponible sur `/concerts/`, les fiches sur `/concerts/<id>/`, le suivi admin des ventes sur `/concerts/administration/ventes/`, le panier sur `/panier/`, le checkout sur `/panier/validation/`, le paiement simule sur `/paiement/` et les commandes payees sur `/commandes/`.

## Decoupage retenu

| Application | Responsabilite |
| --- | --- |
| `accounts` | Identite utilisateur, inscription, authentification et espace personnel de base. |
| `concerts` | Donnees de concerts, categories de places, stock, statut de reservation, consultation publique et gestion admin des concerts/ventes. |
| `cart` | Panier actif utilisateur, lignes de panier, quantites et total courant. |
| `orders` | Commandes issues d'une tentative de paiement, lignes figeant prix et categorie, consultation des commandes payees. |
| `payments` | Resultat du paiement simule et orchestration transactionnelle du paiement. |

## Decisions appliquees

- `cart` et `payments` sont des applications separees pour correspondre a l'architecture cible.
- Un panier actif et une commande ne portent qu'un seul concert. Cette limite simplifie la couverture de `EM10` et permet d'appliquer clairement le plafond de 6 billets par concert/commande.
- `EF5`, `EF6`, `EF7`, `EF8` et `EF9` sont couverts par les services et par les vues panier, checkout, paiement, confirmation et refus.
- `EF1` et `EF2` sont couvertes par les vues publiques et leurs tests d'integration.
- `EF11`, `EM9` et `RG7` sont couverts par les permissions Django, la synthese admin des ventes et les actions d'annulation/cloture.
- Les pages de confirmation et refus de paiement filtrent les commandes par utilisateur.
- L'historique `Mes commandes` et le detail de commande filtrent les commandes payees par utilisateur. `EF10` et `RG8` sont couverts par ce perimetre.
- Les commandes refusees restent tracees comme non finales, mais elles sont exclues de l'historique des achats payes.
- Les fiches brouillon ne sont pas publiees. Les concerts annules, clotures, passes, termines ou complets restent consultables avec une explication francaise et sans action de reservation.
- Les vues d'administration utilisent explicitement les permissions Django : `concerts.view_concert` et `orders.view_order` pour le suivi des ventes, `concerts.change_concert` pour annuler ou cloturer.

## Non fait dans cette etape

- Pas d'historique des tentatives refusees dans `Mes commandes` : elles restent consultables uniquement via la page de refus filtree par proprietaire.
