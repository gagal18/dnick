from django.contrib.auth.models import User
from django.db import models



class Cake(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='cakes/', null=True, blank=True)
    baker = models.ForeignKey('Baker', on_delete=models.CASCADE, null=True, blank=True, related_name='cakes')
    def __str__(self):
        return self.name


class Baker(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bakers/', null=True, blank=True)
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
