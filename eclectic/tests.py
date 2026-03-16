from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User, Article, Journalist, Publisher


class EclecticNewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # 1. Setup Users
        self.journalist = User.objects.create_user(username='writer', role='journalist', password='password')
        self.editor = User.objects.create_user(username='editor_boss', role='editor', password='password')
        self.reader = User.objects.create_user(username='reader_user', role='reader', password='password')
        
        # 2. Setup Publisher
        self.publisher = Publisher.objects.create(name="Tech Times")
        
        # 3. Setup Article
        self.article = Article.objects.create(
            title="API Design", 
            content="Normalisation matters.", 
            author=self.journalist,
            publisher=self.publisher,
            is_approved=False
        )

    def test_unapproved_article_hidden_from_feed(self):
        """Test 1: Readers should not see unapproved articles in their feed."""
        self.reader.subscribed_journalists.add(self.journalist)
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(reverse('article-feed'))
        self.assertEqual(len(response.data), 0)

    def test_journalist_cannot_approve_own_article(self):
        """Test 2: Defensive check - Journalists cannot self-approve articles via API."""
        self.client.force_authenticate(user=self.journalist)
        url = reverse('article-detail', args=[self.article.id])
        # Attempt to flip the approval switch
        response = self.client.patch(url, {'is_approved': True})
        self.article.refresh_from_db()
        self.assertFalse(self.article.is_approved)

    def test_subscription_feed_filtering(self):
        """Test 3: Feed only shows articles from subscribed journalists."""
        self.article.is_approved = True
        self.article.save()
        
        # Reader is NOT subscribed yet
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(reverse('article-feed'))
        self.assertEqual(len(response.data), 0)
        
        # Now Reader subscribes
        self.reader.subscribed_journalists.add(self.journalist)
        response = self.client.get(reverse('article-feed'))
        self.assertEqual(len(response.data), 1)

    def test_editor_approval_permissions(self):
        """Test 4: Editors have the permission to approve articles."""
        self.client.force_authenticate(user=self.editor)
        url = reverse('article-detail', args=[self.article.id])
        response = self.client.patch(url, {'is_approved': True})
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertTrue(self.article.is_approved)

#Test API 
class ArticleAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a Reader
        self.reader = User.objects.create_user(username='reader_user', password='password', role='reader')
        # Create a Journalist & Article
        self.journalist = User.objects.create_user(username='reporter', password='password', role='journalist')
        self.article = Article.objects.create(
            title="Breaking News", 
            author=self.journalist, 
            is_approved=True
        )
        # Subscribe the reader
        self.reader.subscribed_journalists.add(self.journalist)

    def test_feed_returns_correct_articles(self):
        self.client.force_authenticate(user=self.reader)
        url = reverse('article-feed') # Matches your @action name
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Breaking News")