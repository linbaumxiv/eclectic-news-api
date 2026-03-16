"""
URL configuration for eclectic_news project.
Routes are organized modularly using the REST Framework Router.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from eclectic.views import ArticleViewSet, PublisherViewSet, UserViewSet

# 1. Create a router and register our viewsets.
# This modular approach handles all GET/POST/PUT/DELETE routes automatically.
router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'publishers', PublisherViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    # All API routes will start with /api/ (e.g., /api/articles/)
    path('api/', include(router.urls)), 
    
    # Optional: include login for the browsable API
    path('api-auth/', include('rest_framework.urls')),
]

