
from django.http import HttpResponse
from models import Account
from django.contrib import auth
from django.contrib.auth.decorators import login_required  

def login(request):
    user=auth.authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponse("success")
        else:
            return HttpResponse("wrong user")
    else:
        return HttpResponse("invaild login")

#a method used for add data into database
def register(request):
    userName=request.GET['username']
    passWord=request.GET['password']
    test=Account.create_user(userName, passWord)
    test.portrait=open("E:\picture\\test1.jpg","rb")
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
    name=request.POST['username']
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

@login_required
def getPortrait(request):
    return HttpResponse(request.user.portrait.read(),mimetype="image/jpeg")