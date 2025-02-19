from django import forms
from library_app.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User, Review, Wishlist, Book

class UserRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    membership_type = forms.ChoiceField(choices=User.MEMBERSHIP_CHOICES)
    agree_to_terms = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username','firstname', 'lastname', 'email', 'password1', 'password2', 'date_of_birth', 'gender', 'membership_type', 'agree_to_terms']

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, '⭐' * i) for i in range(1, 6)], widget=forms.RadioSelect)  # Star rating
    class Meta:
        model = Review
        fields = ['comment', 'rating']

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = []  # Adjust this if you need fields for wishlist management



class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data