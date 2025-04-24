from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('coin/<int:coin_id>/', views.coin_detail, name='coin_detail'),  # Coin detail page
    path('add/', views.add_to_portfolio, name='add_to_portfolio'),  # Add Coin
    path('delete/<int:id>/', views.delete_coin, name='delete_coin'),
    path('crypto-news/', views.get_crypto_news, name='crypto_news'),
    path('coin/<str:coin_id>/', views.coin_chart, name='coin_chart'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('coins/', views.coins_table, name='coins_table'),
    path('chart/<str:symbol>/', views.chart_view, name='view_chart'),

]
