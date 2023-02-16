from django.db import models
from django.utils.functional import cached_property

from products.models import Product

class Order(models.Model):
    STATUSES = (
        ('P', 'Pending'), 
        ('R', 'Ready'), 
        ('D', 'Delivered'),
        ('C', 'Completed'),
        ('A', 'Aborted'),
    )
    status = models.CharField(max_length=1, choices=STATUSES, default=STATUSES[0][0])
    created_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey('users.User', related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='Product_Order', related_name='orders')

    def __str__(self):
        return f'{self.id}'

    def get_price(self):
        """ 
        Calculate the summary price of products depending on their amount in order
        """
        po = Product_Order.objects.filter(order=self)
        sum = 0
        for p in po:
            sum += p.product.price * p.product_amount
        return sum
    price = cached_property(get_price)


class Product_Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_amount = models.PositiveIntegerField(null=False)
    
    def save(self, *args, **kwargs):
        if self.product_amount > self.product.amount:
            """
            if Product_Order.product_amount greater than Product.amount 
            then raise error, else proceed to save model instance.
            """
            raise ValueError(
                'Amount in order cannot be greater than product amount!'
            )
        self.product.amount -= self.product_amount
        super(Product_Order, self).save(*args, **kwargs)