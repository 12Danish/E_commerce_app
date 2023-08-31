from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormView
from .models import ProductModel
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'seller/dashboard.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return ProductModel.objects.filter(user=self.request.user)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = ProductModel
    template_name = 'seller/details.html'


class AddProductForm(LoginRequiredMixin, FormView):
    form_class = ProductForm
    template_name = 'seller/add_product.html'

    def form_valid(self, form):
        data = form.cleaned_data
        user = self.request.user
        product = ProductModel(
            user=user,
            product_name=data['product_name'],
            product_price=data['product_price'],
            product_description=data['product_description'],
            product_image=data['product_image']
        )
        product.save()
        return HttpResponseRedirect(reverse('seller:dashboard'))


class DeleteProduct(DeleteView):
    model = ProductModel
    template_name = 'seller/confirm_delete.html'
    success_url = reverse_lazy('seller:dashboard')
