import calendar, time
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

CATEGORIES = (
    ('shop', 'Shop'),
    ('supermarket', 'Supermarket'),
    ('pharmacy', 'Phamarcy'),
    ('restorant', 'Restorant'),
)

class VendorManager(models.Manager):
    def search(self, query):
        lookups = (
            models.Q(name__icontains=query) |
            # models.Q(username__icontains=query) |
            # models.Q(username__icontains=query) |
            # models.Q(phone__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class Vendor(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first = models.CharField(max_length=200, null=False, blank=True)
    middle = models.CharField(max_length=200, blank=True, null=True)
    last = models.CharField(max_length=200, null=False, blank=True)
    gender = models.CharField(max_length=200,  default='unspecified', choices=GENDER)
    dob = models.DateField(null=False, blank=False)
    citizenship = models.CharField(max_length=200, null=False, blank=True,  default='Tanzanian')
    region = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = VendorManager()

    def __str__(self):
        return '{} {} {}'.format(self.first, self.middle, self.last)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("shop:detail", kwargs={"slug": self.slug})

    def get_front_url(self):
        return reverse("shop:front", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("vendor-" + str(calendar.timegm(time.gmtime())))
        super(Vendor, self).save(*args, **kwargs)

class ShopManager(models.Manager):
    def search(self, query):
        lookups = (
            models.Q(name__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class Shop(models.Model):
    owner = models.ForeignKey(Vendor, related_name='vendor_shop', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200,  default='unspecified', choices=CATEGORIES)
    tin_number = models.CharField(max_length=200,  default="00000000000000")
    contacts = models.CharField(max_length=50)
    region = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lon = models.CharField(max_length=200, blank=True, null=True)
    lat = models.CharField(max_length=200, blank=True, null=True)
    opening = models.CharField(max_length=200, blank=True, null=True)
    closing = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ShopManager()

    def __str__(self):
        return '{}'.format(self.owner)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("shop:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("shop-" + str(calendar.timegm(time.gmtime())))
        super(Shop, self).save(*args, **kwargs)