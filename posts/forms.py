from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
            'post'
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': '댓글 달기...'
                }
            )
        }