from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content_text', 'category', 'user']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5 or len(title) > 100:
            raise forms.ValidationError('Заголовок должен быть от 5 до 100 символов.')
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

    def __init__(self, *args, **kwargs):
        self.post_id = kwargs.pop('post_id', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.post_id = self.post_id
        if commit:
            instance.save()
        return instance