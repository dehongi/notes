from django import forms
from .models import Note, Comment


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "is_public"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Add a comment...",
                }
            ),
        }
        labels = {
            "content": "",
        }
