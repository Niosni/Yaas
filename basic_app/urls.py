from django.conf.urls import url, include
from basic_app import views

# TEMPOLATE URLs
app_name = 'basic_app'

urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/$',views.view_profile,name='view_profile'),
    url(r'^change-password$', views.change_password, name='change_password'),
    url(r'^auctions/$',views.auctions,name='auctions'),
    url(r'^auctions/add/$',views.add_auction,name='add_auction'),
    url(r'^auctions/bid',views.make_bid,name='make_bid'),
]
