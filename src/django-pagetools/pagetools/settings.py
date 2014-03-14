from django.conf import settings


STATUS_CHOICES = getattr(settings, 'PT_STATUS_CHOICES', (
    ('draft', 'draft'),
    ('published', 'published'),
))
STATUS_PUBLISHED = getattr(settings, 'PT_STATUS_PUBLISHED', 'published')

ADMIN_SET_LANG_FILTER = getattr(settings, 'PT_ADMIN_SET_LANG_FILTER', True)
