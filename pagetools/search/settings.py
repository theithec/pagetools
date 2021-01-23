from django.conf import settings

SEARCH_REPLACEMENTS = getattr(settings, "PT_SEARCH_REPLACEMENTS", True)


SEARCH_REPLACEMENTS_FILE = getattr(settings, "PT_SEARCH_REPLACEMENTS_FILE ", "search_replacements.json")
