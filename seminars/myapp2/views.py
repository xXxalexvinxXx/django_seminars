from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Client, Product, Order, OrderItem
from .forms import ClientForm, ProductForm, OrderForm

# Clients CRUD
class ClientListView(ListView):
    model = Client
    template_name = 'myapp2/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        return queryset

class ClientDetailView(DetailView):
    model = Client
    template_name = 'myapp2/client_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.orders.all().order_by('-order_date')
        return context

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'myapp2/client_form.html'
    success_url = reverse_lazy('myapp2:client_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Клиент успешно добавлен")
        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'myapp2/client_form.html'
    success_url = reverse_lazy('myapp2:client_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Данные клиента обновлены")
        return super().form_valid(form)

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'myapp2/client_confirm_delete.html'
    success_url = reverse_lazy('myapp2:client_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Клиент удален")
        return super().delete(request, *args, **kwargs)

# Products CRUD
class ProductListView(ListView):
    model = Product
    template_name = 'myapp2/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp2/product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'myapp2/product_form.html'
    success_url = reverse_lazy('myapp2:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Товар успешно добавлен")
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'myapp2/product_form.html'
    success_url = reverse_lazy('myapp2:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Данные товара обновлены")
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'myapp2/product_confirm_delete.html'
    success_url = reverse_lazy('myapp2:product_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Товар удален")
        return super().delete(request, *args, **kwargs)

# Orders CRUD
class OrderListView(ListView):
    model = Order
    template_name = 'myapp2/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

class OrderDetailView(DetailView):
    model = Order
    template_name = 'myapp2/order_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'myapp2/order_form.html'
    success_url = reverse_lazy('myapp2:order_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Заказ успешно создан")
        return super().form_valid(form)

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'myapp2/order_form.html'
    success_url = reverse_lazy('myapp2:order_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Заказ обновлен")
        return super().form_valid(form)

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'myapp2/order_confirm_delete.html'
    success_url = reverse_lazy('myapp2:order_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Заказ удален")
        return super().delete(request, *args, **kwargs)

# OrderItem CRUD - функциональные представления
def add_order_item(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
            
            # Проверка наличия товара
            if product.quantity < quantity:
                messages.error(request, f"Недостаточно товара. Доступно: {product.quantity}")
                return redirect('myapp2:order_detail', pk=order_id)
            
            # Создание позиции заказа
            order_item = OrderItem(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            order_item.save()
            
            messages.success(request, "Товар добавлен в заказ")
        
        except Product.DoesNotExist:
            messages.error(request, "Товар не найден")
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")
    
    return redirect('myapp2:order_detail', pk=order_id)

def update_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        
        try:
            # Возвращаем текущее количество на склад
            order_item.product.quantity += order_item.quantity
            
            # Проверка наличия товара
            if order_item.product.quantity < new_quantity:
                messages.error(request, f"Недостаточно товара. Доступно: {order_item.product.quantity}")
                # Возвращаем как было
                order_item.product.quantity -= order_item.quantity
                order_item.product.save()
                return redirect('myapp2:order_detail', pk=order_item.order.id)
            
            # Обновляем позицию заказа
            order_item.quantity = new_quantity
            order_item.save()
            
            messages.success(request, "Позиция заказа обновлена")
        
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")
    
    return redirect('myapp2:order_detail', pk=order_item.order.id)

def delete_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    order_id = order_item.order.id
    
    try:
        order_item.delete()
        messages.success(request, "Позиция удалена из заказа")
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
    
    return redirect('myapp2:order_detail', pk=order_id)

# API функции
def get_product_info(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.quantity,
            'discount': float(product.discount)
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)
