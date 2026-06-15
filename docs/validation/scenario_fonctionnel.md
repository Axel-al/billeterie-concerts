# Scénario fonctionnel automatisé

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## SF1 - Parcours nominal de réservation

Test automatisé : `e2e/test_nominal_booking_flow.py::test_nominal_booking_flow_accepted_payment_appears_in_history`

Exigences couvertes :

- `EF1`, `EF2`, `EF4`, `EF5`, `EF6`, `EF7`, `EF8`, `EF10`, `EF12`
- `EM1`, `EM2`, `EM3`, `EM6`, `EM7`, `EM10`
- `ENF1`, `ENF6`, `ENF7`
- `RG1`, `RG2`, `RG3`, `RG5`

## Préconditions

- Le test utilise `pytest-django`, `transactional_db` et `live_server`.
- Les données sont créées dans la base de test : utilisateur client, concert futur ouvert, catégorie `Fosse` avec 8 places et catégorie `Balcon` avec 4 places.
- Le test ne dépend pas de `db.sqlite3`, de la commande `seed_demo_data` ni d'un état manuel local.

## Déroulement

1. Le visiteur ouvre la liste des concerts.
2. Il ouvre la fiche du concert ouvert créé par fixture.
3. Il utilise le lien de connexion de la fiche réservable.
4. Il se connecte avec le compte créé par fixture.
5. Il sélectionne la catégorie `Fosse`.
6. Il saisit une quantité valide de 2 billets.
7. Il ajoute les billets au panier.
8. Il vérifie le panier et son total de 80,00 EUR.
9. Il lance la validation du panier.
10. Il passe au paiement simulé.
11. Il paie avec la carte acceptée `4242424242424242`.
12. Il voit la confirmation de commande.
13. Il ouvre `Mes commandes`.
14. Il vérifie que la commande payée apparaît dans l'historique.

## Résultats attendus

- La commande est au statut `paid`.
- La quantité totale commandée est 2.
- Le total payé est 80,00 EUR.
- Le prix snapshot de la catégorie est 40,00 EUR.
- Le stock restant de la catégorie `Fosse` passe de 8 à 6.
- L'historique affiche uniquement la commande payée du client connecté.

## Limites

Les parcours paiement refusé, quantité invalide et redirection d'un visiteur anonyme vers la connexion restent couverts par les tests d'intégration Django. Ils ne sont pas ajoutés au premier scénario Playwright pour garder le test e2e court et stable.
