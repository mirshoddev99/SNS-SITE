from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from account.models import Profile


class Action(models.Model):
    user = models.ForeignKey(Profile, related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id']),
        ]
        ordering = ['-created']


"""
target_ct: A ForeignKey field that points to the ContentType model
target_id: A PositiveIntegerField for storing the primary key of the related object
target: A GenericForeignKey field to related object based on the combination of the two previous field
"""

