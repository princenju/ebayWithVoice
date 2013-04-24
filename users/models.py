from mongoengine.django.auth import User
from mongoengine import StringField
from mongoengine import ListField
from mongoengine import ImageField
from bson.objectid import ObjectId
#from users.models import Account
# Create your models here.
class Account(User):
#    username = StringField(required=True)
#    password = StringField(max_length=50)
    friends=ListField(StringField())
    portrait=ImageField()

#ObjectId
