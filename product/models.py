from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


# Connecting this database to the one above
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    # In description this can remain empty, not a required field
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # This field is to order our products
    class Meta:
        ordering = ('-created_at',)

    # This is a string representation of this class
    def __str__(self):
        return self.name

    def get_display_price(self):
        return self.price / 100
