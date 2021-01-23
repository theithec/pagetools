from django.conf import settings


def _(txt):
    return txt


STATUS_CHOICES = getattr(
    settings,
    "PT_STATUS_CHOICES",
    (
        ("draft", _("draft")),
        ("published", _("published")),
    ),
)
"""
Status values for :class: `pagetools.models.PublishedLangModel`
"""

STATUS_PUBLISHED = getattr(settings, "PT_STATUS_PUBLISHED", "published")
"""
Status key of content shown to everybody
"""

SUBMIT_BUTTON_CLASSES = getattr(settings, "PT_SUBMIT_BUTTON_CLASSES", "btn btn-primary button primary")
"""CSS classes for crsipy forms subbmit button. It seems the template pack i signored here"""
