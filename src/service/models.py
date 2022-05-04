import random, calendar, time
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

def upload_location(instance, filename):
    random_ = random.randint(1, 3910209312)
    file_path = 'service/{random}/{title}-{filename}'.format(
        random=str(random_), title=str(instance.name), filename=filename
    )
    return file_path

class ServiceManager(models.Manager):
    def search(self, query):
        lookups = (
            models.Q(name__icontains=query) |
            # models.Q(username__icontains=query) |
            # models.Q(phone__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class Service(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ServiceManager()

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("service:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + "-" + str(calendar.timegm(time.gmtime())))
        super(Service, self).save(*args, **kwargs)
