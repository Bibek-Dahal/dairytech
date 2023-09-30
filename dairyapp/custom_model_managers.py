from django.db import models

class DairyModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_verified=True)