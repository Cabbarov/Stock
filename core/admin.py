from django.contrib import admin
from core.models import Stock,Category,StockHistory
from core.forms import StockCreateForm,HistoryStockCreateForm

class StockAdmin(admin.ModelAdmin):
    list_display=('category', 'item_name', 'quantity')
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']
admin.site.register(Stock,StockAdmin)

class HistoryStockAdmin(admin.ModelAdmin):
    list_display=('category', 'item_name', 'quantity')
    form = HistoryStockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']
admin.site.register(StockHistory,HistoryStockAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_cat', )
    list_filter = ('name', 'parent_cat')
    search_fields = ('name', 'parent_cat')
admin.site.register(Category,CategoryAdmin)

