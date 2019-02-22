#from django.conf.paths import path, include, path

from django.urls import path
from basic_app import views

# TEMPOLATE paths
app_name = 'basic_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.view_profile, name='view_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('auctions/', views.auctions, name='auctions'),
    path('auctions/search/', views.searchAuctions, name='searchAuctions'),
    path('auctions/add/', views.add_auction, name='add_auction'),
    path('auctions/bid/', views.make_bid, name='make_bid'),
    path('auctions/bid/confirm', views.confirm_bid, name='confirm_bid'),
    path('auctions/bid/save', views.save_bid, name='save_bid'),
    path('auctions/edit/<int:id>', views.edit_auction, name='edit_auction'),
    path('auctions/ban/', views.ban_auction, name='ban_auction'),
    path('auctions/banned/', views.show_banned, name='show_banned'),
]
