import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from accounts.models import CustomUser


def generate_slugs():
    users = CustomUser.objects.filter(slug__isnull=True)
    print(f"Generating slugs for {users.count()} users...")

    for user in users:
        # The save method will automatically generate the slug
        user.save()
        print(f"Generated slug '{user.slug}' for user {user.email}")

    print("Slug generation complete!")


if __name__ == "__main__":
    generate_slugs()
