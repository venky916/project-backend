from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class App(BaseModel):
    CHOICES = [
        (1, 'Education App'),
        (2, 'Music & Audio App'),
        (3, 'Business App'),
        (4, 'Tools App'),
        (5, 'Entertainment App'),
        (6, 'Lifestyle App'),
        (7, 'Books & References App'),
        (8, 'Food & Drinks App'),
        (9, 'Shopping App'),
        (10, 'Productivity App'),
    ]
    app_name = models.CharField(max_length=100, unique=True)
    points = models.IntegerField()
    app_category = models.IntegerField(choices=CHOICES, null=True, blank=True)
    app_image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.app_name

class Customer(User, BaseModel):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others")
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    user_image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.username

class AppCustomer(BaseModel):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'app')
