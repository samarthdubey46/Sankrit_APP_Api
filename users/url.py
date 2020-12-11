from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'users'
router = DefaultRouter()
router.register('all', AllinOne)
urlpatterns = [
    path('leaderboard/',LeaderBoard.as_view()),
    path('login/', login, name='api_token_auth'),
    path('', include(router.urls)),
    path('register/',register)
    # <-- And here
]
