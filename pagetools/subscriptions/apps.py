from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    name = "pagetools.subscriptions"
    verbose_name = "Subscriptions"

    from .forms import SubscribeForm

    subscribe_form = SubscribeForm
