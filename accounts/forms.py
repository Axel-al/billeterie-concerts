from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Adresse email",
        error_messages={"required": "L'adresse email est obligatoire."},
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={"autocomplete": "given-name", "class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"autocomplete": "family-name", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = False
        self.fields["last_name"].required = False
        self.fields["password1"].label = "Mot de passe"
        self.fields["password2"].label = "Confirmation du mot de passe"
        self.fields["password1"].widget.attrs.update(
            {"autocomplete": "new-password", "class": "form-control"}
        )
        self.fields["password2"].widget.attrs.update(
            {"autocomplete": "new-password", "class": "form-control"}
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Un compte existe déjà avec cette adresse email.",
                code="duplicate_email",
            )
        return user_model.objects.normalize_email(email)


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "autocomplete": "email",
                "class": "form-control",
                "data-testid": "login-email",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Adresse email ou mot de passe invalide.",
        "inactive": "Ce compte est inactif.",
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["password"].label = "Mot de passe"
        self.fields["password"].widget.attrs.update(
            {
                "autocomplete": "current-password",
                "class": "form-control",
                "data-testid": "login-password",
            }
        )
