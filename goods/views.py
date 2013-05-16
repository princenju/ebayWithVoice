# Create your views here.
from goods.models import Goods
from django.http import HttpResponse
from bson.json_util import dumps

endpoint = "http://192.168.47.19:8080/"
def addGoods(request):
    goods=Goods()
    goods.name=request.GET['name']
    goods.description=request.GET['description']
    goods.picture1=open("tmp\\test1.png","rb")
    goods.picture2=open("tmp\\test2.png","rb")
    goods.picture3=open("tmp\\test3.png","rb")
    goods.price=250.38
#    goods.time=datetime.datetime.now
    goods.save()
    return HttpResponse("success")

def getGoods(request):
    gid=request.GET['id']
    goods=Goods.objects(pk=gid).first()
    result=goods.to_mongo()
    del(result['_types'])
    result['picture1']=endpoint+"goods/getPicture?id="+str(result['_id'])+"&&num=1"
    result['picture2']=endpoint+"goods/getPicture?id="+str(result['_id'])+"&&num=2"
    result['picture3']=endpoint+"goods/getPicture?id="+str(result['_id'])+"&&num=3"
    del(result['_cls'])
    del(result['_id'])
    return HttpResponse(dumps(result))

def getPicture(request):
    gid=request.GET['id']
    num=int(request.GET['num'])
    good=Goods.objects(pk=gid).first()
    if num==1:
        image=good.picture1.read()
    if num==2:
        image=good.picture2.read()
    if num==3:
        image=good.picture3.read()
    return HttpResponse(image,mimetype="image/jpeg")