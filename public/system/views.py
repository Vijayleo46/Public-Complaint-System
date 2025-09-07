from django.db.models import Q

from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

from . models import Complaint, ComplaintImage, Department, DepartmentActivity, User, Place, PublicUser,Message, Rating, RuleRegulation, Staff, UploadWork, Work

# Create your views here.
from django.contrib.auth.models import User ,Group 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password

def home(request):
    return render(request,'home.html')

def adminhome(request):
    return render(request,'adminhome.html')

def phome(request):
    return render(request,"publichome.html")




def user(request):
    if 'submit' in request.POST:
        a=request.POST['username']
        b=request.POST['password']
        try:
            o=authenticate(request,username=a,password=b)
            login(request,o)
        except:
            return HttpResponse("<script>alert('invalid username and password!');window.location='/login'</script>")
        try:
            o=User.objects.get(username=a,password=b)
            if o.groups.filter(name='admin').exists():
                return HttpResponse("<script>alert('Admin was Logged successfully!');window.location='/adminhome'</script>")
            elif o.groups.filter(name='public').exists():
                request.session['pid'] = o.id
                return HttpResponse("<script>alert('Logged in successfully!');window.location='/publichome'</script>")
            elif o.groups.filter(name='department').exists():
                request.session['did'] = o.id
                return HttpResponse("<script>alert('Logged in successfully!');window.location='/depthome'</script>")
            elif o.groups.filter(name='staff').exists():
                request.session['sid'] = o.id
                return HttpResponse("<script>alert('Logged in successfully!');window.location='/staffhome'</script>")
            else:
                return HttpResponse("<script>alert('incorrect username and password!');window.location='/login'</script>")
                
        except User.DoesNotExist:
            return render(request,'login.html',{'error':'Invalid Username or password'})
        
    return render(request,"login.html")


def puser(request):
    if 'submit' in request.POST:
        a=request.POST['fname']
        b=request.POST['lname']
        c=request.POST['hname']
        d=request.POST['phone']
        e=request.POST['email']
        f=request.POST['username']
        g=request.POST['password']
        o=User.objects.create(username=f,password=g)
        o.groups.add(Group.objects.get(name='public'))
        p=PublicUser(first_name=a,last_name=b,house_name=c,phone=d,email=e,login_id=o.pk,place_id=o.pk)
        p.save()
        return HttpResponse("<script>alert('Regstration Successfully!');window.location='/login'</script>")
    return render(request,'register.html')




def manage(request):
    ma=Place.objects.all()
    if 'submit' in request.POST:
        a=request.POST['placename']
        b=request.POST['placedescription']
        c=request.POST['pincode']
        ew=Place(place_name=a,place_description=b,pincode=c)
        ew.save()
        return HttpResponse("<script>alert('places added!');window.location='/admanageplace'</script>")
    return render(request,"admanageplace.html",{'m':ma})

def updatema(request,id):
    w=Place.objects.get(id=id)
    ma=Place.objects.all()
    if 'update' in request.POST:
        w.place_name=request.POST['placename']
        w.place_description=request.POST['placedescription']
        w.pincode=request.POST['pincode']
        w.save()
        return HttpResponse("<script>alert('Updated the details!');window.location='/admanageplace'</script>")
    return render(request,"admanageplace.html",{'a':w,'m':ma})

    
def deletema(reqeuest,id):
    w=Place.objects.get(id=id)
    w.delete()
    return HttpResponse("<script>alert('Deleted the Details!');window.location='/admanageplace'</script>")

def depmanage(request):
    ad=Department.objects.all()
    if 'submit' in request.POST:
        a=request.POST['deptname']
        b=request.POST['phone']
        c=request.POST['email']
        d=request.POST['description']
        e=request.POST['username']
        f=request.POST['password']
        o=User.objects.create(username=e,password=f)
        o.groups.add(Group.objects.get(name='department'))
        de=Department(dept_name=a,phone=b,email=c,description=d,login_id=o.pk,place_id=o.pk)
        de.save()
        return HttpResponse("<script>alert('Department added!');window.location='/admanadept'</script>")
    return render(request,"admanadept.html",{'o':ad})

def updatedp(request,id):
    dq=Department.objects.get(id=id)
    ad=Department.objects.all()
    if 'update' in request.POST:
        dq.dept_name=request.POST['deptname']
        dq.phone=request.POST['phone']
        dq.emaio=request.POST['email']
        dq.description=request.POST['description']
        dq.save()
        return HttpResponse("<script>alert('Updated the details!');window.location='/admanadept'</script>")
    return render(request,"admanadept.html",{'h':dq,'o':ad})

    
def deletedp(request,id):
    we=Department.objects.get(id=id)
    we.delete()
    return HttpResponse("<script>alert('Deleted the Details!');window.location='/admanadept'</script>")


def phome(request):
    return render(request,"publichome.html")


def viewpub(request):
    g=PublicUser.objects.all()
    return render(request,"adviewpub.html",{'p':g})

def deptho(request):
    return render(request,"depthome.html")


def reply(request):
    d=request.session['did']
    u=Department.objects.get(login_id=d)
    o = Complaint.objects.filter(dept_id=u.id)
    if 'submit' in request.POST:
        i=request.POST['reply']
        id=request.POST['id']
        c=Complaint(id=id)
        c.reply=i
        c.save()
        return HttpResponse("<script>alert('replied');window.location='/depviewcompl'</script>")
    return render(request,"depviewcompl.html",{'cm':o})



def viewreview(request):
    w=request.session['did']
    e=Department.objects.get(login_id=w)
    r=Rating.objects.filter(dept_id=e.id)
    print('ggggg',w)
    return render(request,"viewreview.html",{'s':r})

def rules(request):
    r=RuleRegulation.objects.all()  
    if 'submit' in request.POST:
        a=request.POST['title']
        b=request.POST['description']
        re=RuleRegulation(title=a,description=b)
        re.save()
        return HttpResponse("<script>alert('Rules and Regulation added!');window.location='/manrules'</script>")
    return render(request,"manrules.html",{'re':r})

def updateru(request,id):
    ar=RuleRegulation.objects.get(id=id)
    ra=RuleRegulation.objects.all()
    if 'update' in request.POST:
        ar.title=request.POST['title']
        ar.description=request.POST['description']
        ar.save()
        return HttpResponse("<script>alert('Updated the details!');window.location='/manrules'</script>")
    return render(request,"manrules.html",{'r':ar,'re':ra})

    
def deleteru(reqeuest,id):
    ar=RuleRegulation.objects.get(id=id)
    ar.delete()
    return HttpResponse("<script>alert('Deleted the Details!');window.location='/manrules'</script>")

def viewrules(request):
    h=RuleRegulation.objects.all()
    return render(request,"viewrules.html",{'e':h})
    
def viewdepte(request):
    a=request.session['pid']
    ag=Department.objects.all()
    # i=DepartmentActivity.objects.filter(dept_id=ag.id)
    
    return render(request,"viewdept.html",{'q':ag})

# def viewdepte(request):
#     a=request.session['pid']
#     ag=Department.objects.get(login_id=a)
#     i=DepartmentActivity.objects.filter(dept_id=ag.id)
    
#     return render(request,"viewdept.html",{'q':i})

def activi(request,id):
    
    c=DepartmentActivity.objects.filter(dept_id=id)
    # q=request.session['did']
    # dd=Department.objects.get(login_id=q)
    # ui=DepartmentActivity.objects.filter(dept_id=dd.id)
    print(c)
    return render(request,"activity.html",{'u':c})

def rating(request,id):
    ra=Department.objects.get(id=id)
    login_id =request.session['pid']
    z=PublicUser.objects.get(login_id=login_id)
    a=Rating.objects.filter(user_id=z,dept_id=id)

    if 'submit' in request.POST:
        a=request.POST['review']
        b=request.POST['ratings']
     
        ri=Rating(review_description=a,rated_value=b,rating_date=datetime.now(),user_id=z.pk,dept_id=ra.pk) 
        ri.save()
        return HttpResponse("<script>alert('Rating Added');window.location='/viewdept'</script>")
    return render(request,"publicrating.html",{'h':a})

def updaterate(request,id):
    r=Rating.objects.get(id=id)
    rr=Rating.objects.all()
    if 'update' in request.POST:
        r.review_description=request.POST['review']
        r.rated_value=request.POST['ratings']
        r.save()
        return HttpResponse("<script>alert('Rating Updated!');window.location='/viewdept'</script>")
    return render(request,"publicrating.html",{'h':rr,'u':r})

def deleterate(request,id):
    r=Rating.objects.get(id=id)
    r.delete()
    return HttpResponse("<script>alert('Rating Updated!');window.location='/viewdept'</script>")
    
        
def viewcomplaint(request):
    i=request.session['pid']
    re=PublicUser.objects.get(login_id=i)
    ai=Complaint.objects.filter(user_id=re.id)
    return render(request,"viewpubli.html",{'o':ai})


def message(request,id):
    users=User.objects.all()
    departments=Department.objects.all()
    d=Message.objects.filter(receiver_type='public',receiver_id=id)
    if 'submit' in request.POST:
        
        c = request.POST['message']
        de=Message(receiver_type='public',receiver_id=id,message=c,date=datetime.now())
        de.save()
        return HttpResponse("<script>alert('send message!');window.location='/vius'</script>")
    return render(request,"adminmessage.html",{'user':users,'departments':departments,'d':d})

def deleteemsg(request,id):
    g=Message.objects.get(id=id)
    g.delete()
    return HttpResponse("<script>alert('Message Deleted!');window.location='/vius'</script>")
    

def vius(request):
    users=PublicUser.objects.all()  
    return render(request,"um.html",{'u':users})


def viewmessagee(request):
    login_id = request.session['pid']
    user = PublicUser.objects.get(login_id=login_id)
    public_messages = Message.objects.filter(receiver_type='public', receiver_id=user.id)
    return render(request, "publicmsgview.html", {'e': public_messages})




def staff(request):
    a=request.session['did']
    s=Department.objects.get(login_id=a)
    st=Staff.objects.filter(dept_id=s.id)
    if 'submit' in request.POST:
        a=request.POST['fname']
        b=request.POST['lname']
        c=request.POST['place']
        d=request.POST['phone']
        e=request.POST['email']
        f=request.POST['username']
        g=request.POST['password']
        o=User.objects.create(username=f,password=g)
        o.groups.add(Group.objects.get(name='staff'))
        ew=Staff(firstname=a,lastname=b,place=c,phone=d,email=e,dept_id=s.id,login_id=o.pk)
        ew.save()
        return HttpResponse("<script>alert('Staff added!');window.location='/managestaff'</script>")
    return render(request,"managestaff.html",{'o':st})

def updatesta(request,id):
    se=Staff.objects.get(id=id)
    
    if 'update' in request.POST:
        se.firstname=request.POST['fname']
        se.lastname=request.POST['lname']
        se.place=request.POST['place']
        se.phone=request.POST['phone']
        se.email=request.POST['email']
        se.save()
        return HttpResponse("<script>alert('Updated the details!');window.location='/managestaff'</script>")
    return render(request,"managestaff.html",{'s':se})

    
def deletesta(reqeuest,id):
    w=Staff.objects.get(id=id)
    w.delete()
    return HttpResponse("<script>alert('Deleted the Details!');window.location='/managestaff'</script>")
  
def staffHome(request):
    return render(request,"staffhome.html")


def viewcompre(request):
    a=request.session['did']
    s=Department.objects.get(login_id=a)
    ce=Complaint.objects.filter(dept_id=s.id)
    if 'submit' in request.POST:
        r=request.POST['reply']
        id=request.POST['id']
        o=Complaint.objects.get(id=id)
        o.reply = r
        o.save()
        return HttpResponse("<script>alert('replied');window.location='/depviewcompl'</script>")
    return render(request,"depviewcompl.html",{'r':ce})

def manageact(request):
    d=request.session['did']
    de=Department.objects.get(login_id=d)
    da=DepartmentActivity.objects.filter(dept_id=de.id)
    if 'submit' in request.POST:
        a=request.POST['title']
        b=request.POST['description']
        dept_id=d
        ac=DepartmentActivity(title=a,description=b,activity_date=datetime.now(),dept_id=de.id)
        ac.save()
        return HttpResponse("<script>alert('Activity added!');window.location='/manageactivity'</script>")
    return render(request,"manageactivity.html",{'c':da})

def updateact(request,id):
    se=DepartmentActivity.objects.get(id=id)
    ma=DepartmentActivity.objects.all()
    if 'update' in request.POST:
        se.title=request.POST['title']
        se.description=request.POST['description']
        se.save()
        return HttpResponse("<script>alert('Updated the details!');window.location='/manageactivity'</script>")
    return render(request,"manageactivity.html",{'d':se,'c':ma})

    
def deleteact(reqeuest,id):
    w=DepartmentActivity.objects.get(id=id)
    w.delete()
    return HttpResponse("<script>alert('Deleted the Details!');window.location='/manageactivity'</script>")

def viewrate(request):
    dept=request.session['did']
    dep=Department.objects.get(login_id=dept)
    r=Rating.objects.filter(dept=dep)
    return render(request,"deprate.html",{'f':r})

def deptviewmsgeee(request):
    
    d=Message.objects.filter(receiver_type='department')
    return render(request,"deptviewmsg.html",{'g':d})

def publicviewmsgeee(request):
    
    messeges=Message.objects.filter(receiver_type='public')
    return render(request,"publicmsgview.html",{'e':messeges})




def staffreview(request):
    s=request.session['sid']
    h =Staff.objects.get(login_id=s)
    e =Rating.objects.filter(dept_id=h.dept.pk)
    return render(request,"stviewrate.html",{'z':e})



def postcompp(request,id):
    y=request.session['pid']
    re=PublicUser.objects.get(login_id=y)
    s=Complaint.objects.filter(Q(dept_id=id, user_id=re.id, complaint_type='private')|Q(dept_id=id, complaint_type='public'))
    if 'submit' in request.POST:
       d=request.POST['complaint_type']
       a=request.POST['title']
       b=request.POST['description']

    #    dept_id=dep.id
       user_id=re.id
       od=Complaint(complaint_type=d,title=a,description=b,date_time=datetime.now(),dept_id=id,user_id=re.id)
       od.save()
       return HttpResponse("<script>alert('added complaint');window.location='/viewdept'</script>")
    
    return render(request,"postcomp.html",{'s':s})

def upcom(request,id):
    ci=Complaint.objects.get(id=id)
    if 'update' in request.POST:
       ci.complaint_type=request.POST['complaint_type']
       ci.title=request.POST['title']
       ci.description=request.POST['description']
       ci.save()
       return HttpResponse("<script>alert('Update Complaint!');window.location='/viewdept'</script>")
    return render(request,"postcomp.html",{'co':ci})
    

def delecom(request,id):
    co=Complaint.objects.get(id=id)
    co.delete()
    return HttpResponse("<script>alert('Deleted Complaint!');window.location='/viewdept'</script>")

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import Complaint, ComplaintImage, Department
from datetime import datetime

def img(request, id):
    complaint = Complaint.objects.get(id=id)
    user_login_id = request.session['did']
    department = Department.objects.get(login_id=user_login_id)
    all_complaints = Complaint.objects.filter(dept_id=department.id)
    images = ComplaintImage.objects.filter(complaint_id=id)
    
    if 'submit' in request.POST:
        uploaded_image = request.FILES['img']
        fs = FileSystemStorage()
        saved_path = fs.save(uploaded_image.name, uploaded_image)
        
        new_image = ComplaintImage(path=saved_path, date_time=datetime.now(), complaint_id=complaint.id)
        new_image.save()
        return HttpResponse("<script>alert('Added image!');window.location='/viewdept'</script>")
    
    return render(request, "uploaddimg.html", {'f': all_complaints, 'di': images})

def updateimg(request, id):
    image_obj = ComplaintImage.objects.get(id=id)
    if 'update' in request.POST:
        uploaded_image = request.FILES['img']
        fs = FileSystemStorage()
        saved_path = fs.save(uploaded_image.name, uploaded_image)
        
        image_obj.path = saved_path
        image_obj.save()
        return HttpResponse("<script>alert('Updated image!');window.location='/viewdept'</script>")
    
    return render(request, "uploaddimg.html", {'f': image_obj, 'j': image_obj})


def deleimg(request,id):
    de=ComplaintImage.objects.get(id=id)
    de.delete()
    return HttpResponse("<script>alert('Deleted image!');window.location='/viewdept'</script>")
    
def staffcomplaints(request):
    s=request.session['pid']
    a=PublicUser.objects.get(login_id=s)
    co=Complaint.objects.filter(user_id=a.id)
    if 'submit' in request.POST:
        com=request.POST['reply']
        id=request.POST['id']
        o=Complaint.objects.get(id=id)
        o.reply=com
        o.save()
        return HttpResponse("<script>alert('replied');window.location='/staffcomp'</script>")
    return render(request,"staffcomp.html",{'co':co})


def viewactivity(request):
    s=request.session['sid']
    d=Staff.objects.get(login_id=s)
    g=DepartmentActivity.objects.filter(dept_id=d.dept.pk)
    print(s,d,g)
    return render(request,"staffviewact.html",{'ac':g})

def pviewact(request):
    a=request.session['did']
    s=Department.objects.get(login_id=a)
    g=DepartmentActivity.objects.filter(dept_id=s.id)
    return render(request,"pubviewact.html",{'af':g})

def addwork(request):
    u=request.session['did']    
    d=Department.objects.get(login_id=u)
    e=Staff.objects.filter(dept_id=d.id)
    q=e.values_list('id',flat=True)
    print(u)
    ww=Work.objects.filter(staff_id__in=q)
    if 'submit' in request.POST:
        b = request.POST['work']
        z = request.POST['st']
        c = request.POST['description']
        # dept_id=d.id
       
        w=Work(work=b,description=c,date=datetime.now(),staff_id=z)
        w.save()
        return HttpResponse("<script>alert('add the staff!');window.location='/addwork'</script>")
    return render(request,"addwork.html",{'s':ww,'f':e})

def upadd(request,id):
    w=Work.objects.get(id=id)
    u=request.session['did']    
    d=Department.objects.get(login_id=u)
    e=Staff.objects.filter(dept_id=d.id)

    if 'update' in request.POST:
        
        w.work=request.POST['work']
        w.staff_id = request.POST['st']
        w.description=request.POST['description']
        w.save()
        return HttpResponse("<script>alert('Updated the work!');window.location='/addwork'</script>")
    return render(request,"addwork.html",{'d':w, 'f':e})

def deleadd(request,id):
    w=Work.objects.get(id=id)
    w.delete()
    return HttpResponse("<script>alert('Deleted the work!');window.location='/addwork'</script>")


# def viewupload(request,id):
#     # se=request.session['sid']
#     # i=Staff.objects.get(login_id=se)
#     # we=Work.objects.filter(staff_id=id)
#     # q=we.values_list('id',flat=True)
    
#     w=UploadWork.objects.filter(work_id=id) 
#     if 'submit' in request.POST:
#         c = request.FILES['path']   
#         fs=FileSystemStorage()
#         saved_path=fs.save(c.name,c)
#         file_path=fs.url(saved_path)
#         uo=UploadWork(filepath=saved_path,date=datetime.now(),work_id=id)
#         uo.save()
#         return HttpResponse("<script>alert('added work');window.location='/viewworkstaf'</script>")
#     return render(request,"uploadwork.html", {'a':w,'ww':w,'di':w}) 

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from .models import UploadWork  # Make sure this is correctly imported

def viewupload(request, id):
    uploaded_files = UploadWork.objects.filter(work_id=id)

    if  'submit' in request.POST:
        uploaded_file = request.FILES['path']
        if uploaded_file:
            fs = FileSystemStorage()
            saved_path = fs.save(uploaded_file.name, uploaded_file)
            upload_entry = UploadWork(filepath=saved_path, date=datetime.now(), work_id=id)
            upload_entry.save()
            return HttpResponse("<script>alert('Work uploaded successfully');window.location='/viewworkstaf'</script>")

    return render(request, "uploadwork.html", {
        'ww': uploaded_files
    })


def updatefile(request,id):
    ww=UploadWork.objects.get(id=id)
    # i=Staff.objects.get(login_id=se)
    # we=Work.objects.filter(staff_id=i.pk)
    # w=UploadWork.objects.all() 
    if 'update' in request.POST:                    
        file=request.FILES['path'] 
        fs=FileSystemStorage()
        saved_path=fs.save(file.name,file)
        ww.filepath=saved_path
        ww.save()
        return HttpResponse("<script>alert('update work');window.location='/viewworkstaf'</script>")
    return render(request,"uploadwork.html", {'g':ww})
 
def deletefile(request,id):
    ww=UploadWork.objects.get(id=id)
    ww.delete()
    return HttpResponse("<script>alert('delete work');window.location='/viewworkstaf'</script>")
 

def viewstaffwork(request):
    s=request.session['sid']
    f=Staff.objects.get(login_id=s)
    g=Work.objects.filter(staff_id=f.pk)
    return render(request,"viewworkstaf.html",{'p':g})


def msg(request,id):
    users=User.objects.all()
    departments=Department.objects.all()
    o=Message.objects.filter(receiver_type='department',receiver_id=id)
    if 'submit' in request.POST:
        c = request.POST['message']
        de=Message(receiver_type='department',receiver_id=id,message=c,date=datetime.now())  
        de.save()
        return HttpResponse("<script>alert('send message!');window.location='/de'</script>")
    return render(request,"departmsg.html",{'user':users,'departments':departments,'a':o})

# def updatemsg(request,id):
#     p=Message.objects.get(id=id)
#     o=Message.objects.all()
#     if 'update' in request.POST:
#         p.message = request.POST['message']
#         p.save()
#         return HttpResponse("<script>alert('update message!');window.location='/de'</script>")
#     return render(request,"departmsg.html",{'a':o,'a':o})

def deletemsg(request,id):
    p=Message.objects.get(id=id)
    p.delete()  
    return HttpResponse("<script>alert('Deleted message!');window.location='/de'</script>")
      
        
        
        
def dpmsg(request):
    dept=Department.objects.all() 
    return render(request,"de.html",{'k':dept})



def viewworkde(request, wd, st):
    g = UploadWork.objects.filter(work_id=wd)
    return render(request, "viewworkdept.html", {'u': g})


def logout2(request):
    return render(request,"home.html")

def adsolve(request):
    g=Complaint.objects.all()
    return render(request,"adsolve.html",{'un':g})

