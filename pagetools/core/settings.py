from django.conf import settings
_ = lambda x: x

STATUS_CHOICES = getattr(settings, 'PT_STATUS_CHOICES', (
    ('draft', _('draft')),
    ('published', _('published')),
))
STATUS_PUBLISHED = getattr(settings, 'PT_STATUS_PUBLISHED', u'published')

