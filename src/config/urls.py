from django.urls import path, include
from django.contrib import admin
from dashboard.views import dashboard_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('expenses/', include('expenses.urls')),
]
