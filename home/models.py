from django.db import models

# Create your models here.

class Instance(models.Model):
    id = models.AutoField(primary_key = True)
    page_name = models.CharField(max_length = 10, unique=True)
    service = models.CharField(max_length = 10)
    git_url = models.CharField(max_length = 100)
    git_commit = models.CharField(max_length = 30, null = True)
    index_folder = models.CharField(max_length = 100, null = True)
