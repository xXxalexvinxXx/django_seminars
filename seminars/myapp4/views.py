from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from myapp2.models import Product
from .models import ProductPhoto
from .forms import ProductPhotoForm

class ProductPhotoCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для добавления фотографии к товару
    """
    model = ProductPhoto
    form_class = ProductPhotoForm
    template_name = 'myapp4/product_photo_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'product_id' in self.kwargs:
            kwargs['product_id'] = self.kwargs['product_id']
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'product_id' in self.kwargs:
            context['product'] = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Фотография успешно добавлена')
        if 'product_id' in self.kwargs:
            return reverse('myapp2:product_detail', kwargs={'pk': self.kwargs['product_id']})
        return reverse('myapp4:product_photos_list')

class ProductPhotosListView(ListView):
    """
    Представление для отображения списка всех фотографий товаров
    """
    model = ProductPhoto
    template_name = 'myapp4/product_photos_list.html'
    context_object_name = 'photos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по товару, если указан
        product_id = self.request.GET.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        # Поиск по названию товара
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(product__name__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_id'] = self.request.GET.get('product_id')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Если выбран конкретный товар, добавляем его в контекст
        product_id = self.request.GET.get('product_id')
        if product_id:
            context['selected_product'] = get_object_or_404(Product, pk=product_id)
        
        # Добавляем список всех продуктов для формы фильтрации
        context['products'] = Product.objects.all()
        
        return context

class ProductPhotoDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления фотографии товара
    """
    model = ProductPhoto
    template_name = 'myapp4/product_photo_confirm_delete.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Фотография успешно удалена')
        return reverse('myapp4:product_photos_list')

class SetMainPhotoView(LoginRequiredMixin, View):
    """
    Представление для установки фотографии как основной
    """
    def post(self, request, pk):
        photo = get_object_or_404(ProductPhoto, pk=pk)
        photo.is_main = True
        photo.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        messages.success(request, 'Установлена новая основная фотография')
        return redirect('myapp2:product_detail', pk=photo.product.pk)
