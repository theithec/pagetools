from django.conf import settings

MAILFORM_RECEIVERS = getattr(settings,
                             'PT_MAILFORM_RECEIVERS',
                             [a[1] for a in settings.ADMINS]
                             )

MAILFORM_SENDER = getattr(settings,
                          'PT_MAILFORM_SENDER',
                          'form@localhost'
                          )
# It seems crispy_forms Auto Submit does not use the template pack
SUBMIT_BUTTON_CLASSES = getattr(settings,
                                "PT_SUBMIT_BUTTON_CLASSES",
                                "btn btn-primary button primary"
                                )
