# Scénarios fonctionnels automatisés

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## SF1 - Parcours nominal de réservation

Test :
`e2e/test_nominal_booking_flow.py::test_nominal_booking_flow_accepted_payment_appears_in_history`

Exigences couvertes :

- `EF1`, `EF2`, `EF4`, `EF5`, `EF6`, `EF7`, `EF8`, `EF10`, `EF12` ;
- `EM1`, `EM2`, `EM3`, `EM6`, `EM7`, `EM10` ;
- `ENF1`, `ENF6`, `ENF7` ;
- `RG1`, `RG2`, `RG3`, `RG5`.

### Préconditions

- Le test utilise `pytest-django`, `transactional_db` et `live_server`.
- Les fixtures créent un client, un concert futur ouvert et deux catégories.
- Le test ne dépend ni de `db.sqlite3`, ni de `seed_demo_data`, ni d'un compte
  créé manuellement.

### Déroulement

1. Ouvrir la liste des concerts puis la fiche du concert de test.
2. Suivre le lien de connexion avec retour vers la fiche.
3. Se connecter, sélectionner la catégorie `Fosse` et ajouter deux billets.
4. Vérifier le panier et son total de 80,00 €.
5. Valider le panier et ouvrir le paiement simulé.
6. Saisir la carte acceptée `4242424242424242`.
7. Vérifier la confirmation puis l'historique des commandes.

### Résultats attendus

- Une commande `paid` est créée pour le client et le concert.
- Le prix de 40,00 € est figé dans la ligne de commande.
- Le stock de la catégorie passe de 8 à 6.
- Le panier passe à `checked_out`.
- La commande apparaît dans `Mes commandes`.

## SF2 - Quantité invalide et message français

Test :
`e2e/test_nominal_booking_flow.py::test_invalid_quantity_displays_french_server_validation`

Exigences couvertes : `ENF4`, `RG3`.

### Déroulement

1. Se connecter et revenir sur une fiche réservable.
2. Vérifier que le formulaire possède `novalidate`.
3. Vérifier que le champ de quantité conserve `required`, `type="number"`,
   `min="1"` et `max="6"`.
4. Saisir `7` et soumettre le formulaire.

### Résultats attendus

- Django refuse la saisie.
- Le message `La quantité ne peut pas dépasser 6 billets.` est visible.
- Aucune ligne de panier n'est créée.

## Limites

Le paiement refusé, l'absence d'authentification, le stock insuffisant et les
autres bornes de quantité restent couverts par les tests d'intégration Django.
Le parcours administrateur est couvert par les tests d'intégration et par une
vérification navigateur manuelle, mais pas par un scénario Playwright dédié.
