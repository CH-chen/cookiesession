from django.shortcuts import render,redirect

from functools import wraps
def check_login(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        # ret =request.COOKIES.get('islogin','0')
        ret =request.get_signed_cookie('islogin',default='0',salt='jkl')
        if ret == '2':
            return func(request,*args,**kwargs)
        else:
            next = request.path_info
            return redirect('/login/?next={}'.format(next))
    return inner
def login(request):
    print(request.get_full_path())
    print(request.path_info)
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        next = request.GET.get('next')
        if name == 'abc' and pwd == '123':
            if next:
                ret = redirect(next)
            else:
                return redirect('/home/')
            # ret.set_cookie('islogin','1',max_age=7)
            ret.set_signed_cookie('islogin','2', salt='jkl')
            return ret
        else:
            return redirect('/login/')
    return render(request,'login.html')
def home(request):
    # cook = request.COOKIES.get('islogin',0)
    cook = request.get_signed_cookie('islogin',default='0',salt='jkl')
    if cook == '2':
        print('转入home')
        return render(request, 'home.html')
    else:
        return redirect('/login/')
@check_login
def index(request):
    return render(request,'index.html')

def dele(request):
    ret = redirect('/login/')
    ret.delete_cookie('islogin')

    return ret
