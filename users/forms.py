from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class UserRegistration(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwords):
        super(ProfileUpdateForm, self).__init__(*args, **kwords)
        self.fields['img'].label = 'Profile image'

    class Meta:
        model = Profile
        fields = ['img', 'age', 'bio']
