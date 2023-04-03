from django import forms
from core.models import  Stock,StockHistory,Category



class StockCreateForm(forms.ModelForm):
    # authors = forms.ModelChoiceField(queryset=Stock.objects.all())
    def __init__(self, *args, **kwargs):
        
        super(StockCreateForm, self).__init__(*args, **kwargs)
        # self.fields['category'] =forms.CharField(queryset=Category.objects.all())
    
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity'] 
        labels = {
        "category": "Kateqoriya:",
        'item_name': 'Avadanlığın adı:',
        'quantity': 'Say:',
        }
    
    

    # def clean_category(self):
    #     category = self.cleaned_data.get('category')
    #     if not category:
    #         raise forms.ValidationError('This field is required')
        
    #     for instance in Stock.objects.all():
    #         if instance.category == category:
    #             raise forms.ValidationError(category + ' is already created')
    #     return category

    # def clean_item_name(self):
    #     item_name = self.cleaned_data.get('item_name')
    #     if not item_name:
    #         raise forms.ValidationError('This field is required')
    #     return item_name

class HistoryStockCreateForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['category', 'item_name', 'quantity'] 
        labels = {
        "category": "Kateqoriya:",
        'item_name': 'Avadanlığın adı:',
        'quantity': 'Say:',
        }

class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False,label='CSV FAYLA KÖÇÜR')
    class Meta:
        model = Stock
        fields = ['category', 'item_name']
        labels = {
        "category": "Kateqoriya:",
        'item_name': 'Avadanlığın adı:',
        'export_to_CSV': 'CSV',
        }
        

class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False,label='CSV FAYLA KÖÇÜR')
    
    class Meta:
        model = StockHistory
        fields = ['user','category', 'item_name',]
        labels = {
            'user': 'İstifadəçi:',
            'category': "Kateqoriya:",
            'item_name': "Avadanlığın adı:"
        }


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name','quantity']


class HistoryStockUpdateForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['category', 'item_name','quantity']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity','description']
        


class HistoryIssueForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['issue_quantity','description']
        labels = {
            "issue_quantity": 'Say',
            'description': 'Təsvir',
        }

class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity','description']
        

class HistoryReceiveForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['receive_quantity','description']
        labels = {
            "receive_quantity": 'Say',
            'description': 'Təsvir',
        }

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields= ['parent_cat','name']
        labels = {
            'parent_cat': 'Kateqoriya',
            'name': 'Altkateqoriya'
        }
        widgets = {

        }

