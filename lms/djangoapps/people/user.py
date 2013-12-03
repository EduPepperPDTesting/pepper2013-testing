from django_sphinx_db.backend.models import SphinxModel, SphinxField

class User(SphinxModel):
    class Meta:
        # This next bit is important, you don't want Django to manage
        # the table for this model.
        managed = False

    user_name = SphinxField()
    first_name = SphinxField()
    id = SphinxField()
    
