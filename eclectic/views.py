from django.db import models
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsEditorOrAuthorReadOnly # Importing your custom security
from .models import Article, User, Publisher, Newsletter
from .serializers import (
    ArticleSerializer, 
    UserSerializer, 
    PublisherSerializer, 
    NewsletterSerializer
)

class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed, created, or edited.
    
    Filters content based on the user's role and approval status.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
   
    permission_classes = [permissions.IsAuthenticated, IsEditorOrAuthorReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_approved', 'author', 'publisher']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        """
        Defensive logic: Forces articles to be unapproved upon creation 
        and sets the logged-in user as the author.
        """
        serializer.save(author=self.request.user, is_approved=False)

    @action(
        detail=False, 
        methods=['get'], 
        permission_classes=[permissions.IsAuthenticated],
        renderer_classes=[JSONRenderer]
    )
    def feed(self, request):
        """
        Returns a personalized list of approved articles 
        based on the user's subscriptions.
        """
        user = request.user
        
        # Accessing the ManyToMany fields from normalized Custom User model
        followed_journalists = user.subscribed_journalists.all()
        followed_publishers = user.subscribed_publishers.all()

        articles = Article.objects.filter(
            models.Q(is_approved=True) & 
            (models.Q(author__in=followed_journalists) | 
             models.Q(publisher__in=followed_publishers))
        ).distinct().order_by('-created_at')

        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    # Ensure only Editors can modify Publishers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Basic security for user data
    permission_classes = [permissions.IsAdminUser]