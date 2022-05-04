import calendar, time
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from src.client.models import Client

class ShopManager(models.Manager):
    def search(self, query):
        lookups = (
            models.Q(name__icontains=query) |
            # models.Q(username__icontains=query) |
            # models.Q(phone__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class Shop(models.Model):
    account = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lon = models.CharField(max_length=200, blank=True, null=True)
    lat = models.CharField(max_length=200, blank=True, null=True)
    opening = models.CharField(max_length=200, blank=True, null=True)
    closing = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ShopManager()

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("shop:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + "-" + str(calendar.timegm(time.gmtime())))
        super(Shop, self).save(*args, **kwargs)