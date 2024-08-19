from django.contrib.auth import get_user_model
from django.db import models
import uuid

user = get_user_model()


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    payment_method = models.CharField(max_length=255)
    amount = models.FloatField()
    user = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.transaction_id = str(uuid.uuid4()).replace('-','')
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.transaction_id