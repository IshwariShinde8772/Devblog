import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_main.settings')
django.setup()

from assignments.models import About, SocialLink
from django.contrib.auth.models import User

def sync_data():
    print("Syncing backend data with perfected frontend content...")

    # 1. Update About Us info
    about_text = "DevBlog is a modern publishing platform where technology meets creativity. We provide deep dives into software architecture, frontend elegance, and the evolving digital landscape, helping developers build more meaningful web experiences."
    about, created = About.objects.get_or_create(id=1, defaults={
        'about_heading': 'About DevBlog',
        'about_description': about_text
    })
    if not created:
        about.about_heading = 'About DevBlog'
        about.about_description = about_text
        about.save()
    print("✓ About Us section updated.")

    # 2. Update Social Links
    social_data = [
        ('Facebook', 'https://facebook.com'),
        ('Github', 'https://github.com'),
        ('Linkedin', 'https://linkedin.com'),
    ]
    
    # Clear and recreate to avoid duplicates and ensure order
    SocialLink.objects.all().delete()
    for platform, link in social_data:
        SocialLink.objects.create(platform=platform, link=link)
    print("✓ Social links (Facebook, Github, Linkedin) synchronized.")

    # 3. Ensure Admin exists with the known password
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Superuser 'admin' created.")
    else:
        u = User.objects.get(username='admin')
        u.set_password('admin123')
        u.is_superuser = True
        u.is_staff = True
        u.save()
        print("✓ Superuser 'admin' password and permissions refreshed.")

    print("\nSUCCESS: All frontend content data is now securely saved to the backend database!")

if __name__ == "__main__":
    sync_data()
