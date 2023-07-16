from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
from django.utils.deconstruct import deconstructible
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib import auth




class UserManager(BaseUserManager):

    def create_user(self, mobile_number, password=None):
        if not mobile_number:
            raise ValueError("The Mobile Number field must be set")

        user = self.model(mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None):
        user = self.create_user(mobile_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


@deconstructible
class UnicodeMobileValidator(validators.RegexValidator):
    regex=r'^\+91-\d{10}$'
    message = _(
       "Mobile number must be in the format +91-XXXXXXXXXX (e.g., +91-9421652506)"
    )
    flags = 0


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    mobile_validator = UnicodeMobileValidator()

    profile_pic = models.ImageField(blank=True, null=True, upload_to='user/images/')

    mobile_number = models.CharField(
        _("mobile_number"),
        max_length=15,
        unique=True,
        help_text=_(
            "Required. 15 characters or fewer. Letters, digits and +/- only."
        ),
        validators=[mobile_validator],
        error_messages={
            "unique": _("A user with that mobile_number already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "mobile_number"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

def random_pin():
    return str(random.randint(1000,9999))


class UserOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,default=random_pin())
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP: {self.otp} for User: {self.user.username}"
    
    def is_valid(self):
        # Calculate the time difference between current time and created_at
        time_difference = timezone.now() - self.created_at
        # Check if the time difference is less than or equal to 30 minutes (1800 seconds)
        return time_difference.total_seconds() <= 1800