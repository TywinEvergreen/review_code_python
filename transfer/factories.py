import random

from django.contrib.auth.models import User
import factory

from .models import AdditionalUserInformation


def get_unique_inn():
    while True:
        inn = f"{random.randint(0, 9)}{random.randint(0, 999999999)}"
        if not AdditionalUserInformation.objects.filter(inn=inn).exists():
            return inn


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("email")

    class Meta:
        model = User


class AdditionalUserInformationFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    inn = factory.LazyFunction(get_unique_inn)
    account = 100.50

    class Meta:
        model = AdditionalUserInformation
