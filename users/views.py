
from django.http import HttpResponse
from models import Account
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json  
from goods.models import Goods
from bson import json_util as ju
from users.models import Buy
#DBRef
endpoint = "http://192.168.47.19:8080/"
def login(request):
    data=request.raw_post_data
    jsonObject=json.loads(data)
    userName=jsonObject['username']
    passWord=jsonObject['password']
    user=auth.authenticate(username=userName, password=passWord)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            result=user.to_mongo()
            del(result['buylog'])
#            del(result['_id'])
            del(result['_types'])
            del(result['is_active'])
            del(result['is_superuser'])
            del(result['is_staff'])
            del(result['last_login'])
            del(result['_cls'])
            del(result['password'])
            del(result['friends'])
            del(result['date_joined'])
            result['portrait']=endpoint+"users/getPortrait?id="+str(result['_id'])
            del(result['_id'])
            return HttpResponse(ju.dumps(result))
        else:
            return HttpResponse("wrong user")
    else:
        return HttpResponse("invaild login")

#a method used for add data into database
def register(request):
    userName=request.GET['username']
    passWord=request.GET['password']
    test=Account.create_user(userName, passWord)
    test.portrait=open("C:\Users\\zinwang\\picture\\test.jpg","rb")
    test.save()
    return HttpResponse(str(test.to_mongo()))

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponse("success")

@login_required
def newPage(request):
    return HttpResponse(request.user.username)

@login_required
def addFriend(request):
    name=request.GET['username']
    friend=Account.objects(username=name).first()
    user=Account.objects(username=request.user.username).first()
    user.friends=user.friends+[str(friend.id)]
    user.save()
    request.user=user
    return HttpResponse("add success")

@login_required
def showFriends(request):
#    user=Account.objects(username=request.user.username).first()
    ids=request.user.friends
    friends=Account.objects(pk__in=ids).as_pymongo()
    return HttpResponse(friends)

def getPortrait(request):
    nid=request.GET['id']
    user=Account.objects(pk=nid).first()
    return HttpResponse(user.portrait.read()
                        ,mimetype="image/jpeg")
    
@login_required
def addGoods(request):
    gid=request.GET['id']
    good=Goods.objects(pk=gid).first()
    buylog=Buy()
    buylog.good=good
    request.user.buylog=request.user.buylog+[buylog]
    request.user.save()
    return HttpResponse("buy success")

@login_required
def getGoodsList(request):
    buylogs=request.user.to_mongo()['buylog']
    for buylog in buylogs:
#        buylog=buylog.to_mongo()
        del(buylog['_types'])
        del(buylog["_cls"])
        buylog["time"]=str(buylog["time"])
        name=Goods.objects(pk=buylog["good"].id).first().name
        buylog['name']=name
        buylog['id']="http://192.168.47.19:8080/goods/getGoods?id="+str(buylog["good"].id)
        del(buylog['good'])
    return HttpResponse(ju.dumps(buylogs))