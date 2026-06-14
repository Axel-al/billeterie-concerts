from django import forms

from cart.services import MAX_TICKETS_PER_CONCERT, MIN_TICKETS_PER_CONCERT


class AddTicketForm(forms.Form):
    seat_category = forms.ModelChoiceField(
        label="Catégorie",
        queryset=None,
        empty_label="Choisir une catégorie",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "data-testid": "seat-category-select",
            }
        ),
        error_messages={
            "required": "Choisissez une catégorie de place.",
            "invalid_choice": "La catégorie sélectionnée est invalide.",
        },
    )
    quantity = forms.IntegerField(
        label="Quantité",
        min_value=MIN_TICKETS_PER_CONCERT,
        max_value=MAX_TICKETS_PER_CONCERT,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "data-testid": "ticket-quantity-input",
                "min": MIN_TICKETS_PER_CONCERT,
                "max": MAX_TICKETS_PER_CONCERT,
            }
        ),
        error_messages={
            "required": "Indiquez une quantité de billets.",
            "invalid": "La quantité doit être un entier.",
            "min_value": "La quantité doit être au moins égale à 1.",
            "max_value": "La quantité ne peut pas dépasser 6 billets.",
        },
    )

    def __init__(self, concert, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["seat_category"].queryset = concert.seat_categories.filter(
            stock_remaining__gt=0
        )
