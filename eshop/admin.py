from django.contrib import admin

from eshop.models import Product, HelpdeskContact, Category, Author

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","id")
    list_filter = ("name",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price")
    list_filter = ("category", "published")

class HelpdeskContactAdmin(admin.ModelAdmin):
    list_display = ("nazev", "email", "text", "solved")
    list_filter = ("solved",)




admin.site.register(Product, ProductAdmin)
admin.site.register(HelpdeskContact, HelpdeskContactAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author)
