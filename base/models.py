from django.db import models


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=250)


class Vakancy(models.Model):
    title = models.CharField(max_length=250)
    salary = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Company(models.Model):
    title = models.CharField(max_length=250)
    vakancy = models.ForeignKey(Vakancy, on_delete=models.CASCADE, related_name='vakancys')

    def __str__(self):
        return self.title


class Worker(models.Model):
    title = models.CharField(max_length=250)
    from_s = models.PositiveIntegerField()
    to_s = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='worker')

    def __str__(self):
        return self.title
