from django.db import models


class Post(models.Model):
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)