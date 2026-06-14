# Matrice de tracabilite

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Etat de couverture actuel

Le depot contient une fondation Django, un catalogue public de concerts, des fiches detaillees, le modele utilisateur email, les pages d'inscription/connexion/deconnexion/espace personnel, le parcours panier/checkout/paiement simule, l'historique des commandes payees, le detail de commande filtre par proprietaire, une administration concerts/ventes protegee par permissions, le noyau domaine de billetterie, des services testables, Ruff, coverage, GitHub Actions et une configuration SonarCloud.

- `EF1` et `EF2` sont couvertes par les vues publiques et les tests d'integration ;
- `EF3`, `EF4`, `EM8`, `ENF3` et `ENF4` sont couverts pour le perimetre compte utilisateur et authentification ;
- `EF5`, `EF6`, `EF7`, `EF8` et `EF9` sont couvertes par les services et les vues Django ;
- `EF10` et `RG8` sont couverts par l'historique paye et les pages detail filtrees par proprietaire ;
- `EF11`, `EM9` et `RG7` sont couverts par l'admin Django enrichi, les vues d'administration protegees par permissions et les tests d'integration ;
- les confirmations affichees, le message explicite de refus, les pages panier/paiement et le parcours checkout sont couverts par tests d'integration ;
- `EF12`, `EM1` a `EM7`, `EM10`, `RG1` a `RG5` sont couverts par les modeles/services et tests domaine ;
- `RG6` est couvert par les vues de checkout et paiement protegees ;
- `EF8`, `EF9`, `EM6`, `EM7`, `EM10`, `RG4` et `RG5` sont maintenus ou etendus par les tests de navigation et d'affichage, mais leur comportement coeur etait deja implemente par le parcours checkout/paiement ;
- le suivi admin des ventes est une fonctionnalite privilegiee et ne change pas la portee de `RG8`, qui reste l'isolation des commandes des utilisateurs standards.

## Exigences fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| EF1 | `concerts.views.ConcertListView`, route `/concerts/`, template `concerts/concert_list.html` | `tests/test_concert_views.py::test_concert_list_returns_200_and_only_displays_bookable_concerts`, `test_concert_list_displays_a_clear_empty_state` | Couvert | La liste publique masque volontairement tous les concerts non reservables |
| EF2 | `concerts.views.ConcertDetailView`, route `/concerts/<id>/`, template `concerts/concert_detail.html` | `tests/test_concert_views.py::test_concert_detail_displays_required_information`, tests des etats non reservables et des reponses `404` | Couvert | Les brouillons ne sont pas publies |
| EF3 | `accounts.User`, `accounts.forms.RegistrationForm`, `accounts.views.SignUpView` | `tests/test_accounts.py`, `tests/test_authentication_views.py::test_account_creation_succeeds_with_unique_email`, `test_duplicate_email_registration_is_rejected_with_french_message`, `test_registered_password_is_not_stored_in_plain_text` | Couvert | Pas de verification email ni profil avance, hors scope |
| EF4 | `accounts.views.LoginView`, `LogoutView`, `PersonalAreaView`, navigation auth | `tests/test_authentication_views.py::test_login_succeeds_with_valid_credentials`, `test_login_fails_with_invalid_credentials`, `test_logout_clears_session_through_post_logout_view`, `test_personal_area_requires_authentication`, `test_authenticated_user_can_access_personal_area`, `test_navigation_uses_post_logout_form_for_authenticated_user` | Couvert | `Mon espace` ne contient pas encore l'historique |
| EF5 | `cart.forms.AddTicketForm`, `cart.views.AddTicketToCartView`, `cart.services.add_ticket_to_cart`, fiche concert authentifiee | `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries`, `test_insufficient_stock_is_rejected_through_add_to_cart_flow`, `test_past_concert_is_rejected_through_add_to_cart_flow`, `test_cancelled_concert_is_rejected_through_add_to_cart_flow`, `test_closed_concert_is_rejected_through_add_to_cart_flow`, tests domaine existants | Couvert | Panier limite volontairement a un seul concert |
| EF6 | `Cart.total_amount`, `templates/cart/detail.html`, `templates/cart/checkout.html` | `tests/test_booking_flow.py::test_cart_display_calculates_total`, `test_cart_total_amount_uses_current_category_prices` | Couvert | Total calcule sur les prix courants du panier avant paiement |
| EF7 | `payments.forms.SimulatedPaymentForm`, `payments.views.SimulatedPaymentView`, `payments.services.process_simulated_card_payment` | `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `test_refused_payment_does_not_create_validated_order_or_decrement_stock` | Couvert | Paiement simule deterministe, sans prestataire reel |
| EF8 | Creation d'une commande `paid`, paiement `accepted`, page `payments/confirmation.html`, lien vers detail/historique | `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `tests/test_order_history.py::test_paid_order_appears_in_history_after_successful_payment`, test domaine accepte | Couvert | Aucun email de confirmation, hors scope |
| EF9 | Creation d'une commande `refused`, stock inchange, page `payments/refused.html`, exclusion de l'historique paye | `tests/test_booking_flow.py::test_refused_payment_does_not_create_validated_order_or_decrement_stock`, `tests/test_order_history.py::test_refused_orders_remain_non_final_and_are_excluded_from_history`, test domaine refuse | Couvert | Une commande refusee non finale est tracee |
| EF10 | `orders.views.OrderListView`, route `/commandes/`, template `orders/list.html`, historique des commandes payees du client connecte | `tests/test_order_history.py::test_user_sees_only_their_own_paid_orders`, `test_anonymous_order_history_and_detail_access_redirect_to_login`, `test_paid_order_appears_in_history_after_successful_payment` | Couvert | Historique limite aux commandes payees ; tentatives refusees exclues |
| EF11 | `concerts.admin.ConcertAdmin`, `concerts.services.cancel_concert`, `close_concert_sales`, routes `/concerts/administration/ventes/` et actions POST admin | `tests/test_admin_concert_management.py::test_django_admin_can_create_and_modify_concert_with_category`, `test_cancel_action_permission_rules`, `test_cancelled_concert_rejects_new_reservations_and_preserves_paid_order`, `test_closed_concert_rejects_new_reservations_and_keeps_stock`, `test_sales_overview_counts_paid_sales_only` | Couvert | Pas de workflow Playwright admin |
| EF12 | Decrement stock apres paiement accepte dans `process_simulated_payment` | Tests domaine et `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert | Concurrence avancee a completer en integration |

## Exigences metier

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| EM1 | Validation stock + decrement transactionnel + contrainte stock non negatif + rejet UI stock insuffisant | Tests domaine, `tests/test_booking_flow.py::test_insufficient_stock_is_rejected_through_add_to_cart_flow`, `test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert | Tests de concurrence multi-processus futurs |
| EM2 | Quantite minimale 1 et panier non vide | Tests domaine et `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries` | Couvert |  |
| EM3 | Maximum 6 billets agrege par concert/commande | Tests domaine et `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries` | Couvert | Panier limite a un concert |
| EM4 | Concert passe refuse par le domaine, masque du catalogue, explique sur sa fiche et rejete a l'ajout panier | Tests domaine, `tests/test_concert_views.py::test_past_concert_detail_explains_unavailability_without_cta`, `tests/test_booking_flow.py::test_past_concert_is_rejected_through_add_to_cart_flow` | Couvert | Transition automatique vers le statut termine non implementee |
| EM5 | Concert annule refuse par le domaine, masque du catalogue, explique sur sa fiche et rejete a l'ajout panier | Tests domaine, `tests/test_admin_concert_management.py::test_cancelled_concert_rejects_new_reservations_and_preserves_paid_order`, `tests/test_concert_views.py::test_cancelled_concert_detail_explains_unavailability_without_cta`, `tests/test_booking_flow.py::test_cancelled_concert_is_rejected_through_add_to_cart_flow` | Couvert |  |
| EM6 | Commande finale seulement si paiement accepte ; commandes refusees exclues de l'historique paye | Tests domaine, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `test_refused_payment_does_not_create_validated_order_or_decrement_stock`, `tests/test_order_history.py::test_refused_orders_remain_non_final_and_are_excluded_from_history` | Couvert |  |
| EM7 | Prix snapshot au paiement et affiche dans le detail de commande | `test_price_snapshot_is_kept_after_category_price_changes`, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `tests/test_order_history.py::test_order_detail_displays_consistent_paid_order_data` | Couvert | Promotions/remises hors scope |
| EM8 | `accounts.User.email` unique et rejet formulaire des doublons email | `tests/test_accounts.py::test_user_email_must_be_unique`, `tests/test_authentication_views.py::test_duplicate_email_registration_is_rejected_with_french_message` | Couvert | Unicite renforcee cote formulaire pour les variantes de casse |
| EM9 | Vues admin avec `PermissionRequiredMixin`, permissions `concerts.view_concert`, `orders.view_order`, `concerts.change_concert`, admin Django reserve aux administrateurs | `tests/test_admin_concert_management.py::test_sales_overview_permission_rules`, `test_cancel_action_permission_rules`, `test_django_admin_can_create_and_modify_concert_with_category`, tests role utilisateur standard existants | Couvert | Les permissions fines sont limitees au perimetre concerts/ventes demande |
| EM10 | `Order` lie a utilisateur, concert, date, statut ; donnees affichees dans l'historique et le detail | `test_accepted_payment_creates_paid_order_and_decrements_stock`, `tests/test_order_history.py::test_order_detail_displays_consistent_paid_order_data` | Couvert |  |

## Exigences non fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| ENF1 | Acces direct accueil → catalogue → fiche → panier → checkout → paiement → commandes | `tests/test_homepage.py`, tests concert, `tests/test_booking_flow.py`, `tests/test_order_history.py::test_paid_order_appears_in_history_after_successful_payment` | Partiel | Parcours e2e Playwright futur |
| ENF2 | Aucune mesure performance applicative | Aucun | Non couvert | A mesurer avec vues |
| ENF3 | Mot de passe gere par Django auth et formulaire d'inscription Django | `tests/test_accounts.py::test_user_password_is_hashed`, `tests/test_authentication_views.py::test_registered_password_is_not_stored_in_plain_text` | Couvert | Aucun stockage en clair attendu |
| ENF4 | Services et formulaires rejettent les saisies invalides proprement | Tests quantite/stock/statut domaine, tests authentification, `tests/test_booking_flow.py` | Couvert pour le perimetre implemente |  |
| ENF5 | Ruff configure dans `pyproject.toml` et CI | `ruff check .` local et CI | Couvert fondation | Suivi Sonar futur |
| ENF6 | Regles metier isolees en services testables, dont `concerts.services` pour administration et ventes | `tests/test_core_domain.py`, `tests/test_admin_concert_management.py`, `pytest` | Couvert | A maintenir avec les vues |
| ENF7 | Workflow GitHub Actions versionne | `.github/workflows/ci.yml` | Couvert fondation | CI distante a verifier apres push |

## Regles de gestion

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| RG1 | `Concert.is_bookable`, validation service, catalogue, fiche et ajout panier | Tests domaine, `tests/test_concert_views.py`, `tests/test_booking_flow.py`, tests statut `closed` | Couvert domaine et interface | Reservation effective limitee au panier mono-concert |
| RG2 | `validate_category_stock`, formulaire et ajout panier | Tests domaine, `tests/test_booking_flow.py::test_insufficient_stock_is_rejected_through_add_to_cart_flow` | Couvert |  |
| RG3 | `validate_ticket_quantity`, contraintes lignes, `AddTicketForm` | Tests domaine, `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries` | Couvert |  |
| RG4 | Paiement refuse cree commande non finale, affiche refus, stock inchange, historique paye inchange | Tests domaine, `tests/test_booking_flow.py::test_refused_payment_does_not_create_validated_order_or_decrement_stock`, `tests/test_order_history.py::test_refused_orders_remain_non_final_and_are_excluded_from_history` | Couvert |  |
| RG5 | Paiement accepte cree commande payee, affiche confirmation, decremente stock et rend la commande visible dans l'historique | Tests domaine, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `tests/test_order_history.py::test_paid_order_appears_in_history_after_successful_payment` | Couvert |  |
| RG6 | `LoginRequiredMixin` sur checkout et paiement | `tests/test_booking_flow.py::test_anonymous_user_cannot_access_checkout_or_payment` | Couvert |  |
| RG7 | Annulation admin via `cancel_concert`, statut `cancelled` non reservable, fiche sans CTA, commandes payees conservees | `tests/test_admin_concert_management.py::test_cancel_action_permission_rules`, `test_cancelled_concert_rejects_new_reservations_and_preserves_paid_order`, `tests/test_concert_views.py::test_cancelled_concert_detail_explains_unavailability_without_cta`, `tests/test_booking_flow.py::test_cancelled_concert_is_rejected_through_add_to_cart_flow` | Couvert |  |
| RG8 | Pages panier/checkout personnelles, pages resultat, historique paye et detail de commande filtres par utilisateur standard | `tests/test_booking_flow.py::test_user_cannot_access_another_users_cart_checkout_or_order_pages`, `tests/test_order_history.py::test_user_sees_only_their_own_paid_orders`, `test_user_cannot_access_another_users_paid_order_detail`, `test_anonymous_order_history_and_detail_access_redirect_to_login` | Couvert | Historique limite aux commandes payees ; le suivi admin des ventes est hors RG8 |

## Regle de mise a jour

Chaque nouvelle implementation doit ajouter une preuve dans cette matrice :

- fichier ou module d'implementation ;
- fichier de test ;
- statut de couverture ;
- limite connue si la couverture est partielle.
