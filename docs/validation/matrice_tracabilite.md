# Matrice de tracabilite

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Etat de couverture actuel

Le depot contient une fondation Django, un catalogue public de concerts, des fiches detaillees, le modele utilisateur email, les pages d'inscription/connexion/deconnexion/espace personnel, le parcours panier/checkout/paiement simule, le noyau domaine de billetterie, des services testables, Ruff, coverage, GitHub Actions et une configuration SonarCloud.

- `EF1` et `EF2` sont couvertes par les vues publiques et les tests d'integration ;
- `EF3`, `EF4`, `EM8`, `ENF3` et `ENF4` sont couverts pour le perimetre compte utilisateur et authentification ;
- `EF5`, `EF6`, `EF7`, `EF8` et `EF9` sont couvertes par les services et les vues Django ;
- les confirmations affichees, le message explicite de refus, les pages panier/paiement et le parcours checkout sont couverts par tests d'integration ;
- `EF12`, `EM1` a `EM7`, `EM10`, `RG1` a `RG5` et la partie reservation de `RG7` sont couvertes par les modeles/services et tests domaine ;
- `RG6` est couvert par les vues de checkout et paiement protegees ;
- `RG8` est partiellement couvert par les pages resultat de paiement filtrees par utilisateur ;
- `EF10` reste non couvert par absence d'historique complet de commandes ;
- `EF11` a une fondation via l'admin Django ; `EM9` reste une fondation de role seulement et n'est pas revendiquee comme couverte.

## Exigences fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| EF1 | `concerts.views.ConcertListView`, route `/concerts/`, template `concerts/concert_list.html` | `tests/test_concert_views.py::test_concert_list_returns_200_and_only_displays_bookable_concerts`, `test_concert_list_displays_a_clear_empty_state` | Couvert | La liste publique masque volontairement tous les concerts non reservables |
| EF2 | `concerts.views.ConcertDetailView`, route `/concerts/<id>/`, template `concerts/concert_detail.html` | `tests/test_concert_views.py::test_concert_detail_displays_required_information`, tests des etats non reservables et des reponses `404` | Couvert | Les brouillons ne sont pas publies |
| EF3 | `accounts.User`, `accounts.forms.RegistrationForm`, `accounts.views.SignUpView` | `tests/test_accounts.py`, `tests/test_authentication_views.py::test_account_creation_succeeds_with_unique_email`, `test_duplicate_email_registration_is_rejected_with_french_message`, `test_registered_password_is_not_stored_in_plain_text` | Couvert | Pas de verification email ni profil avance, hors scope |
| EF4 | `accounts.views.LoginView`, `LogoutView`, `PersonalAreaView`, navigation auth | `tests/test_authentication_views.py::test_login_succeeds_with_valid_credentials`, `test_login_fails_with_invalid_credentials`, `test_logout_clears_session_through_post_logout_view`, `test_personal_area_requires_authentication`, `test_authenticated_user_can_access_personal_area`, `test_navigation_uses_post_logout_form_for_authenticated_user` | Couvert | `Mon espace` ne contient pas encore l'historique |
| EF5 | `cart.forms.AddTicketForm`, `cart.views.AddTicketToCartView`, `cart.services.add_ticket_to_cart`, fiche concert authentifiee | `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries`, `test_insufficient_stock_is_rejected_through_add_to_cart_flow`, `test_past_concert_is_rejected_through_add_to_cart_flow`, `test_cancelled_concert_is_rejected_through_add_to_cart_flow`, tests domaine existants | Couvert | Panier limite volontairement a un seul concert |
| EF6 | `Cart.total_amount`, `templates/cart/detail.html`, `templates/cart/checkout.html` | `tests/test_booking_flow.py::test_cart_display_calculates_total`, `test_cart_total_amount_uses_current_category_prices` | Couvert | Total calcule sur les prix courants du panier avant paiement |
| EF7 | `payments.forms.SimulatedPaymentForm`, `payments.views.SimulatedPaymentView`, `payments.services.process_simulated_card_payment` | `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `test_refused_payment_does_not_create_validated_order_or_decrement_stock` | Couvert | Paiement simule deterministe, sans prestataire reel |
| EF8 | Creation d'une commande `paid`, paiement `accepted`, page `payments/confirmation.html` | `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, test domaine accepte | Couvert | Aucun email de confirmation, hors scope |
| EF9 | Creation d'une commande `refused`, stock inchange, page `payments/refused.html` | `tests/test_booking_flow.py::test_refused_payment_does_not_create_validated_order_or_decrement_stock`, test domaine refuse | Couvert | Une commande refusee non finale est tracee |
| EF10 | Aucun historique de commandes | Aucun | Non couvert | A implementer |
| EF11 | Admin Django pour concerts et categories | Aucun test permissions admin | Fondation seulement | Suspendre/annuler via UI admin non teste |
| EF12 | Decrement stock apres paiement accepte dans `process_simulated_payment` | Tests domaine et `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert | Concurrence avancee a completer en integration |

## Exigences metier

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| EM1 | Validation stock + decrement transactionnel + contrainte stock non negatif + rejet UI stock insuffisant | Tests domaine, `tests/test_booking_flow.py::test_insufficient_stock_is_rejected_through_add_to_cart_flow`, `test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert | Tests de concurrence multi-processus futurs |
| EM2 | Quantite minimale 1 et panier non vide | Tests domaine et `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries` | Couvert |  |
| EM3 | Maximum 6 billets agrege par concert/commande | Tests domaine et `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries` | Couvert | Panier limite a un concert |
| EM4 | Concert passe refuse par le domaine, masque du catalogue, explique sur sa fiche et rejete a l'ajout panier | Tests domaine, `tests/test_concert_views.py::test_past_concert_detail_explains_unavailability_without_cta`, `tests/test_booking_flow.py::test_past_concert_is_rejected_through_add_to_cart_flow` | Couvert | Transition automatique vers le statut termine non implementee |
| EM5 | Concert annule refuse par le domaine, masque du catalogue, explique sur sa fiche et rejete a l'ajout panier | Tests domaine, `tests/test_concert_views.py::test_cancelled_concert_detail_explains_unavailability_without_cta`, `tests/test_booking_flow.py::test_cancelled_concert_is_rejected_through_add_to_cart_flow` | Couvert | Action d'annulation admin non testee |
| EM6 | Commande finale seulement si paiement accepte | Tests domaine, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock`, `test_refused_payment_does_not_create_validated_order_or_decrement_stock` | Couvert |  |
| EM7 | Prix snapshot au paiement | `test_price_snapshot_is_kept_after_category_price_changes`, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert | Promotions/remises hors scope |
| EM8 | `accounts.User.email` unique et rejet formulaire des doublons email | `tests/test_accounts.py::test_user_email_must_be_unique`, `tests/test_authentication_views.py::test_duplicate_email_registration_is_rejected_with_french_message` | Couvert | Unicite renforcee cote formulaire pour les variantes de casse |
| EM9 | Admin Django base sur `is_staff`/`is_superuser` | `tests/test_accounts.py::test_superuser_defaults_to_staff_and_superuser_flags`, `tests/test_authentication_views.py::test_registered_standard_user_has_no_admin_privileges` | Non couvert, fondation role seulement | Permissions concert admin hors scope |
| EM10 | `Order` lie a utilisateur, concert, date, statut | `test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert domaine/service | Historique utilisateur futur |

## Exigences non fonctionnelles

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| ENF1 | Acces direct accueil → catalogue → fiche → panier → checkout → paiement | `tests/test_homepage.py`, tests concert, `tests/test_booking_flow.py` | Partiel | Historique de commandes non expose |
| ENF2 | Aucune mesure performance applicative | Aucun | Non couvert | A mesurer avec vues |
| ENF3 | Mot de passe gere par Django auth et formulaire d'inscription Django | `tests/test_accounts.py::test_user_password_is_hashed`, `tests/test_authentication_views.py::test_registered_password_is_not_stored_in_plain_text` | Couvert | Aucun stockage en clair attendu |
| ENF4 | Services et formulaires rejettent les saisies invalides proprement | Tests quantite/stock/statut domaine, tests authentification, `tests/test_booking_flow.py` | Couvert pour le perimetre implemente |  |
| ENF5 | Ruff configure dans `pyproject.toml` et CI | `ruff check .` local et CI | Couvert fondation | Suivi Sonar futur |
| ENF6 | Regles metier isolees en services testables | `tests/test_core_domain.py`, `pytest` | Couvert | A maintenir avec les vues |
| ENF7 | Workflow GitHub Actions versionne | `.github/workflows/ci.yml` | Couvert fondation | CI distante a verifier apres push |

## Regles de gestion

| ID | Implementation actuelle | Tests actuels | Statut | Limite connue |
| --- | --- | --- | --- | --- |
| RG1 | `Concert.is_bookable`, validation service, catalogue, fiche et ajout panier | Tests domaine, `tests/test_concert_views.py`, `tests/test_booking_flow.py` | Couvert domaine et interface | Reservation effective limitee au panier mono-concert |
| RG2 | `validate_category_stock`, formulaire et ajout panier | Tests domaine, `tests/test_booking_flow.py::test_insufficient_stock_is_rejected_through_add_to_cart_flow` | Couvert |  |
| RG3 | `validate_ticket_quantity`, contraintes lignes, `AddTicketForm` | Tests domaine, `tests/test_booking_flow.py::test_add_to_cart_quantity_boundaries` | Couvert |  |
| RG4 | Paiement refuse cree commande non finale, affiche refus et stock inchange | Tests domaine, `tests/test_booking_flow.py::test_refused_payment_does_not_create_validated_order_or_decrement_stock` | Couvert |  |
| RG5 | Paiement accepte cree commande payee, affiche confirmation et decremente stock | Tests domaine, `tests/test_booking_flow.py::test_accepted_payment_creates_paid_order_and_decrements_stock` | Couvert |  |
| RG6 | `LoginRequiredMixin` sur checkout et paiement | `tests/test_booking_flow.py::test_anonymous_user_cannot_access_checkout_or_payment` | Couvert |  |
| RG7 | Concert annule non reservable, absent du catalogue et sans CTA sur sa fiche | `test_cancelled_concert_not_bookable`, `tests/test_concert_views.py::test_cancelled_concert_detail_explains_unavailability_without_cta` | Partiel domaine et interface | Action admin d'annulation non testee |
| RG8 | Pages panier/checkout personnelles et pages confirmation/refus filtrees par utilisateur | `tests/test_booking_flow.py::test_user_cannot_access_another_users_cart_checkout_or_order_pages` | Partiel | Historique complet de commandes non implemente |

## Regle de mise a jour

Chaque nouvelle implementation doit ajouter une preuve dans cette matrice :

- fichier ou module d'implementation ;
- fichier de test ;
- statut de couverture ;
- limite connue si la couverture est partielle.
