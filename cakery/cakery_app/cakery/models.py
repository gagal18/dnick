from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError



class Cake(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='cakes/', null=True, blank=True)
    baker = models.ForeignKey('Baker', on_delete=models.CASCADE, null=True, blank=True, related_name='cakes')
    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if Cake.objects.exclude(pk=self.pk).filter(name=self.name).exists():
            raise ValidationError({'name': "A cake with this name already exists."})

        baker_cakes = Cake.objects.filter(baker=self.baker)
        baker_cakes_count = baker_cakes.count()

        change = self.pk is not None

        if not change and baker_cakes_count >= 10:
            raise ValidationError("You can't have more than 10 cakes.")

        total_price = sum(c.price for c in baker_cakes)

        old_cake = baker_cakes.filter(pk=self.pk).first() if change else None

        if not change and total_price + self.price > 10000:
            raise ValidationError("Total cake price exceeds 10,000.")

        if change and old_cake and (total_price + self.price - old_cake.price) > 10000:
            raise ValidationError("Updated cake would exceed total price limit of 10,000.")

class Baker(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bakers/', null=True, blank=True)
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
