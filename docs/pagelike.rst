.. _pagelike

========
Pagelike
========

The abstract :class:`pagetools.core.models.PagelikeModel` inherits from
`django-model-utils: StatusModel
<http://django-model-utils.readthedocs.io/en/latest/models.html#statusmodel>`_
and
`django-model-utils: TimeStampedModel
<http://django-model-utils.readthedocs.io/en/latest/models.html#timestampemodel>`_.
It also has a:

- `title`
- `description` (for meta tag/seo)
- `lang`

and a :class:`pagetools.core.models.PublishableLangManager` with one new method: ``lfilter``,
which returns published content for the current language (or for the keyword argument `lang`).
Content is published if it's status is the same as ``pagetools.core.settings.STATUS_PUBLISHED``, which must be one of
 ``pagetools.core.settings.STATUS_CHOICES``, defaults are "draft" and "published".

The :class:`pagetools.core.admin.PagelikeAdmin` adds tinymce to media and applies it to all textfields.

