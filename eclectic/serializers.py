from rest_framework import serializers
from .models import User, Publisher, Article, Newsletter

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'editors', 'journalists']

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.
    
    Converts Article database records into JSON format for API consumption.
    Includes custom validation to ensure authors are only journalists.
    """
    author_name = serializers.ReadOnlyField(source='author.username')
    publisher_name = serializers.ReadOnlyField(source='publisher.name')

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 'author_name', 
            'publisher', 'publisher_name', 'is_approved', 'published_at'
        ]

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'subject', 'body', 'creator', 'created_at']