from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE)

    def __str__(self):
        return self.user.username


STATES = (
    ('Active', 'Active'),
    ('Banned', 'Banned'),
    ('Due', 'Due'),
    ('Adjudicated', 'Adjudicated')
)


class Auction(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=None)
    due_date = models.DateTimeField()
    author = models.CharField(max_length=128)
    bidder = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, choices=STATES)

    def __str__(self):
        return self.title
