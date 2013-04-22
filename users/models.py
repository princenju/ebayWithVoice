from mongoengine.django.auth import User
from mongoengine import StringField
# Create your models here.
class User(User):
#    username = StringField(required=True)
#    password = StringField(max_length=50)
    email=StringField(max_length=50)