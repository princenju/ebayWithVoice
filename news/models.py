from mongoengine import Document, ReferenceField, CASCADE, StringField, ImageField, FileField, EmbeddedDocument
from users.models import Account
from mongoengine import ListField,EmbeddedDocumentField
# Create your models here.
class Comment(EmbeddedDocument):
    author = ReferenceField(Account)
    content = StringField(max_length=140)
    voice = FileField()

class News(Document):
    author = ReferenceField(Account, reverse_delete_rule=CASCADE)
    discription = StringField(max_length=140)
    picture = ImageField()
    voice = FileField()
    comments= ListField(EmbeddedDocumentField(Comment))
    

