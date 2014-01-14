
class ConcretePublishableLangModel(PublishableLangModel):
    def __str__(self):
        return "%s:%s" % (self.lang, self.status)
