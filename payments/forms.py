from django import forms


class SimulatedPaymentForm(forms.Form):
    card_number = forms.CharField(
        label="Numéro de carte",
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "inputmode": "numeric",
            }
        ),
        error_messages={
            "required": "Indiquez un numéro de carte.",
            "max_length": "Le numéro de carte est trop long.",
        },
    )

    def clean_card_number(self):
        return self.cleaned_data["card_number"].strip()
