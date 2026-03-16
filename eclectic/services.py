"""
Modular services for external platform integrations.
This module handles communication with third-party APIs like X (Twitter).
"""
import tweepy
from django.conf import settings

def post_to_x(title, article_url):
    """
    Handles logic for posting to X. Uses defensive coding to check for 
    placeholder keys and handles API runtime errors gracefully.
    """
    # 1. Defensive Check: Identify if we are in 'Simulation Mode'
    # This prevents the app from crashing if keys aren't set up yet.
    if "your-key" in settings.X_API_KEY or not settings.X_API_KEY:
        print(f"--- SIMULATION MODE ---")
        print(f"Tweet Content: New Article: {title}")
        print(f"Link: {article_url}")
        return True

    # 2. Real API Logic
    try:
        # X API v2 (Required for newer Developer Accounts)
        client = tweepy.Client(
            consumer_key=settings.X_API_KEY,
            consumer_secret=settings.X_API_SECRET,
            access_token=settings.X_ACCESS_TOKEN,
            access_token_secret=settings.X_ACCESS_TOKEN_SECRET
        )
        
        tweet_text = f"New Article: {title}\nRead more: {article_url}"
        
        # This is the actual unit of work
        client.create_tweet(text=tweet_text)
        
        print(f"SUCCESS: Article '{title}' posted to X.")
        return True

    except tweepy.TweepyException as e:
        # Defensive coding: Catch specific API errors without crashing the server
        print(f"API ERROR: X dissemination failed. Technical details: {e}")
        return False
    except Exception as e:
        # Catch-all for unexpected runtime errors
        print(f"UNEXPECTED ERROR in services.py: {e}")
        return False