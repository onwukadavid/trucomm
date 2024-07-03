from django.db import models
from django.db.models import Q
from django.utils import timezone


class CategoryManager(models.Manager):
    def get_all_categories(self):
        return self.all()
    
class ProductManager(models.Manager):
    def get_new_arrivals(self):
        future = timezone.now()-timezone.timedelta(1)
        return self.filter(Q(created_at__gte = future))