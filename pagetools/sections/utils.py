import logging
logger = logging.getLogger('pagetoolpagetools')


def get_template_names_for_obj(obj, suffix=""):
    obj = obj.get_real_obj()
    n = []
    node_type = getattr(obj, 'node_type', None)
    if node_type:
        n = [
            "sections/%s-%s%s.html" % (node_type, obj.slug, suffix),
            "sections/%s%s.html" % (node_type, suffix)
        ]
    n += [
        "sections/%s-%s%s.html" % (obj._meta.model_name, obj.slug, suffix),
        "sections/%s%s.html" % (obj._meta.model_name, suffix),
    ]
    logger.debug("Templates for %s: %s", (obj, n))
    return n
