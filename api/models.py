from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    '''
    creating a manager for a custom user model
    '''
    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "login"

class UserProfile(models.Model):
    gov_id = models.IntegerField(primary_key=True,max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gov_id = models.CharField(primary_key=True,max_length=100)
    company = models.CharField(max_length=100)

    class Meta:
        db_table = "profile"

class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    date_o = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    subtotal = models.FloatField()
    paid = models.CharField(max_length= 20, default='En proceso', blank=True)
    user_p = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "order"

class Shipping(models.Model):
    id_shipping = models.AutoField(primary_key=True)
    address = models.CharField(max_length= 20)
    city = models.CharField(max_length= 20)
    state = models.CharField(max_length= 20)
    country = models.CharField(max_length= 20)
    cost = models.FloatField()
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    class Meta:
        db_table = "shipping"

class Payment(models.Model):
    id_payment = models.AutoField(primary_key=True)
    date_p = models.DateTimeField(auto_now_add=True)
    taxes = models.FloatField()
    total = models.FloatField()
    status = models.CharField(max_length= 20, default='En proceso', blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = "payment"

