from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from webapp.forms import ReviewForm
from webapp.models import Review, Product


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review/review_create.html'
    form_class = ReviewForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        review = form.save(commit=False)
        review.product = product
        review.author = self.request.user
        review.save()
        return redirect('webapp:product_view', pk=product.pk)


class ReviewUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'review/review_update.html'
    model = Review
    form_class = ReviewForm

    def test_func(self):
        review = self.get_object()
        return self.request.user.has_perm('webapp.change_review') or review.author == self.request.user

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.product.pk})


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    permission_required = 'webapp.delete_review'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def has_permission(self):
        review = self.get_object()
        return super().has_permission() or review.author == self.request.user

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.product.pk})