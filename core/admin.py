from django.contrib import admin
from core.models import Stock,Category
from core.forms import StockCreateForm

class StockAdmin(admin.ModelAdmin):
    list_display=('category', 'item_name', 'quantity')
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']
admin.site.register(Stock,StockAdmin)
admin.site.register(Category)

