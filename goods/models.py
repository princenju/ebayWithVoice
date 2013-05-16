from mongoengine import Document
from mongoengine import StringField
from mongoengine import FloatField
from mongoengine import ImageField
from mongoengine import EmbeddedDocument
# Create your models here.
class Goods(Document,EmbeddedDocument):
    name=StringField(max_length=140)
    description=StringField()
    price=FloatField()
    picture1=ImageField()
    picture2=ImageField()
    picture3=ImageField()
