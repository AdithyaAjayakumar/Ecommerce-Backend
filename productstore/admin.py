from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Product, ProductImage

admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(ProductImage)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}  # auto fill while typing
    list_display = ("name", "slug")