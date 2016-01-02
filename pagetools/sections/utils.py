import logging
logger = logging.getLogger('pagetoolpagetools')


def get_template_names_for_obj(obj):
    obj = obj.get_real_obj()
    n = []
    node_type = getattr(obj, 'node_type', None)
    if node_type:
        n = [
            "sections/%s-%s.html" % (node_type, obj.slug),
            "sections/%s.html" % (node_type)
        ]
    n += [
        "sections/%s-%s.html" % (obj._meta.model_name, obj.slug),
        "sections/%s.html" % obj._meta.model_name,
    ]
    logger.debug("Templates for %s: %s" % (obj, n))
    return n
