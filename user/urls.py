from django.urls import path, include
# dj rest auth is registered as an app in our django settings
# config and such we can use this notation to include the views
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls'))
]
