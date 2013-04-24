from mongoengine import Document
from mongoengine import StringField
from mongoengine import FloatField
from mongoengine import ListField
from mongoengine import ImageField
# Create your models here.
class Goods(Document):
    name=StringField(max_length=140)
    description=StringField()
    prices=ListField(FloatField())
    picture=ImageField()