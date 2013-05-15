from mongoengine.django.auth import User
from mongoengine import StringField
from mongoengine import ListField
from mongoengine import ImageField
from mongoengine import EmbeddedDocumentField
from goods.models import Goods
from mongoengine import EmbeddedDocument
import datetime
from mongoengine import DateTimeField
from mongoengine import ReferenceField
#from users.models import Account
# Create your models here.
class Buy(EmbeddedDocument):
    good=ReferenceField(Goods)
    time=DateTimeField(default=datetime.datetime.now)

class Account(User):
#    username = StringField(required=True)
#    password = StringField(max_length=50)
    friends=ListField(StringField())
    portrait=ImageField()
    buylog=ListField(EmbeddedDocumentField(Buy))
#ObjectId
