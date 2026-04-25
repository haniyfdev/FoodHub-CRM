from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# -- -- -- -- -- -- -- -- -- -- 
class User(AbstractUser):
    pass

# -- -- -- -- -- -- -- -- -- -- 
class RestaurantModel(models.Model): # abstract model. barcha modellar shundan meros oladi
    restaurant = models.ForeignKey('users.Restaurant', on_delete=models.CASCADE)
    class Meta:
        abstract = True

# -- -- -- -- -- -- -- -- -- -- 
class Restaurant(models.Model):
    name       = models.CharField(max_length=200)
    address    = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password   = models.CharField(validators=[MinLengthValidator(8)], max_length=16)
    is_active  = models.BooleanField()
    paid_until = models.DateTimeField()

# -- -- -- -- -- -- -- -- -- -- 
class Profile(RestaurantModel):
    class Role(models.TextChoices):
        BOSS   = 'boss' , 'Boshliq'
        ADMIN  = 'admin', 'Admin'
        WORKER = 'worker', 'Ishchi'
        VIEWER = 'viewer', 'Kuzatuvchi'

    user     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar   = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role     = models.CharField(max_length=50, choices=Role.choices, default=Role.WORKER)
    pin_code = models.CharField(validators=[MinLengthValidator(6)], max_length=6, blank=True, null=True)
    phone    = models.CharField(validators=[MinLengthValidator(9)], max_length=9) # +998 auto boshlanadi.
    pasport  = models.CharField(validators=[MinLengthValidator(9)], max_length=9) # passport raqam

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    





