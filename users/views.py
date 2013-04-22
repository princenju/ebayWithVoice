
from django.http import HttpResponse
from models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required  

def login(request):
    user=auth.authenticate(username=request.GET['username'], password=request.GET['password'])
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
    test=User.create_user(userName, passWord, "wzn@wzn.com")
    test.save
    return HttpResponse(test.username)


def logout(request):
    auth.logout(request)
    return HttpResponse("success")

@login_required
def newPage(request):
    return HttpResponse(request.user.username)