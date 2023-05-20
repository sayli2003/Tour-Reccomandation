from django.shortcuts import render,redirect
from . import user as u
import mysql.connector as sql
from . import databaseOp as db

def index(request):
    return render(request,'index2.html')
# Create your views here.
def home(request):
    ob=db.DBConn()
    context={}
    context["apriori"]=[]
    context["knn"]=[]
    context["user"]=u.userdets    
    if u.status==True:
        context["apriori"]=ob.user_recommendation()
        context["knn"]=ob.user_recommendation_rating_based()
    else:
        return redirect("/login")
    return render(request, 'index.html',context)

def profile(request):
    context={}
    ob=db.DBConn()
    context["user"]=u.userdets
    context["search_hist"]=ob.get_user_Search_History()
    context["searchcount"]=12
    print(context)
    return render(request,'userprofile.html',context)

def loginaction(request):
    if request.method == 'POST':
        if"signup" in request.POST:
            print("Signing up")
            em=request.POST['name']
            pwd=request.POST['phno']
            emial=request.POST['email']
            addr=request.POST['addr']
            ob=db.DBConn()
            ob.signupuser(em,pwd,emial,addr)
            val=ob.get_customer_verification(em,pwd)
            print(val)
            if val:
                u.status=True
                print(u.userdets)
                return redirect('/user')
        elif "signin" in request.POST:
            em=request.POST['name']
            pwd=request.POST['password']
            ob=db.DBConn()
            val=ob.get_customer_verification(em,pwd)
            print(val)
            if val:
                u.status=True
                print(u.userdets)
                return redirect('/user')
            else: 
                return render(request,'error.html')
    return render(request,'signuplogin.html')

def loggedin(request):
    if u.status == True:
        return redirect("/")
    else:
        return redirect("/login")
def packages(request):
    ob=db.DBConn()
    data={}
    if request.method=="POST":
        from_dest=request.POST['from']
        to_dest=request.POST['to']
        data["packages"]=ob.get_searched(from_dest,to_dest)
    else:
        data["packages"]=ob.get_close_packages()
    data["apriori"]=ob.user_recommendation()
    data["knn"]=ob.user_recommendation_rating_based()
    return render(request, 'Packages.html', data)
def dest(request):
    ob=db.DBConn()
    data={}
    if request.method == "POST":
        data["destination"]=ob.get_dest_searched(request.POST["state"],request.POST['dest_type'])
    return render(request,'destinations.html',data)
def packageDetails(request, pkid):
    ob=db.DBConn()
    d={}
    d["packages"]=ob.getpackage(pkid)
    d["Hotel"]=ob.get_hotels(d["packages"]["Dest"])
    d["Transport"]=ob.gettransport(pkid)
    d["destination"]=ob.get_dest(d["packages"]["Dest"])
    print(d["Hotel"])

    return render(request, 'packageDetails.html', d)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')