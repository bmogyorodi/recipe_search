from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import (BaseManager)

NB = {"null": True, "blank": True}


class User(AbstractUser):
    pass


class BaseModel(models.Model):
    """
    A base model for all non-User models, storing information about creation
    and modification of each object, as well allowing to deactivate an object
    rather than deleting it
    """
    active = models.BooleanField("Active", default=True)
    created = models.DateTimeField(
        _("Created"), default=timezone.now, editable=False)
    modified = models.DateTimeField(
        _("Modified"), default=timezone.now)

    objects = BaseManager()

    # In order to ensure a model is cleaned before saving
    is_cleaned = False

    def clean(self, *args, **kwargs):
        """
        If a model needs cleaning, overwrite this method but don't call it
        """
        self.is_cleaned = True

    class Meta:
        abstract = True
        ordering = ('-active', '-modified')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # Ensure the model is cleaned before saving
        if not self.is_cleaned:
            self.clean()
        # Set created and modified timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

