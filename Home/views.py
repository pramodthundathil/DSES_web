from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser , GalleryImages
from django.contrib.auth import authenticate, login, logout
import uuid
from django.core.exceptions import ValidationError
from .decotrator import admin_only, Access_Control
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

import base64
from django.core.files.base import ContentFile

@admin_only
def Index(request):
    return render(request,"index.html")

def generate_unique_id_number():
    while True:
        id_num = 'DSES' + get_random_string(length=5, allowed_chars='0123456789')
        if not CustomUser.objects.filter(id_number=id_num).exists():
            return id_num  # Break the loop and return the unique ID number


def SignUp(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        guardian = request.POST.get("guardian")
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
            if CustomUser.objects.filter(phone_number = pnum ).exists():
                messages.info(request,"This Phone number is Already exists...")
                return redirect("SignUp")
            else:
                profile_pic_data = request.POST.get('profile_pic')

        # Decode the image data and save it to the model
                if profile_pic_data:
                    format, imgstr = profile_pic_data.split(';base64,')
                    ext = format.split('/')[-1]
                    profile_pic = ContentFile(base64.b64decode(imgstr), name=f'{fname}_{lname}.{ext}')
                else:
                    profile_pic = None
                user = CustomUser.objects.create(
                    email=email,
                    id_number=generate_unique_id_number(),
                    first_name=fname,
                    last_name=lname,
                    guardian = guardian,
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
                    is_active = True,
                    profile_pic=profile_pic,
                )
                user.set_password(pswd)
                user.save()
                try:
                    email = email
                    mail_subject = 'DSES Account was created'
                    path = "SignUp"
                    message = render_to_string('emailbody.html', {'user': user,
                                                                      
                                                                        })

                    email = EmailMessage(mail_subject, message, to=[email])
                    email.send(fail_silently=True)
                except:
                    pass
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
@Access_Control
@login_required(login_url='SignIn')
def AdminIndex(request):
    user_num = CustomUser.objects.all().count()
    gallery_num = GalleryImages.objects.all().count()
    context = {
        "user_num":user_num,
        "gallery_num":gallery_num
    }
    return render(request,"admin.html",context)

@Access_Control
@login_required(login_url='SignIn')
def Users(request):
    users = CustomUser.objects.all().exclude(is_superuser = True)
    context = {
        "users":users
    }
    return render(request,"admin_users.html",context)

@Access_Control
@login_required(login_url='SignIn')
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

@Access_Control
@login_required(login_url='SignIn')
def delete_gallery(request,pk):
    gallery = GalleryImages.objects.get(id = pk)
    gallery.image.delete()
    gallery.delete()
    
    return redirect("Gallery_admin")

@Access_Control
@login_required(login_url='SignIn')
def Disable_user(request,pk):
    user = CustomUser.objects.get(id = pk)
    if user.is_active == False:
        user.is_active = True
        user.save()
        messages.success(request,"User Activated")
    else:
        user.is_active = False
        user.save()
        messages.success(request,"User Disabled")

    return redirect("Users")


@Access_Control
@login_required(login_url='SignIn')
def IssueIdCard(request,pk):
    return redirect("Membersingleview", pk = pk)

def Active_members_list(request):
    users = CustomUser.objects.filter(is_active = True)
    context = {
        "users":users
    }
    return render(request,"list_of_activeusers.html",context)

def Inctive_members_list(request):
    users = CustomUser.objects.filter(is_active = False)
    context = {
        "users":users
    }
    return render(request,"list_of_inaciveusers.html",context)

@Access_Control
@login_required(login_url='SignIn')
def Membersingleview(request,pk):
    member = CustomUser.objects.get(id = pk)

    context = {
        "member":member
    }
    return render(request,"usersingleview.html",context)

@login_required(login_url='SignIn')
def MemberSingleProfile(request):
    member = request.user
    context = {
        "member":member
    }
    return render(request,"usersingleview_self.html",context)

@login_required(login_url='SignIn')
def DESS_INFO(request):
    return render(request,'dess_details.html')


def Messageing(request):
    users = CustomUser.objects.all()
    if request.method =="POST":
        selected_contacts = request.POST.getlist('contact_id')
        subjuct = request.POST.get("sub_name")
        message = request.POST.get("message")
        print(selected_contacts, subjuct, message)
        email = []
        for item in selected_contacts:
            member = CustomUser.objects.get(id = int(item))
            email.append(member.email)

        try:
            email = email
            mail_subject = subjuct
            message = render_to_string('emailbody_message.html', {'message': message,
                                                            "user": member,
                                                            "subjuct":subjuct
                                                                
                                                                })

            email = EmailMessage(mail_subject, message, to=email)
            email.send(fail_silently=True)
        except:
            pass

        return redirect("Messageing")
    context = {
        "users":users
    }
    return render(request,"messageing.html",context)
