import logging
from django.contrib.contenttypes.models import ContentType
logger = logging.getLogger('sections')


def get_template_names_for_obj(obj):
    obj = obj.get_real_obj()
    n = []
    try:
        n = ["sections/%s.html" % (obj.node_type)]
    except AttributeError:
        pass
    n +=  [
        "sections/%s-%s.html" % (obj._meta.model_name,obj.slug ),
        "sections/%s.html" % obj._meta.model_name,
    ]
    #logger.error("TEMPL "+ ", ".join( n))
    return n



