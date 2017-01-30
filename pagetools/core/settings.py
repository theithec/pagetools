from django.conf import settings


def _(x):
    return x


STATUS_CHOICES = getattr(settings, 'PT_STATUS_CHOICES', (
    ('draft', _('draft')),
    ('published', _('published')),
))
'''
Status values for :class: `pagetools.core.models.PublishedLangModel`
'''

STATUS_PUBLISHED = getattr(settings, 'PT_STATUS_PUBLISHED', 'published')
'''
Status key of content shown to everybody
'''
