from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_item, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("wishlist/<int:listing_id>", views.wishlist, name="handle_wishlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close_listing")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)