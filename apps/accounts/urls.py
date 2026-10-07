from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/', views.profile.as_view(), name='profile'),
    path('<int:group_pk>/', views.GroupUpdateView.as_view(), name='group_update'),

    path('<int:group_pk>/add', views.add_member, name='add_member'),
    path('<int:group_pk>/remove', views.remove_member, name='remove_member'),
    path('profile/create', views.group_create, name='group_create')
]