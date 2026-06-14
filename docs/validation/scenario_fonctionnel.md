# Scenario fonctionnel automatise

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## SF1 - Parcours nominal de reservation

Test automatise : `e2e/test_nominal_booking_flow.py::test_nominal_booking_flow_accepted_payment_appears_in_history`

Exigences couvertes :

- `EF1`, `EF2`, `EF4`, `EF5`, `EF6`, `EF7`, `EF8`, `EF10`, `EF12`
- `EM1`, `EM2`, `EM3`, `EM6`, `EM7`, `EM10`
- `ENF1`, `ENF6`, `ENF7`
- `RG1`, `RG2`, `RG3`, `RG5`

## Preconditions

- Le test utilise `pytest-django`, `transactional_db` et `live_server`.
- Les donnees sont creees dans la base de test : utilisateur client, concert futur ouvert, categorie `Fosse` avec 8 places et categorie `Balcon` avec 4 places.
- Le test ne depend pas de `db.sqlite3`, de la commande `seed_demo_data` ni d'un etat manuel local.

## Deroulement

1. Le visiteur ouvre la liste des concerts.
2. Il ouvre la fiche du concert ouvert cree par fixture.
3. Il utilise le lien de connexion de la fiche reservable.
4. Il se connecte avec le compte cree par fixture.
5. Il selectionne la categorie `Fosse`.
6. Il saisit une quantite valide de 2 billets.
7. Il ajoute les billets au panier.
8. Il verifie le panier et son total de 80,00 EUR.
9. Il lance la validation du panier.
10. Il passe au paiement simule.
11. Il paie avec la carte acceptee `4242424242424242`.
12. Il voit la confirmation de commande.
13. Il ouvre `Mes commandes`.
14. Il verifie que la commande payee apparait dans l'historique.

## Resultats attendus

- La commande est au statut `paid`.
- La quantite totale commandee est 2.
- Le total paye est 80,00 EUR.
- Le prix snapshot de la categorie est 40,00 EUR.
- Le stock restant de la categorie `Fosse` passe de 8 a 6.
- L'historique affiche uniquement la commande payee du client connecte.

## Limites

Les parcours paiement refuse, quantite invalide et redirection d'un visiteur anonyme vers la connexion restent couverts par les tests d'integration Django. Ils ne sont pas ajoutes au premier scenario Playwright pour garder le test e2e court et stable.
