from django.db import models
from django.contrib.auth.models import User



category_choice = {
    ('Hub', 'Hub'),
    ('Switch', 'Switch'),
    ('Router', 'Router'),
    ('Access point', 'Access point'),
    ('Computer devices', 'Computer devices'),
    ('Electric devices', 'Electric devices'),
}


class Category(models.Model):
    parent_cat = models.ForeignKey('self', on_delete=models.CASCADE,
                db_index=True, related_name='children', null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        if self.parent_cat:
            return f'{self.parent_cat}>{self.name}'
        return self.name


class Stock(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                db_index=True, related_name='stocks', blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    receive_quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    issue_quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.PositiveIntegerField(default=0, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    # date = models.DateTimeField(auto_now_add=False, auto_now=False)

    def __str__(self):
        return self.item_name + ' ' + str(self.quantity)

class StockHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                db_index=True, related_name='histories', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                db_index=True, related_name='histories', blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    receive_quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    issue_quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
   

    # user = models.CharField
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False,null=True)
    
    def __str__(self):
        return str(self.item_name)


