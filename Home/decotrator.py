from django.shortcuts import redirect, render


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