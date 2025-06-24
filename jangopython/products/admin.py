from django.contrib import admin
from .models import Product, ProductImages, ProductMetaInformation, Cart, Order

admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(ProductMetaInformation)
admin.site.register(Cart)
admin.site.register(Order)
