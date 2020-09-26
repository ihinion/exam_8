from django.urls import path, include

from webapp.views import IndexView, ProductView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView


app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('product/', include([
        path('add/', ProductCreateView.as_view(), name='product_create'),
        path('<int:pk>/', include([
            path('', ProductView.as_view(), name='product_view'),
            path('update/', ProductUpdateView.as_view(), name='product_update'),
            path('delete/', ProductDeleteView.as_view(), name='product_delete'),
        ])),
    ])),
]
