from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=250)


class Potency(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    potency_value = models.IntegerField(default=300)
    price = models.FloatField(default=0.00)
    supply = models.IntegerField(default=0)


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=50)


class ProductIngredients(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, primary_key=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)