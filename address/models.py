from django.db import models, transaction
from django.conf import settings
# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_default:
                Address.objects.filter(user=self.user, is_default=True).exclude(id=self.id).update(is_default=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}, {self.city}"
