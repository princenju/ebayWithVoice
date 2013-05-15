# Create your views here.
from users.models import Account
from django.http import HttpResponse
from models import News,Comment
from django.contrib.auth.decorators import login_required
from bson.json_util import dumps
from goods.models import Goods
from bson.objectid import ObjectId
import urlparse
#from cgi import log
# TemporaryUploadedFile
# InMemoryUploadedFile
endpoint = "http://192.168.47.19:8080/"
@login_required
def addNews(request):
    url=request.POST['url']
    news = News()
    user = request.user  # change to request.user
    news.author = user
    news.picture = open(request.FILES['picture'].temporary_file_path(), "rb")
    news.voice = open(request.FILES['voice'].temporary_file_path(), "rb")#change to data from request
    result=urlparse.urlparse(url)
    params=urlparse.parse_qs(result.query,True)
    gid=params['id']
    news.good = Goods.objects(pk=gid[0]).first()
    news.save()
    return HttpResponse("success")

@login_required
def getNewsList(request):
    # depend on the friends depart
    num = request.GET['num']
    allFriends = Account.objects(pk__in=request.user.friends).all()
    number = News.objects(author__in=allFriends).count()
    if int(num)*15>number:
        result=[]
        return HttpResponse(dumps(result))
    result = News.objects(author__in=allFriends)[int(num*15):int(num)*15 + 15].order_by("-time").as_pymongo()
    result = list(result)
    for news in result:
        del(news['_types'])
        del(news['_cls'])
        news['picture'] = endpoint + "news/getPicture?id=" + str(news['_id'])
        news['voice'] = endpoint + "news/getVoice?id=" + str(news['_id'])
        uid = news['author']
        user = News.objects(author=uid).first().author
        gid = news['good']
        good = News.objects(good=gid).first().good
        news['good'] = endpoint + "goods/getGoods?id=" + str(good.pk)
        news['author'] = {"portrait": endpoint + "users/getPortrait?id=" + str(user.pk), "name": user.username}
        news['comments'] = endpoint + "news/getComments?id=" + str(news['_id'])
#        news['_id'] = endpoint + "news/getNewsDetail?id=" + str(news['_id'])
        del(news['_id'])
        news['time']=str(news['time'])
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
    result=urlparse.urlparse(request.POST['comment_url'])
    params=urlparse.parse_qs(result.query,True)
    nid=params['id']
    comment = Comment()
    comment.content =""
    if request.POST.has_key("content"):
        content = request.POST['content']
        comment.content = content
    if request.FILES.has_key("voice"):
        voice =open(request.FILES['voice'].temporary_file_path(), "rb")  # change to data from request
        comment.voice = voice
    comment.author = request.user
    news = News.objects(pk=nid[0]).first()
    news.comments = news.comments + [comment]
    news.save()
    return HttpResponse("success")

#@login_required()
def getComments(request):
    nid=request.GET['id']
    news=News.objects(pk=nid).as_pymongo()
    comments=list(news)[0]["comments"]
    for comment in comments:
        del(comment["_types"])
        del(comment["_cls"])
        uid=comment["author"]
        user = News.objects(author=uid).first().author
        if comment["voice"]!=None:
            comment["voice"]=endpoint + "news/getCommentVoice?vid="+str(comment["voice"])
        else:
            comment["voice"]=""
        comment["username"]=user.username
        comment["portrait"]=endpoint+"users/getPortrait?id="+str(user.pk)
        del(comment["author"])
    return HttpResponse(dumps(comments))

def getCommentVoice(request):
    vid=request.GET['vid']
    a=News.objects(comments__voice=ObjectId(str(vid))).first()
    comments=a.comments
    voice=None
    for comment in comments:
        mongo=comment.to_mongo()
        if str(mongo['voice'])==str(vid):
            voice=comment.voice
    return HttpResponse(voice.read(),mimetype="audio/mpeg")
    
def deleteNews(request):
    News.objects(author=request.user).delete()
    return HttpResponse("delete all")
