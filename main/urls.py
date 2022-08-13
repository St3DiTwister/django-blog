from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('auth/', LoginUser.as_view(), name='auth'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('article/<int:id>', article, name='article'),
    path('settings/', profile_edit, name='settings'),
    path('profile/', profile, name='profile')
]

handler404 = pageNotFound