from django.contrib import admin

from store.models import Category, Location, Product, Order


admin.site.empty_value_display = 'Не задано'


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        ProductInline,
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'category',
        'created_at'
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location)
admin.site.register(Order)
