from django.db import models
from ckeditor.fields import RichTextField
from django_cleanup import cleanup
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)


# Create your models here.

@cleanup.ignore
class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    tag = models.CharField(max_length=150, blank=True, null=True)
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    article_image = models.FileField(blank=True, null=True, verbose_name="Add an image to the article")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']
        es_index_name = 'django'
        es_type_name = 'article'
        es_mapping = {
            'properties': {
                'title': {'type': 'string', 'index': 'not_analyzed'},
                'tag': {'type': 'string', 'index': 'not_analyzed'},
                'content': {'type': 'string', 'store': 'yes', 'index': 'not_analyzed'},
            }
        }


class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete = models.CASCADE,related_name="comments", verbose_name = "Article")
    comment_author = models.CharField(max_length=80, verbose_name="Comment Author")
    comment_content = models.TextField(max_length=200,verbose_name="Comment")
    comment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']
    

