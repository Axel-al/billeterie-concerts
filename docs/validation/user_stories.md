# User stories

Les stories ci-dessous servent à organiser les tests et l'implémentation. La preuve détaillée reste dans `docs/validation/matrice_tracabilite.md`.

| ID | Acteur | Story | Exigences liées |
| --- | --- | --- | --- |
| US1 | Visiteur | En tant que visiteur, je veux voir les concerts ouverts afin de choisir un événement. | EF1, RG1 |
| US2 | Visiteur | En tant que visiteur, je veux consulter le détail d'un concert afin de connaître la date, le lieu, le prix et les disponibilités. | EF2 |
| US3 | Visiteur | En tant que visiteur, je veux créer un compte afin de réserver des billets. | EF3, EM8, ENF3 |
| US4 | Client | En tant que client, je veux me connecter et me déconnecter afin d'accéder à mon espace personnel. | EF4, ENF4 |
| US5 | Client | En tant que client, je veux ajouter une quantité valide de billets au panier afin de préparer mon achat. | EF5, EF6, EM1, EM2, EM3, RG2, RG3 |
| US6 | Client | En tant que client, je veux payer mon panier avec un paiement simulé afin de finaliser ma commande. | EF7, EF8, EF9, EM6, RG4, RG5 |
| US7 | Client | En tant que client, je veux consulter mes commandes passées afin de retrouver mes billets. | EF10, RG8 |
| US8 | Administrateur | En tant qu'administrateur, je veux gérer les concerts et consulter les ventes afin de contrôler la billetterie. | EF11, EM9, RG7 |
| US9 | Système | En tant que système, je veux décrémenter le stock seulement après paiement accepté afin d'éviter la survendue. | EF12, EM1, EM6, RG5 |
| US10 | Client | En tant que client, je veux recevoir un message clair en cas de saisie ou paiement invalide afin de comprendre l'erreur. | EF9, ENF4 |

## Couverture actuelle

- `US3` est couverte pour l'inscription avec e-mail unique, rejet d'un doublon et mot de passe haché.
- `US4` est couverte pour connexion, déconnexion POST et accès protégé à `Mon espace`.
- `US1` et `US2` sont couvertes par le catalogue public et les fiches détaillées.
- `US5`, `US6`, `US9` et `US10` sont couvertes par le parcours panier/checkout/paiement simulé et les tests domaine/intégration.
- `US7` est couverte pour l'historique des commandes payées et le détail de commande filtrés par propriétaire (`EF10`, `RG8`).
- `US8` est couverte par l'admin Django enrichi, la synthèse admin des ventes, les actions d'annulation/clôture et les tests de permissions. Le suivi admin des ventes est distinct de `RG8`, qui reste l'isolation des commandes des utilisateurs standards.
