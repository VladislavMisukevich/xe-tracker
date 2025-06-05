from django.contrib import admin
from .models import Product
from .models import Article

admin.site.register(Product)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
