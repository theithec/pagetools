import logging
logger = logging.getLogger('pagetoolpagetools')


def get_template_names_for_obj(obj, suffix=""):
    names = []
    node_type = getattr(obj, 'node_type', None)
    if node_type:
        names = [
            "sections/%s-%s%s.html" % (node_type, obj.slug, suffix),
            "sections/%s%s.html" % (node_type, suffix)
        ]
    names += [
        "sections/%s-%s%s.html" % (obj._meta.model_name, obj.slug, suffix),
        "sections/%s%s.html" % (obj._meta.model_name, suffix),
    ]
    logger.debug("Templates for %s: %s", obj, names)
    return names
