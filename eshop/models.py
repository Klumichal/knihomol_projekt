from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=256)
    price = models.DecimalField(decimal_places=0, max_digits=20)
    published = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images", db_column="image", blank=True, null=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} : {self.id}"

class Cart(models.Model):
    products = models.ManyToManyField(
        Product, related_name="carts",
    )
    user = models.OneToOneField(
        get_user_model(),
        related_name="cart",
        on_delete=models.CASCADE

    )

    @property
    def total_price(self):
        total_price = Decimal("0")
        for product in self.products.all():
            total_price += product.price
        return total_price

class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, related_name="reviews",
        on_delete=models.CASCADE
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    user = models.ForeignKey(
        get_user_model(), related_name="user_reviews",
        on_delete=models.CASCADE
    )
    text = models.TextField()

class HelpdeskContact(models.Model):
    email = models.EmailField()
    nazev = models.CharField(max_length=512)
    text = models.TextField()
    solved = models.BooleanField(default=False)


