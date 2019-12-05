from django.urls import path
from . import views

app_name = 'blog_auth'

urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logut,name='logout'),
    path('register/',views.user_register,name='register'),
    path('delete/<int:id>',views.user_delete,name='delete'),
]
