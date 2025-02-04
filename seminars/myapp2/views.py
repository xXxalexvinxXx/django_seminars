from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Client, Product, Order
from .forms import ClientForm, ProductForm, OrderForm

# Clients CRUD
class ClientListView(ListView):
    model = Client
    template_name = 'myapp2/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

class ClientDetailView(DetailView):
    model = Client
    template_name = 'myapp2/client_detail.html'

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'myapp2/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'myapp2/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'myapp2/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

# Products CRUD
class ProductListView(ListView):
    model = Product
    template_name = 'myapp2/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp2/product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'myapp2/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'myapp2/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'myapp2/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

# Orders CRUD
class OrderListView(ListView):
    model = Order
    template_name = 'myapp2/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

class OrderDetailView(DetailView):
    model = Order
    template_name = 'myapp2/order_detail.html'

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'myapp2/order_form.html'
    success_url = reverse_lazy('order_list')

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'myapp2/order_form.html'
    success_url = reverse_lazy('order_list')

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'myapp2/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')
    