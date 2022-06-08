import calendar, time
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

MARTIAL = (
    ('single', 'Single'),
    ('relation', 'In Relation'),
    ('married', 'Married'),
    ('divorsed', 'Divorsed'),
)

IDS = (
    ('none', 'None'),
    ('nida', 'National ID'),
    ('voters id', 'Voters ID'),
    ('licence', 'Driving Licence'),
)

SOURCE = (
    ('employment', 'Employment'),
    ('consultant', 'Consultant'),
    ('business', 'Business'),
)

def upload_location(instance, filename):
    file_path = 'clients/profile/{name}-{filename}'.format(
        name=str(instance.name), filename=filename
    )
    return file_path

class ClientManager(models.Manager):
    def search(self, query):
        lookups = (
            models.Q(name__icontains=query) |
            models.Q(phone__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class Client(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first = models.CharField(max_length=200, null=False, blank=True)
    middle = models.CharField(max_length=200, blank=True, null=True)
    last = models.CharField(max_length=200, null=False, blank=True)
    gender = models.CharField(max_length=200,  default='unspecified', choices=GENDER)
    dob = models.DateField(null=False, blank=False)
    citizenship = models.CharField(max_length=200, null=False, blank=True,  default='Tanzanian')
    location = models.CharField(max_length=200, blank=True, null=True)
    martial = models.CharField(max_length=200,  default='single', choices=MARTIAL)
    identification = models.CharField(max_length=200,  default='single', choices=IDS)
    id_number = models.CharField(max_length=200,  default="00000000000000")
    phone = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    profile = models.ImageField(upload_to=upload_location, null=False, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClientManager()

    def __str__(self):
        return '{} {} {}'.format(self.first, self.middle, self.last)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("client:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("client-" + str(calendar.timegm(time.gmtime())))
        super(Client, self).save(*args, **kwargs)

class Finance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    source = models.CharField(max_length=200,  default='employed', choices=SOURCE)
    employer = models.CharField(max_length=200,  default="None")
    branch = models.CharField(max_length=200, blank=True, null=True)
    referee = models.CharField(max_length=200,  default="0712345743")
    duration = models.CharField(max_length=200,  default="1")
    range = models.FloatField(max_length=200, default=0.00)
    dependants = models.CharField(max_length=200, null=False, blank=True, default='0') 
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClientManager()

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("client:detail", kwargs={"slug": self.slug})
