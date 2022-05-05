import calendar, time
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

def upload_location(instance, filename):
    file_path = 'clients/profile/{name}-{filename}'.format(
        name=str(instance.name), filename=filename
    )
    return file_path

class ClientManager(models.Manager):
    def search(self, query):
        lookups = (
            models.Q(name__icontains=query) |
            models.Q(username__icontains=query) |
            models.Q(phone__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class Client(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    employer = models.CharField(max_length=200,  default="NIL")
    branch = models.CharField(max_length=200, blank=True, null=True)
    office_phone = models.CharField(max_length=200,  default="0712345743")
    months = models.CharField(max_length=200,  default="1 Month")
    nid = models.CharField(max_length=200,  default="00000000000000")
    phone = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    profile = models.ImageField(upload_to=upload_location, null=False, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClientManager()

    def __str__(self):
        return '{}, {}'.format(self.name, self.account.email)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("client:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + "-" + str(calendar.timegm(time.gmtime())))
        super(Client, self).save(*args, **kwargs)

