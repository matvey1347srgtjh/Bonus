from django.views.generic import ListView
from django.db.models import Q
from .models import Product, Category

class MerchListView(ListView):
    model = Product
    template_name = 'merch/index.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, stock__gt=0).select_related('category')
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            
        cat_slug = self.request.GET.get('category')
        if cat_slug:
            queryset = queryset.filter(category__slug=cat_slug)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context