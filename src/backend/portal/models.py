# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384


class RijpModelBase(models.Model):
    PRIORITY_CHOICES = (
        (0, 'Ultra low'),
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Immediate'),
    )
    created = models.DateTimeField(
        default=datetime.now
    )
    modified = models.DateTimeField(
        # default value is handled by the signals in signals.py
        # default=datetime.now
    )
    is_archived = models.BooleanField(
        default=False
    )
    name = models.CharField(
        max_length=STRING_LENGTH_SHORT
    )
    description = models.TextField(
        max_length=STRING_LENGTH_MEDIUM,
        blank=True
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2
    )

    def get_priority(self):
        return '{0} priority'.format(self.PRIORITY_CHOICES[self.priority][1])

    def get_priority_bulma_class(self):
        return {
            0: 'is-white',
            1: 'is-info',
            2: 'is-warning',
            3: 'is-danger',
            4: 'is-black',
        }.get(self.priority)


class StorageResourceBase(RijpModelBase):
    BARCODE_CHOICES = (
        (0, 'UNKNOWN'),
        (1, 'UPC'),
        (2, 'EAN'),
        (3, 'CODE39'),
        (4, 'CODE128')
    )
    barcode = models.CharField(
        max_length=STRING_LENGTH_SHORT
    )
    length = models.DecimalField(
        decimal_places=3,
        max_digits=10
    )
    width = models.DecimalField(
        decimal_places=3,
        max_digits=10
    )
    height = models.DecimalField(
        decimal_places=3,
        max_digits=10
    )
    weight = models.DecimalField(
        decimal_places=3,
        max_digits=10
    )


class Profile(RijpModelBase):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return 'Profile of: {0}'.format(self.user)


class StorageResource(StorageResourceBase):
    storage_owner = models.ForeignKey(
        Profile,
        related_name='storage_resources',
        on_delete=models.CASCADE,
        default=None
    )


class StorageItem(StorageResourceBase):
    storage_resource = models.ForeignKey(
        StorageResource,
        related_name='storage_items',
        on_delete=models.CASCADE,
        default=None
    )
