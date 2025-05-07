# Create your models here.
from django.db import models
from django.utils import timezone

class History(models.Model):
    prompt = models.TextField()
    metaphor = models.TextField()
    image = models.ImageField(upload_to='generated_images/')
    created_at = models.DateTimeField(default=timezone.now)