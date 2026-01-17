from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_loan, name='apply_loan'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path("logout/", views.logout, name="logout"),
    path('login/', views.login_view, name='login'),
    path("register/", views.register_view, name="register"),
]
