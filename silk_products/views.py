from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import SilkProduct, UserProfile
from .forms import SilkProductForm, CustomUserCreationForm, ContactSellerForm


def product_list(request):
    products = SilkProduct.objects.select_related('owner').all()
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(type__icontains=query))
    return render(request, 'silk_products/product_list.html', {'products': products, 'query': query})


def product_detail(request, pk):
    product = get_object_or_404(SilkProduct, pk=pk)
    contact_form = None
    
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        if request.user.userprofile.role == 'buyer' and product.owner != request.user:
            if request.method == 'POST':
                contact_form = ContactSellerForm(request.POST)
                if contact_form.is_valid():
                    subject = f"Interest in your product: {product.name}"
                    message = f"""
                    From: {request.user.get_full_name()} ({request.user.email})
                    Subject: {contact_form.cleaned_data['subject']}
                    
                    {contact_form.cleaned_data['message']}
                    
                    Product: {product.name}
                    Price: ${product.price}
                    """
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [product.owner.email],
                            fail_silently=False,
                        )
                        messages.success(request, 'Your message has been sent to the seller!')
                        return redirect('product_detail', pk=pk)
                    except:
                        messages.error(request, 'Failed to send message. Please try again.')
            else:
                contact_form = ContactSellerForm()
    
    return render(request, 'silk_products/product_detail.html', {
        'product': product,
        'contact_form': contact_form
    })


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def product_create(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'seller':
        messages.error(request, 'Only sellers can add products.')
        return redirect('product_list')
    
    if request.method == 'POST':
        form = SilkProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = SilkProductForm()
    return render(request, 'silk_products/product_form.html', {'form': form, 'title': 'Create Product'})


@login_required
def product_update(request, pk):
    product = get_object_or_404(SilkProduct, pk=pk)
    
    if product.owner != request.user:
        messages.error(request, 'You can only edit your own products.')
        return redirect('product_list')
    
    if request.method == 'POST':
        form = SilkProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = SilkProductForm(instance=product)
    return render(request, 'silk_products/product_form.html', {'form': form, 'title': 'Update Product'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(SilkProduct, pk=pk)
    
    if product.owner != request.user:
        messages.error(request, 'You can only delete your own products.')
        return redirect('product_list')
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'silk_products/product_confirm_delete.html', {'product': product})


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('product_list')


def favicon_view(request):
    return HttpResponse(status=204)
