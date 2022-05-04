import calendar, time
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

def upload_location(instance, filename):
    file_path = 'manager/profile/{name}-{filename}'.format(
        name=str(instance.name), filename=filename
    )
    return file_path

class ManagerManager(models.Manager):
    def search(self, query):
        lookups = (
            models.Q(name__icontains=query) |
            models.Q(slug__icontains=query)
        )
        return self.filter(lookups).distinct()

class Manager(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    profile = models.ImageField(upload_to=upload_location, null=False, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ManagerManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["timestamp"]

    def get_absolute_url(self):
        return reverse("manager:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + "-" + str(calendar.timegm(time.gmtime())))
        super(Manager, self).save(*args, **kwargs)


class Settings(models.Model):
    # days = models.IntegerField(default=4, choices=DAYS)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # expected = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # status = models.CharField(max_length=200, default='New', choices=CATEGORY_CHOICES)
    invest = models.BooleanField(default=False)
    # date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today)
    # timestamp = models.DateTimeField(auto_now_add=True)

    # objects = InvestmentManager()
 
    def __str__(self):
        return "Setting"

    # class Meta:
    #     ordering = ["date"]
