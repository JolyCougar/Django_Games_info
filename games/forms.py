from django import forms

from .models import Review, Rating, RatingStar


class ReviewForm(forms.ModelForm):
    """ Form for review """

    class Meta:
        model = Review
        fields = ['name', 'email', 'text']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border", "id": "contactcomment"}),
        }


class RatingForm(forms.ModelForm):
    """ Forms add Rating """
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
