from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils import timezone

# --- 1. Custom User Model ---
# Note: We inherit from AbstractUser to replace the default Django user.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')

    # Requirement: Fields for Readers (Subscriptions)
    # Using 'self' for journalist subscriptions since Journalists are now Users.
    subscribed_publishers = models.ManyToManyField(
        'Publisher', 
        blank=True, 
        related_name='reader_subscribers'
    )
    subscribed_journalists = models.ManyToManyField(
        'self', 
        blank=True, 
        symmetrical=False, 
        limit_choices_to={'role': 'journalist'},
        related_name='followed_by'
    )

    def save(self, *args, **kwargs):
        """
        Handles group assignment and role-based field resetting.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Logic: Assign to Group based on role
        group, created = Group.objects.get_or_create(name=self.role.capitalize())
        self.groups.add(group)

        # Requirement: If NOT a reader, set reader fields to None/Empty
        if self.role != 'reader':
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()

    def __str__(self):
        return f"{self.username} ({self.role})"


# --- 2. Publisher Model ---
class Publisher(models.Model):
    """
    Can have multiple editors and journalists.
    """
    name = models.CharField(max_length=255, unique=True)
    editors = models.ManyToManyField(
        User, 
        limit_choices_to={'role': 'editor'}, 
        related_name='managed_publishers'
    )
    journalists = models.ManyToManyField(
        User, 
        limit_choices_to={'role': 'journalist'}, 
        related_name='publisher_affiliations'
    )

    def __str__(self):
        return self.name


# --- 3. Article Model ---
class Article(models.Model):
    """
    Includes approval workflow and connections to authors/publishers.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'journalist'},
        related_name='articles_published'
    )
    publisher = models.ForeignKey(
        Publisher, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='articles'
    )
    
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-set published_at when approved
        if self.is_approved and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# --- 4. Newsletter Model ---
class Newsletter(models.Model):
    """
    Requirement: Journalists can create these independently.
    """
    subject = models.CharField(max_length=255)
    body = models.TextField()
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'journalist'},
        related_name='newsletters_published'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject