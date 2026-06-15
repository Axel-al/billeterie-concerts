# Matrice de traçabilité

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## État de couverture actuel

Le dépôt contient une fondation Django, un catalogue public de concerts, des fiches détaillées, le modèle utilisateur e-mail, les pages d'inscription/connexion/déconnexion/espace personnel, le parcours panier/checkout/paiement simulé, l'historique des commandes payées, le détail de commande filtré par propriétaire, une administration concerts/ventes protégée par permissions, le noyau domaine de billetterie, des services testables, Ruff, coverage, GitHub Actions et une configuration SonarCloud.

- `EF1` et `EF2` sont couvertes par les vues publiques et les tests d'intégration ;
- `EF3`, `EF4`, `EM8`, `ENF3` et `ENF4` sont couverts pour le périmètre compte utilisateur et authentification ;
- `EF5`, `EF6`, `EF7`, `EF8` et `EF9` sont couvertes par les services et les vues Django ;
- `EF10` et `RG8` sont couverts par l'historique payé et les pages détail filtrées par propriétaire ;
- `EF11`, `EM9` et `RG7` sont couverts par l'admin Django enrichi, les vues d'administration protégées par permissions et les tests d'intégration ;
- les confirmations affichées, le message explicite de refus, les pages panier/paiement et le parcours checkout sont couverts par tests d'intégration ;
- `EF12`, `EM1` à `EM7`, `EM10`, `RG1` à `RG5` sont couverts par les modèles/services et tests domaine ;
- le rollback sur échec du décrément conditionnel renforce `EF12`, `EM1`, `EM6`, `ENF4`, `RG2` et `RG5` ;
- `RG6` est couvert par les vues de checkout et paiement protégées ;
- `EF8`, `EF9`, `EM6`, `EM7`, `EM10`, `RG4` et `RG5` sont maintenus ou étendus par les tests de navigation et d'affichage, mais leur comportement cœur était déjà implémenté par le parcours checkout/paiement ;
- `e2e/test_nominal_booking_flow.py::test_nominal_booking_flow_accepted_payment_appears_in_history` couvre le parcours nominal complet en navigateur avec `live_server` et des fixtures de base de test ;
- `e2e/test_nominal_booking_flow.py::test_invalid_quantity_displays_french_server_validation` vérifie que la quantité supérieure à 6 est rejetée par Django avec un message français, tout en conservant les attributs HTML sémantiques ;
- `e2e/test_page_performance.py::test_standard_page_lcp_under_two_seconds` couvre `ENF2` par mesure LCP Chromium sur des pages standards sous conditions contrôlées ;
- le suivi admin des ventes est une fonctionnalité privilégiée et ne change pas la portée de `RG8`, qui reste l'isolation des commandes des utilisateurs standards.

## Preuve Playwright nominale

| Test | Exigences couvertes | Implémentation exercée | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| `e2e/test_nominal_booking_flow.py::test_nominal_booking_flow_accepted_payment_appears_in_history` | `EF1`, `EF2`, `EF4`, `EF5`, `EF6`, `EF7`, `EF8`, `EF10`, `EF12`, `EM1`, `EM2`, `EM3`, `EM6`, `EM7`, `EM10`, `ENF1`, `ENF6`, `ENF7`, `RG1`, `RG2`, `RG3`, `RG5` | Catalogue, fiche concert, connexion, formulaire panier, checkout, paiement simulé accepté, confirmation, historique et assertions ORM sur commande/stock/prix | Couvert | Le paiement refusé et la redirection anonyme restent couverts par les tests d'intégration Django |

## Preuve Playwright de validation française

| Test | Exigences couvertes | Implémentation exercée | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| `e2e/test_nominal_booking_flow.py::test_invalid_quantity_displays_french_server_validation` | `ENF4`, `RG3` | Formulaire de réservation avec `novalidate`, attributs HTML `required`, `min`, `max` et `type="number"`, validation Django et message d'erreur français | Couvert | Le test cible la borne haute ; les autres classes et limites restent couvertes par les tests Django |

## Preuve Playwright performance ENF2

| Test | Exigences couvertes | Pages mesurées | Seuil et preuves | Limite connue |
| --- | --- | --- | --- | --- |
| `e2e/test_page_performance.py::test_standard_page_lcp_under_two_seconds` | `ENF2` | Accueil `/`, catalogue `/concerts/`, fiche `/concerts/<id>/`, historique authentifié `/commandes/` | Chromium Playwright, `live_server`, viewport 1366x768, données contrôlées, contexte froid par page, LCP `<= 2 000 ms`, durée `PerformanceNavigationTiming` en diagnostic, Bootstrap 5.3.3 rejoué depuis fixtures locales conformes SRI | Mesure de laboratoire CI contrôlée ; ne prouve pas la performance de production sur tous les appareils, états CDN ou réseaux |

## Exigences fonctionnelles

| ID | Implémentation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| EF1 | `concerts.views.ConcertListView`, route `/concerts/`, template `concerts/concert_list.html` | `tests/test_concert_views.py::test_concert_list_returns_200_and_only_displays_bookable_concerts`, `test_concert_list_displays_a_clear_empty_state` | Couvert | La liste publique masque volontairement tous les concerts non réservables |
| EF2 | `concerts.views.ConcertDetailView`, route `/concerts/<id>/`, template `concerts/concert_detail.html` | `tests/test_concert_views.py::test_concert_detail_displays_required_information`, tests des états non réservables et des réponses `404` | Couvert | Les brouillons ne sont pas publiés |
| EF3 | `accounts.User`, `accounts.forms.RegistrationForm`, `accounts.views.SignUpView` | `tests/test_accounts.py`, `tests/test_authentication_views.py::test_account_creation_succeeds_with_unique_email`, `test_duplicate_email_registration_is_rejected_with_french_message`, `test_registered_password_is_not_stored_in_plain_text` | Couvert | Pas de vérification e-mail ni profil avance, hors scope |
| EF4 | `accounts.views.LoginView`, `LogoutView`, `PersonalAreaView`, navigation auth | `tests/test_authentication_views.py::test_login_succeeds_with_valid_credentials`, `test_login_fails_with_invalid_credentials`, `test_logout_clears_session_through_post_logout_view`, `test_personal_area_requires_authentication`, `test_authenticated_user_can_access_personal_area`, `test_navigation_uses_post_logout_form_for_authenticated_user` | Couvert | `Mon espace` ne contient pas encore l'historique |
| EF5 | `cart.forms.AddTicketForm`, `cart.views.AddTicketToCartView`, `cart.services.add_ticket_to_cart`, fiche concert authentifiée | `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries`, `test_insufficient_stock_is_rejected_through_add_to_cart_flow`, `test_past_concert_is_rejected_through_add_to_cart_flow`, `test_cancelled_concert_is_rejected_through_add_to_cart_flow`, `test_closed_concert_is_rejected_through_add_to_cart_flow`, tests domaine existants | Couvert | Panier limité volontairement à un seul concert |
| EF6 | `Cart.total_amount`, `templates/cart/detail.html`, `templates/cart/checkout.html` | `tests/test_booking_flow.py::test_cart_display_calculates_total`, `test_cart_total_amount_uses_current_category_prices` | Couvert | Total calculé sur les prix courants du panier avant paiement |
| EF7 | `payments.forms.SimulatedPaymentForm`, `payments.views.SimulatedPaymentView`, `payments.services.process_simulated_card_payment` | `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `test_refused_payment_does_not_create_validated_order_or_decrement_stock` | Couvert | Paiement simulé déterministe, sans prestataire réel |
| EF8 | Création d'une commande `paid`, paiement `accepted`, page `payments/confirmation.html`, lien vers détail/historique | `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `tests/test_order_history.py::test_paid_order_appears_in_history_after_successful_payment`, test domaine accepté | Couvert | Aucun e-mail de confirmation, hors scope |
| EF9 | Création d'une commande `refused`, stock inchangé, page `payments/refused.html`, exclusion de l'historique payé | `tests/test_booking_flow.py::test_refused_payment_does_not_create_validated_order_or_decrement_stock`, `tests/test_order_history.py::test_refused_orders_remain_non_final_and_are_excluded_from_history`, test domaine refusé | Couvert | Une commande refusée non finale est tracée |
| EF10 | `orders.views.OrderListView`, route `/commandes/`, template `orders/list.html`, historique des commandes payées du client connecté | `tests/test_order_history.py::test_user_sees_only_their_own_paid_orders`, `test_anonymous_order_history_and_detail_access_redirect_to_login`, `test_paid_order_appears_in_history_after_successful_payment` | Couvert | Historique limité aux commandes payées ; tentatives refusées exclues |
| EF11 | `concerts.admin.ConcertAdmin`, administration Django francisée, `concerts.services.cancel_concert`, `close_concert_sales`, routes `/concerts/administration/ventes/` et actions POST admin | `tests/test_admin_concert_management.py::test_django_admin_can_create_and_modify_concert_with_category`, `test_django_admin_uses_french_site_app_and_model_labels`, `test_cancel_action_permission_rules`, `test_cancelled_concert_rejects_new_reservations_and_preserves_paid_order`, `test_closed_concert_rejects_new_reservations_and_keeps_stock`, `test_sales_overview_counts_paid_sales_only` | Couvert | Pas de workflow Playwright admin |
| EF12 | Décrément stock après paiement accepté dans `process_simulated_payment`, avec rollback atomique si le décrément conditionnel échoue | `tests/test_core_domain.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `test_failed_conditional_stock_update_rolls_back_payment`, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert | La concurrence multi-processus reste hors du test SQLite local |

## Exigences métier

| ID | Implémentation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| EM1 | Validation stock + décrément transactionnel + contrainte stock non négatif + rollback si l'update conditionnel ne modifie aucune ligne | `tests/test_core_domain.py::test_failed_conditional_stock_update_rolls_back_payment`, tests domaine stock, `tests/test_booking_flow.py::test_insufficient_stock_is_rejected_through_add_to_cart_flow`, `test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert | La simulation cible la défense transactionnelle ; pas un test multi-processus |
| EM2 | Quantité minimale 1 et panier non vide | Tests domaine et `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries` | Couvert |  |
| EM3 | Maximum 6 billets agrégé par concert/commande | Tests domaine et `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries` | Couvert | Panier limité à un concert |
| EM4 | Concert passé refusé par le domaine, masqué du catalogue, expliqué sur sa fiche et rejeté à l'ajout panier | Tests domaine, `tests/test_concert_views.py::test_past_concert_detail_explains_unavailability_without_cta`, `tests/test_booking_flow.py::test_past_concert_is_rejected_through_add_to_cart_flow` | Couvert | Transition automatique vers le statut terminé non implémentée |
| EM5 | Concert annulé refusé par le domaine, masqué du catalogue, expliqué sur sa fiche et rejeté à l'ajout panier | Tests domaine, `tests/test_admin_concert_management.py::test_cancelled_concert_rejects_new_reservations_and_preserves_paid_order`, `tests/test_concert_views.py::test_cancelled_concert_detail_explains_unavailability_without_cta`, `tests/test_booking_flow.py::test_cancelled_concert_is_rejected_through_add_to_cart_flow` | Couvert |  |
| EM6 | Commande finale seulement si paiement accepté et stock décrémenté ; rollback complet si la validation atomique échoue | `tests/test_core_domain.py::test_failed_conditional_stock_update_rolls_back_payment`, tests domaine accepté/refusé, tests booking et historique | Couvert |  |
| EM7 | Prix figé au paiement et affiché dans le détail de commande | `test_price_snapshot_is_kept_after_category_price_changes`, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `tests/test_order_history.py::test_order_detail_displays_consistent_paid_order_data` | Couvert | Promotions et remises hors périmètre |
| EM8 | `accounts.User.email` unique et rejet formulaire des doublons e-mail | `tests/test_accounts.py::test_user_email_must_be_unique`, `tests/test_authentication_views.py::test_duplicate_email_registration_is_rejected_with_french_message` | Couvert | Unicité renforcée côté formulaire pour les variantes de casse |
| EM9 | Vues admin avec `PermissionRequiredMixin`, permissions `concerts.view_concert`, `orders.view_order`, `concerts.change_concert`, admin Django francisé et réservé aux administrateurs | `tests/test_admin_concert_management.py::test_sales_overview_permission_rules`, `test_cancel_action_permission_rules`, `test_django_admin_can_create_and_modify_concert_with_category`, `test_django_admin_uses_french_site_app_and_model_labels`, tests rôle utilisateur standard existants | Couvert | Les permissions fines sont limitées au périmètre concerts/ventes demandé |
| EM10 | `Order` lié à utilisateur, concert, date, statut ; données affichées dans l'historique et le détail | `test_accepted_payment_creates_paid_order_and_decrements_stock`, `tests/test_order_history.py::test_order_detail_displays_consistent_paid_order_data` | Couvert |  |

## Exigences non fonctionnelles

| ID | Implémentation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| ENF1 | Accès direct accueil -> catalogue -> fiche -> panier -> checkout -> paiement -> commandes | `tests/test_homepage.py`, tests concert, `tests/test_booking_flow.py`, `tests/test_order_history.py::test_paid_order_appears_in_history_after_successful_payment`, `e2e/test_nominal_booking_flow.py::test_nominal_booking_flow_accepted_payment_appears_in_history` | Couvert pour le parcours nominal | Le parcours administrateur ne possède pas de scénario Playwright |
| ENF2 | Mesure navigateur de pages standards avec LCP comme métrique primaire et durée de chargement comme diagnostic | `e2e/test_page_performance.py::test_standard_page_lcp_under_two_seconds` | Couvert sous conditions contrôlées | Accueil, catalogue, fiche et historique seulement ; pas une preuve production multi-appareils ou multi-réseaux |
| ENF3 | Mot de passe géré par Django auth et formulaire d'inscription Django | `tests/test_accounts.py::test_user_password_is_hashed`, `tests/test_authentication_views.py::test_registered_password_is_not_stored_in_plain_text` | Couvert | Aucun stockage en clair attendu |
| ENF4 | Services et formulaires rejettent les saisies invalides proprement avec des messages français ; `novalidate` laisse Django produire ces messages sans retirer `required`, `min`, `max`, types ou `inputmode` utiles ; une incohérence de stock tardive provoque un rollback explicite | Tests quantité/stock/statut domaine, `tests/test_core_domain.py::test_failed_conditional_stock_update_rolls_back_payment`, tests authentification, `tests/test_booking_flow.py::test_booking_form_keeps_html_constraints_with_server_side_validation`, `test_payment_form_keeps_html_constraints_and_displays_french_errors`, test Playwright de quantité invalide | Couvert pour le périmètre implémenté |  |
| ENF5 | Ruff, couverture applicative de branches avec seuil global de 90 %, chemins XML relatifs non ambigus, contrôle SRI/accessibilité statique et analyse SonarCloud des sources, templates et workflows | `ruff check .`, `pytest --cov --cov-report=term-missing --cov-report=xml`, `.github/scripts/validate_coverage_xml.py`, `tests/test_template_quality.py`, Quality Gate Sonar externe | Couvert | Le seuil local ne doit pas encourager les tests artificiels |
| ENF6 | Règles métier isolées en services testables, dont le rollback transactionnel stock/paiement | `tests/test_core_domain.py`, `tests/test_admin_concert_management.py`, `pytest` | Couvert | Les tests multi-processus restent hors SQLite local |
| ENF7 | Workflow GitHub Actions versionné avec Ruff, checks Django, contrôle migrations, tests, couverture, validation du XML, Playwright et Sonar conditionnel | `.github/workflows/ci.yml`, `.github/scripts/validate_coverage_xml.py`, checks requis `Django checks` et `SonarCloud Code Analysis` | Couvert | Une PR de fork peut ne pas recevoir `SONAR_TOKEN` et rester bloquée par le check requis |

## Règles de gestion

| ID | Implémentation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| RG1 | `Concert.is_bookable`, validation service, catalogue, fiche et ajout panier | Tests domaine, `tests/test_concert_views.py`, `tests/test_booking_flow.py`, tests statut `closed` | Couvert domaine et interface | Réservation effective limitée au panier mono-concert |
| RG2 | `validate_category_stock`, formulaire, ajout panier et contrôle conditionnel au décrément | Tests domaine, `tests/test_core_domain.py::test_failed_conditional_stock_update_rolls_back_payment`, `tests/test_booking_flow.py::test_insufficient_stock_is_rejected_through_add_to_cart_flow` | Couvert |  |
| RG3 | `validate_ticket_quantity`, contraintes lignes, `AddTicketForm`, attributs HTML `min="1"` et `max="6"` conservés avec validation Django en français | Tests domaine, `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries`, `test_booking_form_keeps_html_constraints_with_server_side_validation`, `e2e/test_nominal_booking_flow.py::test_invalid_quantity_displays_french_server_validation` | Couvert |  |
| RG4 | Paiement refusé créé commande non finale, affiche refus, stock inchangé, historique payé inchangé | Tests domaine, `tests/test_booking_flow.py::test_refused_payment_does_not_create_validated_order_or_decrement_stock`, `tests/test_order_history.py::test_refused_orders_remain_non_final_and_are_excluded_from_history` | Couvert |  |
| RG5 | Paiement accepté crée une commande payée, affiche confirmation et décrémente le stock dans une transaction ; tout échec du décrément annule la commande, le paiement et la transition du panier | `tests/test_core_domain.py::test_failed_conditional_stock_update_rolls_back_payment`, tests domaine acceptés, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `tests/test_order_history.py::test_paid_order_appears_in_history_after_successful_payment` | Couvert |  |
| RG6 | `LoginRequiredMixin` sur checkout et paiement | `tests/test_booking_flow.py::test_anonymous_user_cannot_access_checkout_or_payment` | Couvert |  |
| RG7 | Annulation admin via `cancel_concert`, statut `cancelled` non réservable, fiche sans CTA, commandes payées conservées | `tests/test_admin_concert_management.py::test_cancel_action_permission_rules`, `test_cancelled_concert_rejects_new_reservations_and_preserves_paid_order`, `tests/test_concert_views.py::test_cancelled_concert_detail_explains_unavailability_without_cta`, `tests/test_booking_flow.py::test_cancelled_concert_is_rejected_through_add_to_cart_flow` | Couvert |  |
| RG8 | Pages panier/checkout personnelles, pages résultat, historique payé et détail de commande filtrés par utilisateur standard | `tests/test_booking_flow.py::test_user_cannot_access_another_users_cart_checkout_or_order_pages`, `tests/test_order_history.py::test_user_sees_only_their_own_paid_orders`, `test_user_cannot_access_another_users_paid_order_detail`, `test_anonymous_order_history_and_detail_access_redirect_to_login` | Couvert | Historique limité aux commandes payées ; le suivi admin des ventes est hors RG8 |

## Règle de mise à jour

Chaque nouvelle implémentation doit ajouter une preuve dans cette matrice :

- fichier ou module d'implémentation ;
- fichier de test ;
- statut de couverture ;
- limite connue si la couverture est partielle.
