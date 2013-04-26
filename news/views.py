# Create your views here.
from users.models import Account
from django.http import HttpResponse
from models import News
from django.contrib.auth.decorators import login_required
from news.models import Comment
from bson.json_util import dumps

@login_required
def addNews(request):
    news = News()
    user = Account.objects(username='wzn').first()#change to request.user
    news.author = user
    news.discription = "hhhhhhhh"#change to data from request
    news.picture = open("E:\picture\\test.jpg", "rb")#change to data from request
    news.voice = open("E:\music\\test\\CD8\\test.wav", "rb")#change to data from request
    news.save()
    return HttpResponse("success")

@login_required
def getNewsList(request):
    #depend on the friends depart
    num = request.GET['num']
    allFriends = Account.objects(pk__in=request.user.friends).all()
    result = News.objects(author__in=allFriends)[int(num):int(num) + 15].as_pymongo()
    result = list(result)
    for news in result:
        del(news['_types'])
        del(news['_cls'])
        news['picture'] = "http://192.168.47.19:8080/news/getPicture?id=" + str(news['_id'])
        news['voice'] = "http://192.168.47.19:8080/news/getVoice?id=" + str(news['_id'])
        uid = news['author']
        user = News.objects(author=uid).first().author
        news['author'] = {"portrait": "http://192.168.47.19:8080/users/getPortrait?id=" + str(user.pk), "name": user.username}
        news['comments']=len(news['comments'])
        news['_id']="http://192.168.47.19:8080/news/getNewsDetail?id=" + str(news['_id'])
    result = dumps(result)
    return HttpResponse(result)

def getPicture(request):
    nid = request.GET['id']
    result = News.objects(pk=nid).first()
    image = result.picture.read()
    return HttpResponse(image, mimetype="image/jpeg")

def getVoice(request):
    nid = request.GET['id']
    result = News.objects(pk=nid).first()
    voice = result.voice.read()
    return HttpResponse(voice, mimetype="audio/mpeg")

@login_required
def addComment(request):
    nid = request.GET['id']
    content = request.GET['content']
    voice = open("E:\music\\test\\CD8\\test.wav", "rb")#change to data from request
    comment = Comment()
    comment.content = content
    comment.voice = voice
    comment.author = request.user
    news = News.objects(pk=nid).first()
    news.comments = news.comments + [comment]
    news.save()
    return HttpResponse("success")

def deleteNews(request):
    News.objects(author=request.user).delete()
    return HttpResponse("delete all")
