from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.lander_details, name='lander_details'),
    path('interaction/', views.user_intriguer_response, name='interaction'),
    path('leaderboard/', views.get_leaderboard, name='leaderboard'),
]
