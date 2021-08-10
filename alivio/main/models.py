from django.db import models


class Product(models.Model):
	product_name = models.CharField(max_length=100)
	product_description = models.CharField(max_length=250)

	def __str__(self):
		return self.product_name

class Potency(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	potency_value = models.IntegerField(default=300)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	supply = models.IntegerField(default=0)
	
	def __str__(self):		
		return str(self.product) + " " + str(self.potency_value) + "mg"    

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=50)


class ProductIngredients(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, primary_key=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class Customer(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	device = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		if self.name:
			name = self.name
		else:
			name = self.device
		return str(name)

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_quantity(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	potency = models.ForeignKey(Potency, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "Order: " + str(self.order) + " | Item: " + str(self.potency) + " | Quantity: " + str(self.quantity)

	@property
	def get_total(self):
		total = self.potency.price * self.quantity
		return total