from mongoengine import Document
from mongoengine import StringField
from mongoengine import FloatField
from mongoengine import ListField
from mongoengine import ImageField
from mongoengine import EmbeddedDocument
# Create your models here.
class Goods(Document,EmbeddedDocument):
    name=StringField(max_length=140)
    description=StringField()
    prices=ListField(FloatField())
    picture=ImageField()
