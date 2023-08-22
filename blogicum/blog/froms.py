from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': '20', 'cols': '40'})
        }
        exclude = ('author', 'pub_date')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

