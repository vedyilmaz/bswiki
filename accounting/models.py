from django.db import models
from django_cleanup import cleanup
from ckeditor.fields import RichTextField
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)


# Create your models here.

@cleanup.ignore
class Customers(models.Model):
    company = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    web = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    responsible = models.CharField(max_length=150, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    company_logo = models.FileField(blank=True, null=True, verbose_name="Add the company logo")
    note = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.company

    class Meta:
        ordering = ['-created_date']
        es_index_name = 'django'
        es_type_name = 'customer'
        es_mapping = {
            'properties': {
                'company': {'type': 'string', 'index': 'not_analyzed'},
                'address': {'type': 'string', 'index': 'not_analyzed'},
                'web': {'type': 'string', 'index': 'not_analyzed'},
                'responsible': {'type': 'string', 'index': 'not_analyzed'},
                'note': {'type': 'string', 'index': 'not_analyzed'}
            }
        }
