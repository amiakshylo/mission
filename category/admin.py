from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from category import models


@admin.register(models.MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory_count']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            subcategory_count=Count('subcategory')
        )

    @admin.display(ordering='subcategory_count', description='SubCategories')
    def subcategory_count(self, obj):
        url = reverse('admin:category_subcategory_changelist') + f'?main_category__id__exact={obj.id}'
        return format_html('<a href="{}">{} Sub Categories</a>', url, obj.subcategory_count)


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_category_name']
    list_select_related = ['main_category']

    @admin.display(ordering='main_category__name', description='Main Categoty')
    def main_category_name(self, obj):
        return obj.main_category.name


