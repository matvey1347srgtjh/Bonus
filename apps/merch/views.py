from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category

class HomeTemplateView(TemplateView):
    template_name = 'merch/home.html'

class MerchListView(ListView):
    model = Product
    template_name = 'merch/index.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, stock__gt=0).select_related('category')
        
        query = self.request.GET.get('q')
        if query:
            query = query.lower()
            queryset = queryset.annotate(lower_name=Lower('name')).filter(
                Q(lower_name__contains=query) | Q(description__icontains=query)
            )
            
        cat_slug = self.request.GET.get('category')
        if cat_slug:
            queryset = queryset.filter(category__slug=cat_slug)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'merch/product_detail.html'
    context_object_name = 'product'