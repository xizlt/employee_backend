import re

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

default_account = list
TYPE_EMAIL = 2
TYPE_MOBILE = 1
TYPE_INNER_PHONE = 3


class DateBase(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=True)
    update = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        abstract = True


class Position(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Filial(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(DateBase):
    name_first = models.CharField(max_length=200)
    name_middle = models.CharField(max_length=200, blank=True, null=True)
    name_last = models.CharField(max_length=200)
    comment = models.CharField(max_length=255, null=True, blank=True)
    position = models.ManyToManyField(Position)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    account = models.ManyToManyField('Account', blank=True)

    class Meta:
        ordering = ['name_last']

    def __str__(self):
        return f"{self.name_last} {self.name_first} {self.name_middle}".strip()

    def full_name(self):
        return re.sub('\W+', ' ', f"{self.name_last} {self.name_first} {self.name_middle}")

    def get_main_phone_number(self):
        try:
            return self.account.get(basic=True, type__id=TYPE_MOBILE).item
        except ObjectDoesNotExist:
            return ""

    def get_main_email(self):
        try:
            return self.account.get(basic=True, type__id=TYPE_EMAIL).item
        except ObjectDoesNotExist:
            return ""


class SpecialUsers(DateBase):
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=255, null=True, blank=True)
    appointment = models.CharField(max_length=255, null=True, blank=True)
    account = models.ForeignKey('Account', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class AccountType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Account(models.Model):
    type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    basic = models.BooleanField(default=False)
    item = models.CharField(max_length=50)
    password = models.CharField(max_length=50, null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.type.name} - {self.item}"
