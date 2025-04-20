from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count
from myapp2.models import Client, Product, OrderItem, Order
import logging

logger = logging.getLogger(__name__)

class ClientOrderedProductsView(TemplateView):
    template_name = 'myapp3/client_ordered_products.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_id = self.kwargs.get('client_id')
        client = get_object_or_404(Client, id=client_id)
        period = self.request.GET.get('period', 'week')  # По умолчанию показываем за неделю
        
        # Текущая дата
        now = timezone.now()
        
        # Определяем начало периода в зависимости от выбранного периода
        if period == 'week':
            start_date = now - timedelta(days=7)
            period_name = 'за последние 7 дней'
        elif period == 'month':
            start_date = now - timedelta(days=30)
            period_name = 'за последние 30 дней'
        elif period == 'year':
            start_date = now - timedelta(days=365)
            period_name = 'за последние 365 дней'
        else:
            start_date = now - timedelta(days=7)  # По умолчанию неделя
            period_name = 'за последние 7 дней'
            
        # Выводим детальную информацию
        logger.debug(f'Период: {period}, начальная дата: {start_date}, конечная дата: {now}')
            
        # Получаем все заказы клиента за указанный период
        orders = Order.objects.filter(
            client=client,
            order_date__gte=start_date,
            order_date__lte=now
        ).order_by('-order_date')
        
        # Для отладки - выводим количество заказов за период
        order_count = orders.count()
        context['total_orders'] = order_count
        
        # Получаем уникальные товары из этих заказов
        ordered_products = Product.objects.filter(
            orderitem__order__in=orders
        ).distinct()
        
        # Получаем список заказов для каждого товара с датами
        products_with_dates = []
        for product in ordered_products:
            # Находим все заказы этого товара за выбранный период
            order_items = OrderItem.objects.filter(
                product=product,
                order__in=orders
            ).order_by('-order__order_date')
            
            # Получаем количество заказов для этого товара за выбранный период
            order_count = order_items.count()
            
            # Берем первый (самый последний) заказ для сортировки
            latest_order = order_items.first()
            latest_order_date = latest_order.order.order_date if latest_order else None
            
            products_with_dates.append({
                'product': product,
                'latest_order_date': latest_order_date,
                'order_count': order_count
            })
        
        # Сортируем товары по дате последнего заказа
        products_with_dates.sort(key=lambda x: x['latest_order_date'] or timezone.now(), reverse=True)
        
        context.update({
            'client': client,
            'products_with_dates': products_with_dates,
            'period': period,
            'period_name': period_name,
            'start_date': start_date,
            'end_date': now,
        })
        
        return context
