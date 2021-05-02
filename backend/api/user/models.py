from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from api.cart.models import Cart


class UserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password):
        if not email:
            raise ValueError('User must have an email address')
        if not firstname or not lastname:
            raise ValueError('User must have firstname and lastname')
        if not password:
            raise ValueError('User must have password')
        
        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname
        )

        user.set_password(password)
        user.save(using=self._db)

        # create cart for user
        cart = Cart(user_id=user.id)
        cart.save()

        return user
    
    def create_superuser(self, email, firstname, lastname, password):
        user = self.create_user(email, firstname, lastname, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser):
    email = models.EmailField(max_length=128, unique=True)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin