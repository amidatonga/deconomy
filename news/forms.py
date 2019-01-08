from django import forms
from .models import Post

class PublicationForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = ('title', 'text')
