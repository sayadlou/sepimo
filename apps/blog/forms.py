from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "text", "post",)
        widgets = {
            "post": forms.TextInput(attrs={'hidden': True}),
            "text": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'دیدگاه شما *'}),
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
        }
