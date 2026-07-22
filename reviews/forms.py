from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class MovieSearchForm(forms.Form):
    q = forms.CharField(
        label="Search by title",
        max_length=255,
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={"type": "search"}),
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")


class ReviewForm(forms.Form):
    rating = forms.TypedChoiceField(
        choices=[(rating, rating) for rating in range(1, 6)],
        coerce=int,
        empty_value=None,
    )
    body = forms.CharField(
        label="Review",
        widget=forms.Textarea(attrs={"rows": 6}),
    )
