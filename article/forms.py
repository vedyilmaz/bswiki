from django.forms import ModelForm
from .models import Article

# Create the form class.


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'tag', 'content', 'article_image']
