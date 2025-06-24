from django.db import models
import uuid
from django.contrib.auth.models import User

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(unique=True)
    product_description = models.TextField()
    product_price = models.IntegerField(default=0)
    product_demo_price = models.IntegerField(default=0)
    quantity = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.product_name

class ProductMetaInformation(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="meta_info")
    product_measuring = models.CharField(max_length=100, null=True, blank=True, choices=(
        ("KG", "KG"), ("ML", "ML"), ("L", "L"), ("G", "G")))
    product_quantity = models.CharField(null=True, blank=True, max_length=100)
    is_restrict = models.BooleanField(default=False)
    restrict_quantity = models.IntegerField(default=0)

class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    product_image = models.ImageField(upload_to="products")

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.product_price

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(Cart)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=20, default="Placed")
