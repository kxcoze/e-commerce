from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Product, Review, Category

class ProductAdmin(admin.ModelAdmin):
    pass

class ReviewAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ['tree_actions', 'indented_title',]
    # list_display += ['related_products_count', 'related_products_cumulative_count']
    list_display_links = ('indented_title',)


    # def related_products_count(self, instance):
    #     return instance.products_count
    # related_products_count.short_description = 'Related products (for this specific category)'

    # def related_products_cumulative_count(self, instance):
    #     return instance.products_cumulative_count
    # related_products_cumulative_count.short_description = 'Related products (in tree)'

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)