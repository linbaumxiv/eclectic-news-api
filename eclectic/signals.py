from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article, User
from .services import post_to_x

@receiver(post_save, sender=Article)
def disseminate_article(sender, instance, created, **kwargs):
    """
    Triggered whenever an Article is saved. 
    Handles Requirement #4 (Email/X logic) when an article is approved.
    """
    # Only act if the article is marked as approved
    if instance.is_approved:
        
        # 1. Identify Subscribers (Journalist followers OR Publication subscribers)
        # We use 'followed_by' and 'reader_subscribers' related_names from our new models
        journalist_subscribers = instance.author.followed_by.all()
        
        publisher_subscribers = []
        if instance.publisher:
            publisher_subscribers = instance.publisher.reader_subscribers.all()

        # Combine both lists and remove duplicates using a set
        recipients = set(list(journalist_subscribers) + list(publisher_subscribers))
        
        # Extract emails safely
        recipient_emails = [u.email for u in recipients if u.email]

        if recipient_emails:
            try:
                # 2. Send Newsletter via Email
                send_mail(
                    subject=f"New Article: {instance.title}",
                    message=(
                        f"Read the latest from {instance.author.username}:\n\n"
                        f"{instance.content[:200]}..."
                    ),
                    from_email="noreply@eclecticnews.com",
                    recipient_list=recipient_emails,
                    fail_silently=False,
                )
            except Exception as e:
                # Defensive coding: prevents email failures from breaking the app
                print(f"Error sending email: {e}")

        # 3. Disseminate to X (Twitter) via Service logic
        try:
            article_url = f"http://127.0.0.1:8000/api/articles/{instance.id}/"
            post_to_x(instance.title, article_url)
        except Exception as e:
            print(f"Error posting to X: {e}")