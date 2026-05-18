# Matrice de tracabilite

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Etat de couverture actuel

Le depot contient une fondation Django, le modele utilisateur email, les pages d'inscription/connexion/deconnexion/espace personnel, le noyau domaine de billetterie, des services testables, Ruff, coverage, GitHub Actions et une configuration SonarCloud.

- `EF3`, `EF4`, `EM8`, `ENF3` et `ENF4` sont couverts pour le perimetre compte utilisateur et authentification ;
- `EF5`, `EF7`, `EF8` et `EF9` sont couvertes partiellement au niveau domaine/service seulement ;
- aucune couverture n'est revendiquee pour les confirmations affichees, les messages explicites de refus, les pages panier/paiement ou le parcours checkout complet ;
- `EF12`, `EM1` a `EM7`, `EM10`, `RG1` a `RG5` et la partie reservation de `RG7` sont couvertes par les modeles/services et tests domaine ;
- `EF1`, `EF2`, `EF10`, `RG6` et `RG8` restent non couverts par absence de vues et de controle d'acces utilisateur ;
- `EF11` a une fondation via l'admin Django ; `EM9` reste une fondation de role seulement et n'est pas revendiquee comme couverte.

## Exigences fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| EF1 | Aucune vue liste concerts | Aucun | Non couvert | Modeles seulement |
| EF2 | Donnees `Concert`/`SeatCategory` disponibles | Aucun test de fiche | Non couvert | Pas de vue detail |
| EF3 | `accounts.User`, `accounts.forms.RegistrationForm`, `accounts.views.SignUpView` | `tests/test_accounts.py`, `tests/test_authentication_views.py::test_account_creation_succeeds_with_unique_email`, `test_duplicate_email_registration_is_rejected_with_french_message`, `test_registered_password_is_not_stored_in_plain_text` | Couvert | Pas de verification email ni profil avance, hors scope |
| EF4 | `accounts.views.LoginView`, `LogoutView`, `PersonalAreaView`, navigation auth | `tests/test_authentication_views.py::test_login_succeeds_with_valid_credentials`, `test_login_fails_with_invalid_credentials`, `test_logout_clears_session_through_post_logout_view`, `test_personal_area_requires_authentication`, `test_authenticated_user_can_access_personal_area`, `test_navigation_uses_post_logout_form_for_authenticated_user` | Couvert | `Mon espace` ne contient pas encore l'historique |
| EF5 | `cart.services.add_ticket_to_cart`, `Cart`, `CartLine` | `test_aggregate_quantity_six_accepted_across_categories`, `test_aggregate_quantity_seven_rejected_across_categories`, `test_insufficient_stock_rejected`, `test_active_cart_rejects_adding_another_concert` | Partiel domaine/service | Pas de formulaire ni UI panier |
| EF6 | `Cart.total_amount` | `test_cart_total_amount_uses_current_category_prices` | Partiel domaine | Pas d'affichage panier |
| EF7 | `payments.services.process_simulated_payment` | `test_accepted_payment_creates_paid_order_and_decrements_stock`, `test_refused_payment_records_refused_order_and_leaves_stock` | Partiel domaine/service | Pas de page paiement |
| EF8 | Creation d'une commande `paid` et paiement `accepted` | `test_accepted_payment_creates_paid_order_and_decrements_stock` | Partiel domaine/service | Pas de confirmation affichee |
| EF9 | Creation d'une commande `refused` sans stock decremente | `test_refused_payment_records_refused_order_and_leaves_stock` | Partiel domaine/service | Pas de message explicite affiche |
| EF10 | Aucun historique de commandes | Aucun | Non couvert | A implementer |
| EF11 | Admin Django pour concerts et categories | Aucun test permissions admin | Fondation seulement | Suspendre/annuler via UI admin non teste |
| EF12 | Decrement stock apres paiement accepte | `test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert domaine/service | Concurrence avancee a completer en integration |

## Exigences metier

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| EM1 | Validation stock + decrement transactionnel + contrainte stock non negatif | `test_insufficient_stock_rejected`, `test_stock_cannot_become_negative`, `test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert domaine/service | Tests de concurrence multi-processus futurs |
| EM2 | Quantite minimale 1 et panier non vide | `test_quantity_zero_rejected`, `test_quantity_one_accepted`, `test_empty_cart_rejected_for_checkout` | Couvert domaine/service | UI non couverte |
| EM3 | Maximum 6 billets agrege par concert/commande | `test_quantity_six_accepted`, `test_quantity_seven_rejected`, `test_checkout_rejects_preexisting_cart_above_six_tickets` | Couvert domaine/service | Panier limite a un concert |
| EM4 | Concert passe refuse | `test_past_concert_not_bookable` | Couvert domaine/service | UI non couverte |
| EM5 | Concert annule refuse | `test_cancelled_concert_not_bookable` | Couvert domaine/service | Annulation admin non testee |
| EM6 | Commande finale seulement si paiement accepte | `test_accepted_payment_creates_paid_order_and_decrements_stock`, `test_refused_payment_records_refused_order_and_leaves_stock` | Couvert domaine/service | Parcours UI futur |
| EM7 | Prix snapshot au paiement | `test_price_snapshot_is_kept_after_category_price_changes` | Couvert domaine/service | Promotions/remises hors scope |
| EM8 | `accounts.User.email` unique et rejet formulaire des doublons email | `tests/test_accounts.py::test_user_email_must_be_unique`, `tests/test_authentication_views.py::test_duplicate_email_registration_is_rejected_with_french_message` | Couvert | Unicite renforcee cote formulaire pour les variantes de casse |
| EM9 | Admin Django base sur `is_staff`/`is_superuser` | `tests/test_accounts.py::test_superuser_defaults_to_staff_and_superuser_flags`, `tests/test_authentication_views.py::test_registered_standard_user_has_no_admin_privileges` | Non couvert, fondation role seulement | Permissions concert admin hors scope |
| EM10 | `Order` lie a utilisateur, concert, date, statut | `test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert domaine/service | Historique utilisateur futur |

## Exigences non fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| ENF1 | Page d'accueil minimale seulement | Aucun | Non couvert | Actions metier non exposees |
| ENF2 | Aucune mesure performance applicative | Aucun | Non couvert | A mesurer avec vues |
| ENF3 | Mot de passe gere par Django auth et formulaire d'inscription Django | `tests/test_accounts.py::test_user_password_is_hashed`, `tests/test_authentication_views.py::test_registered_password_is_not_stored_in_plain_text` | Couvert | Aucun stockage en clair attendu |
| ENF4 | Services rejettent les saisies invalides par `ValidationError`; formulaire inscription et connexion affichent des labels et erreurs en francais | `test_quantity_zero_rejected`, `test_quantity_seven_rejected`, `test_non_integer_quantity_rejected`, `test_invalid_simulated_payment_result_rejected`, tests stock/statut, `tests/test_authentication_views.py::test_authentication_pages_use_french_labels`, `test_duplicate_email_registration_is_rejected_with_french_message`, `test_login_fails_with_invalid_credentials` | Couvert pour le perimetre implemente | Messages paiement/UI panier futurs |
| ENF5 | Ruff configure dans `pyproject.toml` et CI | `ruff check .` local et CI | Couvert fondation | Suivi Sonar futur |
| ENF6 | Regles metier isolees en services testables | `tests/test_core_domain.py`, `pytest` | Couvert | A maintenir avec les vues |
| ENF7 | Workflow GitHub Actions versionne | `.github/workflows/ci.yml` | Couvert fondation | CI distante a verifier apres push |

## Regles de gestion

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| RG1 | `Concert.is_bookable` et validation service | `test_future_open_concert_with_stock_is_bookable`, `test_past_concert_not_bookable`, `test_cancelled_concert_not_bookable`, `test_draft_concert_not_bookable`, `test_future_open_concert_without_stock_not_bookable` | Couvert domaine/service | Liste concerts future |
| RG2 | `validate_category_stock` | `test_insufficient_stock_rejected`, `test_exact_stock_accepted` | Couvert domaine/service | UI future |
| RG3 | `validate_ticket_quantity`, contraintes lignes | `test_quantity_zero_rejected`, `test_quantity_one_accepted`, `test_quantity_six_accepted`, `test_quantity_seven_rejected`, `test_non_integer_quantity_rejected` | Couvert domaine/service | Champs formulaire futurs |
| RG4 | Paiement refuse cree commande non finale et stock inchange | `test_refused_payment_records_refused_order_and_leaves_stock` | Couvert domaine/service | Message UI futur |
| RG5 | Paiement accepte cree commande payee et decremente stock | `test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert domaine/service | Confirmation UI future |
| RG6 | Aucun controle d'acces paiement cote vue | Aucun | Non couvert | A implementer avec checkout UI |
| RG7 | Concert annule non reservable | `test_cancelled_concert_not_bookable` | Partiel domaine/service | Action admin d'annulation non testee |
| RG8 | Aucun historique de commandes | Aucun | Non couvert | A implementer |

## Regle de mise a jour

Chaque nouvelle implementation doit ajouter une preuve dans cette matrice :

- fichier ou module d'implementation ;
- fichier de test ;
- statut de couverture ;
- limite connue si la couverture est partielle.
