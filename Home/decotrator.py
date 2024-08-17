from django.shortcuts import redirect, render, HttpResponse


def admin_only(view_fun):
    def wrapper_fun(request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser == True:
                return redirect("AdminIndex")
            else:
                return view_fun(request,*args,**kwargs)
        else:
            return view_fun(request,*args,**kwargs)
    return wrapper_fun


def Access_Control(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_superuser == True:
            return view_func(request,*args,**kwargs)
        else:
            return HttpResponse("<h1 style='text-align:center;color:red'>You dont have permission to view this page<h1><a style='text-align:center;color:green' href='/'>Go back</a>")
    return wrapper_func
