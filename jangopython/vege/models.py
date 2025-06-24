from django.db import models
from django.contrib.auth.models import User

class Recepie(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipe_name = models.CharField(max_length=100)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to="receipes/", null=True, blank=True)
    receipe_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # New Field

    def __str__(self):
        return self.receipe_name
