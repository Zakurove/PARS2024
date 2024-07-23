from django.urls import path
from . import views

urlpatterns = [
    # Registration URL
    path('register/', views.register, name='register'),

    # Login URL
    path('login/', views.login, name='login'),

    # Logout URL
    path('logout/', views.logout_view, name='logout'),

    # # Profile URL
    # path('profile/', views.profile_view, name='profile'),
]