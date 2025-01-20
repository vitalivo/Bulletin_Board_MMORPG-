from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content_text', 'category', 'user']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5 or len(title) > 100:
            raise forms.ValidationError('Заголовок должен быть от 5 до 100 символов.')
        return title
