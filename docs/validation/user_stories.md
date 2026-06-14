# User stories

Les stories ci-dessous servent a organiser les tests et l'implementation. La preuve detaillee reste dans `docs/validation/matrice_tracabilite.md`.

| ID | Acteur | Story | Exigences liees |
| --- | --- | --- | --- |
| US1 | Visiteur | En tant que visiteur, je veux voir les concerts ouverts afin de choisir un evenement. | EF1, RG1 |
| US2 | Visiteur | En tant que visiteur, je veux consulter le detail d'un concert afin de connaitre date, lieu, prix et disponibilites. | EF2 |
| US3 | Visiteur | En tant que visiteur, je veux creer un compte afin de reserver des billets. | EF3, EM8, ENF3 |
| US4 | Client | En tant que client, je veux me connecter et me deconnecter afin d'acceder a mon espace personnel. | EF4, ENF4 |
| US5 | Client | En tant que client, je veux ajouter une quantite valide de billets au panier afin de preparer mon achat. | EF5, EF6, EM1, EM2, EM3, RG2, RG3 |
| US6 | Client | En tant que client, je veux payer mon panier avec un paiement simule afin de finaliser ma commande. | EF7, EF8, EF9, EM6, RG4, RG5 |
| US7 | Client | En tant que client, je veux consulter mes commandes passees afin de retrouver mes billets. | EF10, RG8 |
| US8 | Administrateur | En tant qu'administrateur, je veux gerer les concerts et consulter les ventes afin de controler la billetterie. | EF11, EM9, RG7 |
| US9 | Systeme | En tant que systeme, je veux decrementer le stock seulement apres paiement accepte afin d'eviter la survendue. | EF12, EM1, EM6, RG5 |
| US10 | Client | En tant que client, je veux recevoir un message clair en cas de saisie ou paiement invalide afin de comprendre l'erreur. | EF9, ENF4 |

## Couverture actuelle

- `US3` est couverte pour l'inscription avec email unique, rejet d'un doublon et mot de passe hache.
- `US4` est couverte pour connexion, deconnexion POST et acces protege a `Mon espace`.
- `US1` et `US2` sont couvertes par le catalogue public et les fiches detaillees.
- `US5`, `US6`, `US9` et `US10` sont couvertes par le parcours panier/checkout/paiement simule et les tests domaine/integration.
- `US7` est couverte pour l'historique des commandes payees et le detail de commande filtres par proprietaire (`EF10`, `RG8`).
- `US8` est couverte par l'admin Django enrichi, la synthese admin des ventes, les actions d'annulation/cloture et les tests de permissions. Le suivi admin des ventes est distinct de `RG8`, qui reste l'isolation des commandes des utilisateurs standards.
