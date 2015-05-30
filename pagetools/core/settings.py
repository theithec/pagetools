from django.conf import settings
_ = lambda x: x


'''status-values for pagetools.core.models.PubLangModel'''
STATUS_CHOICES = getattr(settings, 'PT_STATUS_CHOICES', (
    ('draft', _('draft')),
    ('published', _('published')),
))

'''status-key of content shown to everybody'''
STATUS_PUBLISHED = getattr(settings, 'PT_STATUS_PUBLISHED', 'published')

