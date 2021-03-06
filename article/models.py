from django.db import models
from ckeditor.fields import RichTextField
from django_cleanup import cleanup

# Create your models here.

@cleanup.ignore
class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE)
    title = models.CharField(max_length=80)
    tag = models.CharField(max_length=150,blank=True,null=True)
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    article_image = models.FileField(blank = True,null=True,verbose_name="Add an image to the article")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete = models.CASCADE,related_name="comments", verbose_name = "Article")
    comment_author = models.CharField(max_length=80, verbose_name="Comment Author")
    comment_content = models.TextField(max_length=200,verbose_name="Comment")
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']
    

