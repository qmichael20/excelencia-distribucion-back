from django.db import models
from django.core.validators import MinLengthValidator


class Vendedor(models.Model):
    vendedor = models.CharField(
        max_length=3, validators=[MinLengthValidator(3)], unique=True
    )

    def __str__(self):
        return self.vendedor
