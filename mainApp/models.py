from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from .choices import SOURCE_CHOICES

class Document(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name="exports")
    created=models.DateTimeField(auto_now_add=True)
    type=models.CharField(max_length=100)
    source_type=models.CharField(choices=SOURCE_CHOICES, blank=True, null=True, max_length=20)
    source_id=models.CharField(blank=True, null=True, max_length=50)
    input_meta_data=JSONField(default=dict, null=True, blank=True)
