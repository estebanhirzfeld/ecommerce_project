from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from store.models import Product
from orders.models import Order
from .forms import ProductForm, UserForm, OrderForm

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('custom_admin:dashboard')
    return auth_views.LoginView.as_view(template_name='custom_admin/login.html')(request)

@staff_member_required
def dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(paid=True).aggregate(Sum('items__price'))['items__price__sum'] or 0
    total_revenue = "{:.2f}".format(total_revenue)
    total_products = Product.objects.count()
    total_users = User.objects.count()
    
    # Simple data for charts (last 5 orders)
    recent_orders = Order.objects.order_by('-created')[:5]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_users': total_users,
        'recent_orders': recent_orders,
    }
    return render(request, 'custom_admin/dashboard.html', context)

@method_decorator(staff_member_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'custom_admin/product/list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

@method_decorator(staff_member_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'custom_admin/product/form.html'
    success_url = reverse_lazy('custom_admin:product_list')

@method_decorator(staff_member_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'custom_admin/product/form.html'
    success_url = reverse_lazy('custom_admin:product_list')

@method_decorator(staff_member_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'custom_admin/product/confirm_delete.html'
    success_url = reverse_lazy('custom_admin:product_list')

@method_decorator(staff_member_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'custom_admin/user/list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(username__icontains=query)
        return queryset

@method_decorator(staff_member_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'custom_admin/user/form.html'
    success_url = reverse_lazy('custom_admin:user_list')

@method_decorator(staff_member_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'custom_admin/user/confirm_delete.html'
    success_url = reverse_lazy('custom_admin:user_list')

@method_decorator(staff_member_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'custom_admin/order/list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        paid = self.request.GET.get('paid')
        if paid == 'true':
            queryset = queryset.filter(paid=True)
        elif paid == 'false':
            queryset = queryset.filter(paid=False)
        return queryset

@method_decorator(staff_member_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'custom_admin/order/detail.html'
    context_object_name = 'order'

@method_decorator(staff_member_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'custom_admin/order/form.html'
    success_url = reverse_lazy('custom_admin:order_list')
