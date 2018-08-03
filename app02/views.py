from django.shortcuts import render,redirect

from functools import wraps
def check_login(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        ret =request.session.get('islogin')
        if ret == '2':
            return func(request,*args,**kwargs)
        else:
            next = request.path_info
            return redirect('/app02/login/?next={}'.format(next))
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
                ret = redirect('/app02/home/')
            # ret.set_cookie('islogin','1',max_age=7)
            request.session['islogin'] = '2'
            request.session['user'] = name
            return ret
        else:
            return redirect('/app02/login/')
    return render(request,'app02/login.html')
@check_login
def home(request):
    user = request.session.get('user')
    return render(request, 'app02/home.html',{'user':user})
@check_login
def index(request):
    return render(request,'app02/index.html')

def dele(request):
    request.session.flush()

    return redirect('/app02/login/')