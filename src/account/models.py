import random, string, uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.shortcuts import reverse
from django.template.loader import get_template
from django.utils import timezone

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

def upload_location(instance, filename):
    file_path = 'manager/profile/{name}-{filename}'.format(
        name=str(instance.name), filename=filename
    )
    return file_path

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_adminuser(self, email, password):
        user = self.create_user(email, password=password, is_active=True)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, is_active=True)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    vendor = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_name(self):
        if self.staff:
            return self.manager_set.all().first().name
        elif self.vendor:
            return self.shop_set.all().first().name
        else:
            return self.client_set.all().first().name

    def get_acc(self):
        if self.staff:
            return self.manager_set.all().first()
        elif self.vendor:
            return self.shop_set.all().first()
        else:
            return self.client_set.all().first()

    def get_short_name(self):
        return self.email

    def get_absolute_url(self):
        if self.staff:
            return self.manager_set.all().first().get_absolute_url()
        elif self.vendor:
            return self.shop_set.all().first().get_absolute_url()
        else:
            return self.client_set.all().first().get_absolute_url()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(activated=False, forced_expired=False).filter(
            timestamp__gt=start_range, timestamp__lte=end_range
        )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
            models.Q(email=email) | models.Q(user__email=email)
        ).filter(activated=False)

class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                path = "{base}{path}".format(base=settings.BASE_URL,
                    path=reverse("account:email_activate", kwargs={'key': self.key}))
                context = {'path': path, 'email': self.email}
                txt_ = get_template("account/emails/verify.txt").render(context)
                html_ = get_template("account/emails/verify.html").render(context)
                sent_mail = send_mail(
                    'Account Verification', txt_, settings.DEFAULT_FROM_EMAIL,
                    [self.email,], html_message=html_, fail_silently=False,)
                return sent_mail
        return False

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_key_generator(instance):
    size = random.randint(30, 45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_key_generator(instance)
    return key

def pre_save_email_activation(instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)
pre_save.connect(pre_save_email_activation, sender=EmailActivation)

# def post_save_user_create_reciever(instance, created, *args, **kwargs):
#     if created and not instance.admin:
#         obj = EmailActivation.objects.create(user=instance, email=instance.email)
#         obj.send_activation()
# post_save.connect(post_save_user_create_reciever, sender=User)
