from django.db import models

class DomainCrawl(models.Model):
    domain = models.CharField(max_length=255)
    hash_value = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=[('RUNNING', 'Running'), ('COMPLETED', 'Completed')], default='RUNNING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
