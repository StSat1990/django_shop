from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django2 import settings
from products import views
from products.views import IndexPageView, ShopPageView, send_form, ShopDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPageView.as_view(), name='index'),
    path('shop', ShopPageView.as_view(), name='shop'),
    path('shop/<int:pk>/', ShopDetailView.as_view(), name='shop-detail'),
    path('user_cart', views.user_cart),
    path('add_to_cart/<int:pk>', views.add_products_to_user_card),
    path('delete_product/<int:pk>', views.delete_exact_user_cart),
    path('forms', send_form, name='forms'),
    path('accounts/', include('allauth.urls')),
    path('login', views.CustomLoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
