from django.shortcuts import render, redirect,  HttpResponse
from .TodoForms import TodoForm
from api_app.models import Data
from django.contrib.auth.models import User
import requests
import json
from django.contrib import messages

def returnToken(Cookies):
    isnotAccess = 0
    if  Cookies.get("access") != None:
        token = {
            "token" : Cookies.get("access")
        }
    else:
        isnotAccess = 1
        token = {
            "token" : Cookies.get("refresh")
        }
    yield token
    yield isnotAccess

def isAuthenticated(request, path, isRender): #isAuthenticated
    if  request.COOKIES.get("refresh") == None: 
        return False
    tokenEndpoint = request.META["HTTP_HOST"]
    tokenObject = returnToken(request.COOKIES)
    token = next(tokenObject)
    isValid =  requests.post(f"http://{tokenEndpoint}/api/verify/", json=token) #checking if token is Valid
    if isValid.status_code != 200:
        return False
    if next(tokenObject) == 1: #next(tokenObject) its the isnotAccess flag
        if isRender:            
            httpResponse = render(request,path) 
        else:
            httpResponse = redirect(path) 
        newAccess = requests.post(f"http://{tokenEndpoint}/api/refresh/", json={ "refresh" : token["token"]  }) 
        newAccess = newAccess.json()
        httpResponse.set_cookie("access", newAccess["access"])
        return httpResponse
    if isRender:
        return render(request,path)
    return redirect(path)


def setTokens(request,tokenEndpoint,creds):
    getTokens = requests.post(f"{tokenEndpoint}/api/token/", json=creds)
    if getTokens.status_code != 200:
        messages.success(request, 'account not found')
        return render(request,  "login.html", {})
    getTokens = getTokens.json()
    httpResponse = redirect("/home")
    httpResponse.set_cookie("refresh", getTokens["refresh"])
    httpResponse.set_cookie("access", getTokens["access"])
    return httpResponse

def login(request):
    if isAuthenticated(request,"/home", False) != False:
        return isAuthenticated(request,"/home", False)
    if request.method == "POST":
        if request.POST.get('button_clicked') == "signin":
            return redirect("/signin")
        login_data = request.POST.dict()
        creds = {
            "username" : login_data.get("username"),
            "password" : login_data.get("password"), 
        }
        httpResponse = setTokens(request, request.META["HTTP_ORIGIN"], creds) # request.META["HTTP_ORIGIN"] = 127.0.0.1:8000
        return httpResponse
    return render(request, "login.html", {})

def homepage(request):
    if isAuthenticated(request, "/login", False) == False:
        return redirect("/login")
    if request.method == "POST":
        httpResponse = redirect("/login")
        httpResponse.delete_cookie("refresh") # deleting cookies on logout
        httpResponse.delete_cookie("access")
        httpResponse.delete_cookie("sessionid")
        return httpResponse
    httpResponse = isAuthenticated(request, "home.html", True)
    return httpResponse

def signin(request):
    if isAuthenticated(request,"/home", False) != False:
        return isAuthenticated(request,"/home", False)
    if request.method == "POST":
        myform = TodoForm(request.POST)
        if  myform.is_valid():
            try:
                newuser = User.objects.create_user(
                username = myform.cleaned_data["username"],
                email = myform.cleaned_data["email"],
                password = myform.cleaned_data["password"],)
                creds = {
                    "username" : myform.cleaned_data["username"],
                    "password" : myform.cleaned_data["password"]
                }
                httpResponse = setTokens(request, request.META["HTTP_ORIGIN"], creds)
                return httpResponse
            except:
                return HttpResponse("User already exists")
        return HttpResponse("404")
    else:
        myform = TodoForm()
    return render(request, "signin.html", {"myform" : myform})