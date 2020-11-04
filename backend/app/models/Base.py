from mongoengine import Document

class Base(Document):
    """
    每次都写get_base_info好烦
    """
    meta = {'allow_inheritance': True}

    def get_base_info(self):
        return dict(
            [(k, v) for k, v in vars(self).items() if k[:1] != '_'] +
            [("id", str(self.id))]
        )
