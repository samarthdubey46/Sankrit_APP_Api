
from django.contrib import admin
from django.urls import path, include
import users.url as userurls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(userurls))
]
