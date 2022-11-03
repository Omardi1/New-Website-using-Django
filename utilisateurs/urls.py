from django.urls import path

from utilisateurs.views import logout_user, user

urlpatterns = [
    path('user/', user, name="user"),
    path('logout/', logout_user, name="logout")
    
]
