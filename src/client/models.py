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

STATUS = (
    ('employed', 'Employed'),
    ('not-employed', 'Not Employed'),
)

SOURCE = (
    ('consultant', 'Consultant'),
    ('business', 'Business'),
    ('freelance', 'Freelance'),
)

RANGE = (
    ('Grade 1', 'Below 150,000'),
    ('Grade 2', '150,000-250,000'),
    ('Grade 3', '250,000-350,000'),
    ('Grade 4', '350,000-550,000'),
    ('Grade 5', '550,000-750,000'),
    ('Grade 6', '750,000-1,000,000'),
    ('Grade 7', 'Above 1,000,000'),
)

DURATION = (
    ('Duration 1', 'Less Than 3 Months'),
    ('Duration 2', '3 Months-6 Months'),
    ('Duration 3', '6 Months-1 Year'),
    ('Duration 4', '1 Year-2 Years'),
    ('Duration 5', '2 Years-3 Years'),
    ('Duration 6', '3 Years-5 Years'),
    ('Duration 7', 'Above 5 Years'),
)

DEPENDANTS = (
    ('0', '0 Dependant'),
    ('1', '1 Dependant'),
    ('2', '2 Dependant'),
    ('3', '3 Dependant'),
    ('4', '4 Dependant'),
    ('5', '5 Dependant'),
    ('Above', 'Above 5'),
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
    region = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
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

    def evaluate(self):
        finance = Finance.objects.filter(client=self).first()
        if finance:
            if finance.range == 'Grade 1':
                return 15000.00
            elif finance.range == 'Grade 2':
                return 25000.00
            elif finance.range == 'Grade 3':
                return 35000.00
            elif finance.range == 'Grade 4':
                return 50000.00
            elif finance.range == 'Grade 5':
                return 65000.00
            elif finance.range == 'Grade 6':
                return 80000.00
            elif finance.range == 'Grade 7':
                return 100000.00
        else:
            return 0.00
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("client-" + str(calendar.timegm(time.gmtime())))
        super(Client, self).save(*args, **kwargs)

class Finance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=200,  default='employed', choices=STATUS)
    source = models.CharField(max_length=200,  default='employed', choices=SOURCE)
    employer = models.CharField(max_length=200,  default="None")
    position = models.CharField(max_length=200,  default="None")
    branch = models.CharField(max_length=200, default="None")
    referee = models.CharField(max_length=200,  default="0712345743")
    duration = models.CharField(max_length=200, default="Duration 1", choices=DURATION)
    range = models.CharField(max_length=200,  default="Grade 1", choices=RANGE)
    dependants = models.CharField(max_length=200, default='0', choices=DEPENDANTS) 
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClientManager()

    def __str__(self):
        return '{}'.format(self.client)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("client:detail", kwargs={"slug": self.slug})
