from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_item, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("mark_wishlist/<int:listing_id>", views.mark_wishlist, name="handle_wishlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close_listing"),
    path("comment/<int:listing_id>", views.comment, name='comment'),
    path("delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
    path("my_auctions", views.my_auctions, name="my_auctions"),
    path("my_wins", views.my_wins, name="wins"),
    path("category/<str:category>", views.category_filter, name="category")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)