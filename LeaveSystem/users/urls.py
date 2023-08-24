from django.urls import path
from .import views

app_name='users'

urlpatterns=[
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.register,name='register'),
    path('change_password/',views.changepassword,name='change_password'),
    #path('profile/',views.profile,name='profile'),

    #Users Views
    path('users/all',views.users_list,name='users'),
    path('users/<int:id>/block',views.users_block,name='userblock'),
    path('users/<int:id>/unblock',views.users_unblock,name='userunblock'),
    path('users/blocked/all',views.users_blocked_list,name='erasedusers'),

]