# Applications Django

## `accounts`

Responsabilités :

- modèle `User` personnalisé avec e-mail unique ;
- manager de création des utilisateurs et superutilisateurs ;
- inscription, connexion, déconnexion POST et espace personnel ;
- administration des utilisateurs.

Exigences principales : `EF3`, `EF4`, `EM8`, `ENF3`, `ENF4`.

## `concerts`

Responsabilités :

- modèles `Concert` et `SeatCategory` ;
- catalogue public et fiches détaillées ;
- calcul de réservabilité selon date, statut et stock ;
- synthèse administrateur des ventes ;
- annulation et clôture ;
- commande `seed_demo_data`.

Exigences principales : `EF1`, `EF2`, `EF11`, `EF12`, `EM1`, `EM4`,
`EM5`, `EM9`, `RG1`, `RG2`, `RG7`.

## `cart`

Responsabilités :

- modèles `Cart` et `CartLine` ;
- panier actif unique par utilisateur ;
- limite mono-concert ;
- quantité agrégée de 1 à 6 ;
- ajout, total et validation du checkout.

Exigences principales : `EF5`, `EF6`, `EM1`, `EM2`, `EM3`, `RG2`,
`RG3`, `RG6`.

## `orders`

Responsabilités :

- modèles `Order` et `OrderLine` ;
- prix et nom de catégorie figés au paiement ;
- historique des commandes payées ;
- détail filtré par propriétaire ;
- surfaces administrateur en lecture seule pour les données métier.

Exigences principales : `EF8`, `EF9`, `EF10`, `EM6`, `EM7`, `EM10`,
`RG4`, `RG5`, `RG8`.

## `payments`

Responsabilités :

- modèle `Payment` ;
- formulaire de carte simulée ;
- acceptation de `4242424242424242` et refus des autres valeurs ;
- transaction de création de commande et décrément du stock ;
- pages de confirmation et refus filtrées par utilisateur.

Exigences principales : `EF7`, `EF8`, `EF9`, `EF12`, `EM6`, `RG4`,
`RG5`, `RG6`.

## `config`

Responsabilités :

- configuration par variables d'environnement ;
- déclaration des applications ;
- routes racines ;
- langue `fr-fr` et fuseau `Europe/Paris` ;
- titres français de l'administration Django ;
- points d'entrée ASGI et WSGI.

## Découpage

Le découpage maintient les règles sensibles dans des services proches du
domaine. Il évite un contrôleur unique pour le panier, le paiement et les
commandes, tout en conservant un déploiement monolithique simple.
