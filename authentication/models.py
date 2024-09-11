"""Module providing a function printing python version."""

from django.db import models


class AuditModel(models.Model):
    """Class representing a person"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Class representing a person"""

        abstract = True


class Usuarios(AuditModel):
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)

    class Meta:
        db_table = "Usuarios"
