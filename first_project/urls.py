from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('register/', include('users.urls')),
    path('admin/', admin.site.urls),
]
