from django.shortcuts import render,redirect
from . import admin as admin
from . import AdminRecommendation as rs
from .import models as db

global From_City
global From_State
global Dest
global days 
global season
global budget
# Create your views here.
def login(request):
    if request.method=="POST":
        em=request.POST['email']
        pwd=request.POST['password']        
        if em==admin.admin_log["Email"]:
            if pwd ==admin.admin_log["Password"]:
                admin.status=True
                return redirect("/admin/dash/")
            else:
                return render(request,"error.html")
        else:
            return render(request,"error.html")
        
    return render(request,'login_admin.html')

def dash(request):
    if admin.status == True :
        return render(request,'admin.html')
    else:
        return redirect('/admin/login/')

def logout(request):
    admin.status=False
    return redirect('/admin/login/')

def addpackage(request):
    global data
    if request.method=="POST":
        data["From_City"]=request.POST['F_City']
        data["From_State"]=request.POST['F_State']
        data["Dest"]=request.POST['Dest']
        data["day"]=request.POST['NoOfDays'] 
        data["season"]=request.POST['season']
        b=request.POST['Budget']
        if b=="High":
            data["budget"]=1
        if b=="Medium-High":
            data["budget"]=2
        if b=="Medium":
            data["budget"]=3
        if b=="Medium-Low":
            data["budget"]=4
        if b=="Low":
            data["budget"]=5    
        print(data)
        return redirect("predict")
    return render(request, 'addpackage.html')
    
def predict(request):
    context={}
    val=(rs.R_Admin(data["From_City"],data["From_State"],data["Dest"],int(data["day"]),data["season"],int(data["budget"])))
    if val == 'Excellent':
        context["message"]="The package will give a good yield and will be loved by the Customers"
    elif val == "Satisfactory":
        context["message"]= "The Package is Okay"
    else:
        context["message"]="The package is not satisfactory"
    
    if request.method == "POST":
        return redirect("/admin/msg/")

    return render(request,'pridict.html',context)

def msg(request):
    ob=db.DBConn()
    context={}
    val=ob.add_new_package(data["From_City"],data["From_State"],data["Dest"],int(data["day"]),data["season"],int(data["budget"]))
    if val==0:
        context["message"]="Cannot add to database there are no corresponding destination or hotels for stay"
    else:
        context["message"]="Successfully Added to the database"
    return render(request,'msg.html',context)


data={}