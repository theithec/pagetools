from django.conf import settings


AVAIL_NODES = getattr(settings, 'PT_AVAIL_NODES',
        (('page', 'Page'),
        ('section', 'Section'),
        ('content', 'Content'),
        #('product', 'Product'),
        #('product-landing', 'Product-Landing'),
        #('round-icons', 'Round Icons Row'),
        #('angular-icons', 'Angular Icons Row'),
        #('slider', 'Slider'),
        # ('text', 'Text'),
        # ('image', 'Image'),
        # ('video', 'Movie'),
        )
    )

