from django.db import models


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=30)
    text = models.TextField(max_length=5000)
    publish_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return self.headline