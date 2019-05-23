from django import forms
from .models import Feed#, Category

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['url', 'category']
        labels = {
            'url': 'RSS/Atom URL',
            'category': 'Категория'
        }
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            #'category': forms.Select(choices=Category.objects.all())
        }
