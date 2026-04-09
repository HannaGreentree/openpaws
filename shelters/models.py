from django.db import models
from django.contrib.auth.models import User


class Shelter(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    animals_count = models.IntegerField(default=0)

    social_link_1 = models.URLField(default="https://example.com")
    social_link_2 = models.URLField(default="https://example.com")

    image = models.ImageField(upload_to="shelters/", blank=True, null=True)

    trust_points = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def update_verification(self):
        closed_cases_count = self.cases.filter(status="CLOSED").count()
        self.is_verified = closed_cases_count >= 10
        self.save(update_fields=["is_verified"])