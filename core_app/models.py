from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

from django.db import models
from .managers import SoftManager


User = get_user_model()


class OwnerMixin(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='owner')

    class Meta:
        abstract = True


class CreateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    is_deleted = models.BooleanField(null=True, blank=True, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    objects = SoftManager()

    class Meta:
        abstract = True
