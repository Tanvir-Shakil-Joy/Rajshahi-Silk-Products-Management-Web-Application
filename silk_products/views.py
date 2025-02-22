from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import SilkProduct
from .forms import SilkProductForm

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = SilkProduct.objects.filter(
            Q(name__icontains=query) | Q(type__icontains=query)
        )
    else:
        products = SilkProduct.objects.all()
    return render(request, 'silk_products/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = SilkProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = SilkProductForm()
    return render(request, 'silk_products/product_form.html', {'form': form, 'action': 'Create'})

def product_update(request, pk):
    product = get_object_or_404(SilkProduct, pk=pk)
    if request.method == 'POST':
        form = SilkProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = SilkProductForm(instance=product)
    return render(request, 'silk_products/product_form.html', {'form': form, 'action': 'Update'})

def product_delete(request, pk):
    product = get_object_or_404(SilkProduct, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'silk_products/product_confirm_delete.html', {'product': product})
