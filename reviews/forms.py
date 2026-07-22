from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class AccessibleFormMixin:
    """Associate field help and validation errors with their controls."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        errors = self.errors if self.is_bound else {}
        for name, field in self.fields.items():
            described_by = []
            if field.help_text:
                described_by.append(f"id_{name}_helptext")
            if name in errors:
                field.widget.attrs["aria-invalid"] = "true"
                described_by.append(f"id_{name}_errors")
            if described_by:
                field.widget.attrs["aria-describedby"] = " ".join(described_by)


class MovieSearchForm(AccessibleFormMixin, forms.Form):
    q = forms.CharField(
        label="Search by title",
        max_length=255,
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={"type": "search"}),
    )


class RegistrationForm(AccessibleFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")


class ReviewForm(AccessibleFormMixin, forms.Form):
    rating = forms.TypedChoiceField(
        choices=[(rating, rating) for rating in range(1, 6)],
        coerce=int,
        empty_value=None,
    )
    body = forms.CharField(
        label="Review",
        widget=forms.Textarea(attrs={"rows": 6}),
    )
