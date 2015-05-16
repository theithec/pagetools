from django.contrib.contenttypes.models import ContentType


def get_template_names_for_obj(obj):
    n = []
    try:
        n = ["cnodes/%s.html" % (obj.node_type)]
    except AttributeError:
        pass
    n +=  [
        "cnodes/%s-%s.html" % (obj._meta.model_name,obj.slug ),
        "cnodes/%s.html" % obj._meta.model_name,
    ]
    return n



