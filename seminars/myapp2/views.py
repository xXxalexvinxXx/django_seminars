from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, Client

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'myapp2/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(client=self.request.user.client)

class ClientOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'myapp2/order_detail.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(client=self.request.user.client)