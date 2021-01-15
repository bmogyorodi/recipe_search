from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        ''' Don't return any inactive objects '''
        return super().get_queryset().filter(active=True)

    def including_inactive(self):
        ''' Return all objects, including the inactive ones '''
        return super().get_queryset()
