from django.contrib import admin
from shop.models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("slug", "name",)
    list_display = ( "name", "price",)

# Register the models
admin.site.register(Product, ProductAdmin)  # Product est déjà enregistré ici avec une configuration admin.
admin.site.register(Category)
