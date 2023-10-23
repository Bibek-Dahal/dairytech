from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from basemodels.models import BaseModel
from django.utils.html import mark_safe


class MyUserManager(BaseUserManager):
    def create_user(self,email,phone_number,first_name,last_name, password=None,middle_name=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        
        if not phone_number:
            raise ValueError(_("User must have phone number set."))
        
        if not first_name:
            raise ValueError(_("User must have first name set."))
        
        if not last_name:
            raise ValueError("User must have last name set.")
        
        if not email:
            raise ValueError(_("User must have email set."))
        
        userobj = User.objects.filter(email=email,phone_number=phone_number).exists()
        
        if userobj:
            
            raise ValueError(_("User with email or phone number already exists."))
        
        
        # user = None
        # if extra_fields.get('email'):

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            middle_name = middle_name
            
        )
        # else:
        #     user = self.model(
        #         first_name=first_name,
        #         last_name=last_name,
        #         phone_number=phone_number,
        #         password=password,  
        #         **extra_fields
        #     )
            

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,phone_number,first_name,last_name, password,middle_name=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        print("create sup called")
        print("email")
        
        user = self.create_user(
            email = email,
            phone_number=phone_number,
            middle_name=middle_name,
            first_name=first_name,
            last_name=last_name,
            password=password
            
            
        )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin,BaseModel):
    first_name = models.CharField(_("First name"),max_length=40)
    middle_name = models.CharField(_("Middle name"),max_length=40,blank=True,null=True)
    last_name = models.CharField(_("Last name"),max_length=40)
    email = models.EmailField(_("Email"),max_length=200,unique=True,blank=True,null=True)
    phone_number = models.BigIntegerField(_("Phone number"),unique=True)
    is_email_verified = models.BooleanField(_("Email verified"),default=False)
    address = models.CharField(_("Address"),max_length=100,blank=True,null=True)
    has_verified_dairy = models.BooleanField(_("Has verified dairy"),default=False)
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

    def __str__(self):
        return self.email
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","phone_number"]

    objects = MyUserManager()

    def get_name(self) -> str:
        
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    
    

