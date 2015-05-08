from django.contrib.contenttypes.models import ContentType


def get_template_names_for_obj(obj):
    n =  ("cnodes/%s.html" % obj._meta.model_name)
    print("N",n)
    return n



