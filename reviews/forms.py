from django import forms


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
