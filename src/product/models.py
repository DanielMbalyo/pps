import random, calendar, time

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.db.models import Q

from src.shop.models import Shop, Vendor

def upload_location(instance, filename):
    random_ = random.randint(1, 3910209312)
    file_path = 'product/{random}/{title}-{filename}'.format(
        random=str(random_), title=str(instance.title), filename=filename
    )
    return file_path

class ProductManager(models.Manager):
    def search(self, query):
        lookups = (
            models.Q(title__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(calendar.timegm(time.gmtime())))
        super(Product, self).save(*args, **kwargs)

class UserProductManager(models.Manager):
    def search(self, query):
        lookups = (
            # models.Q(product__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class UserProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    quantity = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UserProductManager()

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.title + "-" + str(calendar.timegm(time.gmtime())))
        super(UserProduct, self).save(*args, **kwargs)