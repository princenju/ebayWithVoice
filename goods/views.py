# Create your views here.
from goods.models import Goods
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
def addGoods(request):
    goods=Goods()
    goods.name=request.GET['name']
    goods.description=request.GET['description']
    goods.picture=open("E:\picture\\test.jpg","rb")
#    goods.time=datetime.datetime.now
    goods.save()
    return HttpResponse("success")

@login_required
def getGoods(request):
    gid=request.GET['id']
    goods=Goods.objects(pk=gid).first()
    result=json.dumps(str(goods.to_mongo()))
    s=json.loads(result)
    return HttpResponse(s)

@login_required
def getPicture(request):
    gid=request.GET['id']
    image=Goods.objects(pk=gid).first().picture.read()
    return HttpResponse(image,mimetype="image/jpeg")