from django.contrib.contenttypes.models import ContentType


def get_template_names_for_obj(obj):
    return ("cnodes/%s.html" % obj._meta.model_name)



