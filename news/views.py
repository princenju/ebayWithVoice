# Create your views here.
from users.models import Account
from django.http import HttpResponse
from models import News
from django.contrib.auth.decorators import login_required
from news.models import Comment

@login_required
def addNews(request):
    news=News()
    user= Account.objects(username='wzn').first()#change to request.user
    news.author=user
    news.discription="hhhhhhhh"#change to data from request
    news.picture=open("E:\picture\\test.jpg","rb")#change to data from request
    news.voice=open("E:\music\\test\\CD8\\test.wav","rb")#change to data from request
    news.save()
    return HttpResponse("success")

@login_required
def getNewsList(request):
    #depend on the friends depart
    result=News.objects(author=request.user).all()
    return HttpResponse(result.as_pymongo())

@login_required
def getPicture(request):
    nid=request.GET['id']
    result=News.objects(pk=nid).first()
    image=result.picture.read()
    return HttpResponse(image,mimetype="image/jpeg")

@login_required   
def getVoice(request):
    nid=request.GET['id']
    result=News.objects(pk=nid).first()
    voice=result.voice.read()
    return HttpResponse(voice,mimetype="audio/mpeg")

@login_required
def addComment(request):
    nid=request.GET['id']
    content=request.POST['content']
    voice=open("E:\music\\test\\CD8\\test.wav","rb")#change to data from request
    comment=Comment()
    comment.content=content
    comment.voice=voice
    comment.author=request.user
    news=News.objects(pk=nid).first()
    news.comments=news.comments+[comment]
    news.save()
    return HttpResponse("success")

def deleteNews(request):
    News.objects(author=request.user).delete()
    return HttpResponse("delete all")