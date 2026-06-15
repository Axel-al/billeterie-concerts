# Applications Django

## État actuel

Le dépôt contient cinq applications Django métier :

| Application | État actuel | Exigences liées |
| --- | --- | --- |
| `accounts` | Modèle `User` personnalisé avec e-mail unique, manager, admin Django, inscription, connexion, déconnexion POST et espace personnel protégé. | EF3, EF4, EM8, ENF3, ENF4 |
| `concerts` | Modèles `Concert` et `SeatCategory`, catalogue public, fiches détaillées, services et vues d'administration, admin avec catégories inline, commande `seed_demo_data`. | EF1, EF2, EF5 partiel, EF11, EF12, EM1, EM4, EM5, EM9, RG1, RG2, RG7 |
| `cart` | Modèles `Cart` et `CartLine`, services d'ajout/validation de panier, vues panier et checkout. | EF5, EF6, EM1, EM2, EM3, RG2, RG3, RG6 |
| `orders` | Modèles `Order` et `OrderLine`, statuts, prix snapshots, historique payé et détail de commande filtrés par utilisateur. | EF8, EF9, EF10, EM6, EM7, EM10, RG4, RG5, RG8 |
| `payments` | Modèle `Payment`, règle de carte simulée, service de paiement et vues paiement/confirmation/refus. | EF7, EF8, EF9, EF12, EM6, RG4, RG5, RG6 |

Le module `config` porte les réglages, les URLs racines, le rendu de la page d'accueil et les redirections d'authentification. Le catalogue est disponible sur `/concerts/`, les fiches sur `/concerts/<id>/`, le suivi admin des ventes sur `/concerts/administration/ventes/`, le panier sur `/panier/`, le checkout sur `/panier/validation/`, le paiement simulé sur `/paiement/` et les commandes payées sur `/commandes/`.

## Découpage retenu

| Application | Responsabilité |
| --- | --- |
| `accounts` | Identité utilisateur, inscription, authentification et espace personnel de base. |
| `concerts` | Données de concerts, catégories de places, stock, statut de réservation, consultation publique et gestion admin des concerts/ventes. |
| `cart` | Panier actif utilisateur, lignes de panier, quantités et total courant. |
| `orders` | Commandes issues d'une tentative de paiement, lignes figeant prix et catégorie, consultation des commandes payées. |
| `payments` | Résultat du paiement simulé et orchestration transactionnelle du paiement. |

## Décisions appliquées

- `cart` et `payments` sont des applications séparées pour correspondre à l'architecture cible.
- Un panier actif et une commande ne portent qu'un seul concert. Cette limite simplifie la couverture de `EM10` et permet d'appliquer clairement le plafond de 6 billets par concert/commande.
- `EF5`, `EF6`, `EF7`, `EF8` et `EF9` sont couverts par les services et par les vues panier, checkout, paiement, confirmation et refus.
- `EF1` et `EF2` sont couvertes par les vues publiques et leurs tests d'intégration.
- `EF11`, `EM9` et `RG7` sont couverts par les permissions Django, la synthèse admin des ventes et les actions d'annulation/clôture.
- Les pages de confirmation et refus de paiement filtrent les commandes par utilisateur.
- L'historique `Mes commandes` et le détail de commande filtrent les commandes payées par utilisateur. `EF10` et `RG8` sont couverts par ce périmètre.
- Les commandes refusées restent tracées comme non finales, mais elles sont exclues de l'historique des achats payés.
- Les fiches brouillon ne sont pas publiées. Les concerts annulés, clôturés, passés, terminés ou complets restent consultables avec une explication française et sans action de réservation.
- Les vues d'administration utilisent explicitement les permissions Django : `concerts.view_concert` et `orders.view_order` pour le suivi des ventes, `concerts.change_concert` pour annuler ou clôturer.

## Non fait dans cette étape

- Pas d'historique des tentatives refusées dans `Mes commandes` : elles restent consultables uniquement via la page de refus filtrée par propriétaire.
