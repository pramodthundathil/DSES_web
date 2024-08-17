from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, id_number, password=None, **extra_fields):
        if not id_number:
            raise ValueError('The ID Field field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='last name')
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='phone number'
    )
    date_of_birth = models.DateField(auto_now_add=False)
    # age = models.BigIntegerField()
    address = models.TextField(blank=True, null=True, verbose_name='address')
    village = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff status')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')

    id_card_type = models.CharField(max_length=20, choices=(("PAN CARD","PAN CARD"),("VOTER ID","VOTER ID"),("DRIVING LICENCE","DRIVING LICENCE")))
    id_card_number = models.CharField(max_length=20)

    nominee_name = models.CharField(max_length=20, null=True, blank=True)
    nominee_relation = models.CharField(max_length=20,null=True, blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ["first_name", "pancard", "ifsc_code", "phone_number"]

    DSES_idcard = models.BooleanField(default=False)
    blood = models.CharField(max_length=10, default="O+")

    profile_pic = models.FileField(upload_to='profile_pic', null=True, blank=True)


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args, **kwargs):
        if not self.id_number:
            self.id_number = self.generate_unique_order_number()
        super(CustomUser, self).save(*args, **kwargs)

    def generate_unique_order_number(self):
        # Generate a unique order number using UUID
        return str(uuid.uuid4().hex[:5]).upper()
        
    def __str__(self):
        return self.email
    
class GalleryImages(models.Model):
    image_caption = models.CharField(max_length=200)
    image = models.FileField(upload_to='gallery')
    date = models.DateField(auto_now_add=True) 

