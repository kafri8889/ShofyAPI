from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f"User(name={self.name}, username={self.username}, email={self.email})"


class Store(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Store(name={self.name}, location={self.location}, user={self.user})"


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=14, decimal_places=3)  # max price: Rp.999.999.999,999
    quantity = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return (f"Product("
                f"name={self.name}, "
                f"description={self.description}, "
                f"price={self.price}, "
                f"quantity={self.quantity}, "
                f"store={self.store}"
                f")")


class CartItem(models.Model):
    """
    Shopping cart item

    1 cart item = 1 product
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
