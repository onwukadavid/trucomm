from django.db import models


class CategoryManager(models.Manager):
    def get_all_categories(self):
        return self.all()