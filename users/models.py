from mongoengine.django.auth import User,EmbeddedDocument
from mongoengine import StringField
from mongoengine import ListField
#from users.models import Account
# Create your models here.
class Account(User,EmbeddedDocument):
#    username = StringField(required=True)
#    password = StringField(max_length=50)
    email=StringField(max_length=50)
    friends=ListField(StringField())


