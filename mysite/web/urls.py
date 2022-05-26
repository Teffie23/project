from django.urls import path
from .views import *
urlpatterns = [
    path('',home.as_view(),name='home'),
    path('scafs/<slug:scafs_slug>/',test,name='scafs'),
    path('trainer/<slug:train_slug>/',tray,name='train'),
    path('think/',Think.as_view(),name='think'),
    path('login/',LoginUser.as_view(),name='login'),
    path('register/',registerUser.as_view(),name='register'),
    path('logout/',logout_user,name='logout'),
    path('other/',other,name='other'),
    path('reverse_top/',reverse_top,name='reverse_top'),
    path('bye/<order_id>',bye,name='bye'),

]
#showpost.as_view()