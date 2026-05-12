from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<int:id>/<str:message>", views.listing_page, name="listing_page"), 
    path("add_bid", views.add_bid, name="add_bid"),
    path("category", views.category, name="category"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("inactive_listings", views.inactive_listings, name="inactive_listings"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("delete_watchlist", views.delete_watchlist, name="delete_watchlist") 

]
