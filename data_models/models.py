from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    vendor_url = models.URLField()
    vendor_id = models.CharField(max_length=10, unique=True)


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    vendor_url = models.URLField()
    vendor_id = models.CharField(max_length=15, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    product_description = models.TextField()
    vendor_id = models.CharField(max_length=15, unique=True)
    sub_category = models.ManyToManyField(SubCategory)
    category = models.ManyToManyField(Category)
    ingredients = models.ManyToManyField(Ingredient)
