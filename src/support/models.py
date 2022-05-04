import uuid, json, datetime
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.template import Context, Template

class NewsLetter(models.Model):
    email = models.EmailField()
    subscribed = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=120, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email
