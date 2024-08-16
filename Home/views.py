from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser , GalleryImages
from django.contrib.auth import authenticate, login, logout
import uuid
from django.core.exceptions import ValidationError
from .decotrator import admin_only

@admin_only
def Index(request):
    return render(request,"index.html")

def generate_unique_id_number():
    return 'DSES'+ str(uuid.uuid4().hex[:5]).upper()


def SignUp(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        village = request.POST.get('village')
        district = request.POST.get('district')
        state = request.POST.get('state')
        address = request.POST.get('address')
        nomine = request.POST.get('nomine')
        relation = request.POST.get('relation')
        pnum = request.POST.get('pnum')
        email = request.POST.get('email')
        blood_group = request.POST.get("blood_group")
        idcard = request.POST.get("idcard")
        id_num = request.POST.get('id_num')
        pswd = request.POST.get('pswd')
        cpassword = request.POST.get('cpassword')

        if pswd != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
           
            if CustomUser.objects.filter(email = email ).exists():
                messages.info(request,"Email Id  Already exists...")
                return redirect("SignUp")
            else:
                user = CustomUser.objects.create(
                    email=email,
                    id_number=generate_unique_id_number(),
                    first_name=fname,
                    last_name=lname,
                    date_of_birth=dob,
                    village=village,
                    district=district,
                    state = state,
                    address=address,
                    nominee_name = nomine,
                    nominee_relation = relation,
                    id_card_type = idcard,
                    id_card_number = id_num,
                    phone_number=pnum,
                    blood = blood_group,   
                    is_active = True
                )
                user.set_password(pswd)
                user.save()
                
                messages.success(request, "User registered successfully.")
                return redirect('Registration_confirmation', pk = user.id)
        except ValidationError as e:
            messages.error(request, e.messages)
            return redirect('SignUp')

    # return redirect(SignUp, token = token)

    context = {
        
    }
    return render(request,'register.html',context)

def Registration_confirmation(request,pk):
    member = CustomUser.objects.get(id = pk)
    context ={
        "member":member
    }
    return render(request,"registration_confromation.html",context)

def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        pswd = request.POST['pswd']
        # try:
        user = authenticate(request,id_number = uname, password = pswd)
        if user is not None:
            user = login(request,user)
            return redirect('Index')
        else:
            messages.error(request,"username or password in correct")
            return redirect("SignIn")
        # except:
            # messages.error(request,"username or password in correct")
            # return redirect("SignIn")
    else:
        return render(request,"login.html")
    
def SignOut(request):
    logout(request)
    return redirect("Index")

def Gallery(request):
    gallery = GalleryImages.objects.all()
    context = {
        "gallery":gallery
    }
    return render(request,"gallery.html",context)

def AdminIndex(request):
    return render(request,"admin.html")


def Users(request):
    users = CustomUser.objects.all().exclude(is_superuser = True)
    context = {
        "users":users
    }
    return render(request,"admin_users.html",context)


def Gallery_admin(request):
    gallary = GalleryImages.objects.all()
    if request.method == "POST":
        caption = request.POST.get('caption')
        image = request.FILES.get('image')
        gallary = GalleryImages.objects.create(image_caption = caption,image = image )
        gallary.save()
        messages.success(request,"Image Added To Gallery")
        return redirect("Gallery_admin")
    context = {
        "gallary":gallary
    }
    return render(request,"admin_gallery.html",context)

def delete_gallery(request,pk):
    gallery = GalleryImages.objects.get(id = pk)
    gallery.image.delete()
    gallery.delete()
    return redirect("Gallery_admin")

def Membersingleview(request,pk):
    member = CustomUser.objects.get(id = pk)

    context = {
        "member":member
    }
    return render(request,"usersingleview.html",context)

def MemberSingleProfile(request):
    member = request.user
    context = {
        "member":member
    }
    return render(request,"usersingleview_self.html",context)
