from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "text", "post",)
        widgets = {
            "post": forms.TextInput(attrs={'hidden': True}),
            "text": forms.Textarea(attrs={'class': 'form-control mb-0 mt-0'}),
            "name": forms.TextInput(attrs={'class': 'form-control mb-0 mt-0'}),
            "email": forms.EmailInput(attrs={'class': 'form-control mb-0 mt-0'}),
        }
