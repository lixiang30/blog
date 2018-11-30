from django.test import TestCase

# Create your tests here.

from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=10)

