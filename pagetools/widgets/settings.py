from django.conf import settings


def _(_x):
    return _x


AREAS = getattr(settings, 'PT_AREAS',
                (('sidebar', _('Sidebar'),),)
                )

TEMPLATETAG_WIDGETS = getattr(settings, 'PT_TEMPLATETAG_WIDGETS', {})
