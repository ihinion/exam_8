from urllib.parse import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Product
from webapp.forms import SearchForm, ProductForm


class IndexView(ListView):
    template_name = 'product/index.html'
    model = Product
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(name__icontains=self.search_value)
        return queryset

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProductView(DetailView):
    template_name = 'product/product_view.html'
    model = Product


class ProductCreateView(UserPassesTestMixin, CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm
    model = Product

    def test_func(self):
        return self.request.user.has_perm('webapp.add_product')

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'product/product_update.html'
    form_class = ProductForm
    model = Product

    def test_func(self):
        return self.request.user.has_perm('webapp.change_product')

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_product')

