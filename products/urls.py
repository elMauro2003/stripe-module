from django.urls import path
from .views import home, success, cancel
from .views import product_list, checkout


urlpatterns = [
    path("", home, name="home"),
    path("success/", success, name="success"),
    path("cancel/<int:product_id>/", cancel, name="cancel"),
    path('products/', product_list, name='product_list'),
    path('checkout/', checkout, name='checkout'),
]