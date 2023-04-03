from django.views.generic import ListView
from django.shortcuts import render,redirect
from core.models import Stock,StockHistory,Category
from core.forms import StockCreateForm,StockSearchForm,StockUpdateForm,IssueForm,ReceiveForm,ReorderLevelForm,HistoryStockCreateForm,HistoryIssueForm,HistoryReceiveForm,CategoryForm,StockHistorySearchForm
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator

def index(request):
    device = Stock.objects.all()

    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()

    categories = Category.objects.filter(parent_cat=None)
    context = {
        'categories': categories,
        'devices': device,
        'form': form,
        
    }
    

    return render(request,'index.html',context)



@login_required
def list_items(request):
    title = 'Avadanlıqların siyahısı'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    category = form['category'].value()

    categories = Category.objects.filter(parent_cat=None)

    context = {
        'form'  : form,
        'title' : title,
        'queryset' : queryset,
        'categories' : categories,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(
                                        item_name__icontains=form['item_name'].value())

        if (category != ''):
            queryset = queryset.filter(category_id=category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['KATEQORIYA','AVADANLIĞIN ADI','SAY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category,stock.item_name,stock.quantity])
            return response
        context = {
        'form'  : form,
        'title' : title,
        'queryset' : queryset,
        'categories' : categories,
    }
    
    return render(request, 'list_items.html',context)





# @login_required
# def update_items(request,pk):
#     queryset = Stock.objects.get(id=pk)
#     form = StockUpdateForm(instance=queryset)
#     if request.method == 'POST':
#         form = StockUpdateForm(request.POST, instance=queryset)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Successfully Saved')
#             return redirect('/list_items')
#     context = {
#         'form': form,
#         'title': "Add Item"
#     }
#     return render(request, 'add_items.html', context)

@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    form1 = HistoryStockCreateForm(request.POST or None)
    categories = Category.objects.filter(parent_cat=None)

    if form.is_valid() and form1.is_valid:
        form.save()
        form1.instance.user = request.user
        form1.save()
        messages.success(request, 'Uğurlu əlavə edildi')
        return redirect('/list_items')
    
    context = {
        'form' : form,
        'form': form1,
        'title' : 'Avadanlıq əlavə edin',
        'categories' : categories,
    }
    return render(request,'add_items.html',context)

# @login_required
# def delete_items(request,pk):
#     queryset = Stock.objects.get(id=pk)
#     queryset1 = StockHistory.objects.filter(item_name=queryset.item_name,category=queryset.category)

#     if request.method == 'POST':
#         queryset.delete()
#         queryset1.delete()
#         messages.success(request, 'Deleted Successfully')
#         return redirect('/list_items')
#     return render(request,'delete_items.html')

@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        'title': queryset.item_name,
        'queryset': queryset,
    }
    return render(request,'stock_detail.html',context)

@login_required
def issue_items(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance = queryset)
    form1 = HistoryIssueForm(request.POST or None)
    
    if form.is_valid() and form1.is_valid:
        form1.instance.item_name = form.instance.item_name
        form1.instance.category = form.instance.category
        form1.instance.user = request.user
        instance = form.save(commit=False)
        form1.save()
        instance.quantity -=  instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Əməliyyat uğurla yerinə yetirildi." +  "Anbarda" +  str(instance.quantity) + " " +str(instance.item_name) + ' var.')
        instance.save()
        return redirect('/stock_detail/'+str(instance.id))
    
    context = {
        'title': 'Götürülən avadanlıq: ' + str(queryset.item_name),
        'queryset': queryset,
        'form' : form,
        'form' : form1, 
        'username': 'Issue By: ' + str(request.user),
    }

    return render(request,'add_items.html',context)

@login_required
def receive_items(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance = queryset)
    form1 = HistoryReceiveForm(request.POST or None)
    
    if form.is_valid() and form1.is_valid:
        instance = form.save(commit=False)
        form1.instance.item_name = form.instance.item_name
        form1.instance.category = form.instance.category
        form1.instance.user = request.user
        form1.save()
        # instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Əməliyyat uğurla yerinə yetirildi. " + "Anbarda" + str(instance.quantity) + " " + str(instance.item_name)+"var. ")

        return redirect('/stock_detail/'+str(instance.id))
    
    context = {
        'title': 'Əlavə edilən avadanlıq: ' + str(queryset.item_name),
        'queryset': queryset,
        'form' : form,
        'form' : form1, 
        'username': 'Recieved By: ' + str(request.user),
    }

    return render(request,'add_items.html',context)
    

def reorder_level(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None,instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'Reorder level for ' + str(instance.item_name) + ' is updated to ' + str(instance.reorder_level))
        return redirect ('/list_items')

    context = {
        'instance': queryset,
        'form': form,
    }
    return render(request, "add_items.html",context)


@login_required
def list_history(request):
    header = 'Tarixçə'
    queryset = StockHistory.objects.all()
    paginator = Paginator(queryset,10)
    form = StockHistorySearchForm(request.POST or None)
    categories = Category.objects.filter(parent_cat=None)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'header': header,
        # 'queryset': queryset,
        'page_obj': page_obj,
        'form': form,
        'categories' : categories,
    }

    if request.method == 'POST':
        category = form['category'].value()
        user = form['user'].value()
        queryset = StockHistory.objects.filter(
            item_name__icontains = form['item_name'].value(),
            # last_updated__range = {
            #     form['start_date'].value(),
            #     form['end_date'].value()
            # }
        )

        if (category != ''):
            queryset = queryset.filter(category_id=category)
        
        if (user != ''):
            queryset = queryset.filter(user_id=user)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY','ITEM NAME','QUANTITY_IN_STORE','RECEIVE','ISSUE','DESCRIPTION','LAST_UPDATE'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category,stock.item_name,stock.quantity,stock.receive_quantity,stock.issue_quantity,stock.description,stock.last_updated])
            return response

        context = {
        'header': header,
        'queryset': queryset,
        'form': form,
        'categories' : categories,
        }

    return render(request,'list_history.html',context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is None:
            context = {'error': 'Invalid username or password'}
            return render(request,'login.html',context)
        login(request,user)
        return redirect('/list_items')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login')

##########################################
@login_required
def categories(request):
    categories = Category.objects.filter(parent_cat=None)
    title = 'Categories'
    context = {
        'categories': categories,
        'title' : title,
    }
    return render(request,'categories.html',context)

@login_required
def category_detail(request,pk):
    queryset = StockHistory.objects.filter(category__id=pk)
    categories = Category.objects.filter(parent_cat=None)
    context = {
        'queryset' : queryset,
        'categories' : categories,
    }
    if StockHistory.objects.filter(category__id=pk).first():
        queryset1 = StockHistory.objects.filter(category__id=pk).first()
        context = {
        'queryset' : queryset,
        'queryset1': queryset1,
        'categories' : categories,
    }

    return render(request,'category_list_items.html',context)

@login_required
def add_category(request):
    categories = Category.objects.filter(parent_cat=None)
    form = CategoryForm(request.POST or None)
    title = "Add category"
    if form.is_valid():
        form.save()
        return redirect('/list_items')
    context = {
        'title': title,
        "form": form,
        'categories' : categories,
    }
    return render(request,'add_category.html',context)





