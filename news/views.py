# Create your views here.
from users.models import Account
from django.http import HttpResponse
from models import News,Comment
from django.contrib.auth.decorators import login_required
from bson.json_util import dumps
from goods.models import Goods
from bson.objectid import ObjectId
# TemporaryUploadedFile
# InMemoryUploadedFile
endpoint = "http://127.0.0.1:8000/"
@login_required
def addNews(request):
#    data=request.raw_post_data
#    jsonObject=json.loads(data)
    news = News()
    user = Account.objects(username='wzn').first()  # change to request.user
    news.author = user
#    news.discription = jsonObject['description']
#    news.picture = open(request.FILES['picture'].temporary_file_path(), "rb")
#    news.voice = open(request.FILES['voice'].temporary_file_path(), "rb")#change to data from request
    news.discription = "description"
    news.picture = open("tmp\\test.png", "rb")
    news.voice = open("tmp\\test.mp3", "rb")
    news.good = Goods.objects(pk="518746aee8384318b4ad5f8f").first()
    news.save()
    
    return HttpResponse(news.picture.read(), mimetype="image/jpeg")

@login_required
def getNewsList(request):
    # depend on the friends depart
    num = request.GET['num']
    allFriends = Account.objects(pk__in=request.user.friends).all()
    result = News.objects(author__in=allFriends)[int(num):int(num) + 15].as_pymongo()
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
        news['author'] = {"portrait": endpoint + "/users/getPortrait?id=" + str(user.pk), "name": user.username}
        news['comments'] = endpoint + "news/getComments?id=" + str(news['_id'])
        news['_id'] = endpoint + "news/getNewsDetail?id=" + str(news['_id'])
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
    voice = open("tmp\\test.mp3", "rb")  # change to data from request
    comment = Comment()
    comment.content = content
    comment.voice = voice
    comment.author = request.user
    news = News.objects(pk=nid).first()
    news.comments = news.comments + [comment]
    news.save()
    return HttpResponse("success")

@login_required()
def getComments(request):
    nid=request.GET['id']
    news=News.objects(pk=nid).as_pymongo()
    comments=list(news)[0]["comments"]
    for comment in comments:
        del(comment["_types"])
        del(comment["_cls"])
        uid=comment["author"]
        user = News.objects(author=uid).first().author
        comment["voice"]=endpoint + "news/getCommentVoice?vid="+str(comment["voice"])
        comment["username"]=user.username
        comment["portrait"]=endpoint+"users/getPortrait?id="+str(user.pk)
        del(comment["author"])
    return HttpResponse(dumps(comments))

@login_required()
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
