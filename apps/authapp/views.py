from django.shortcuts import render, redirect
from . import models
from .froms import UserForm
from .froms import RegisterForm
from .froms import ForgetForm
import hashlib
from utils.email_send import send_register_email
from django.views import View
from django.contrib.auth import authenticate

# Create your views here.

def index(request):
    pass
    return render(request, 'index.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.MyUser.objects.get(username=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'authapp/login.html', locals())

    login_form = UserForm()
    return render(request, 'authapp/login.html', locals())


def create(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            mobile = register_form.cleaned_data['mobile']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'authapp/create.html', locals())
            else:
                same_name_user = models.MyUser.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'authapp/create.html', locals())
                same_mobile_user = models.MyUser.objects.filter(mobile=mobile)
                if same_mobile_user: #电话号码唯一
                    message = '该电话号码已被注册，请换一个号码！'
                    return render(request, 'authapp/create.html', locals())
                same_email_user = models.MyUser.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'authapp/create.html', locals())
                # 当一切都OK的情况下，创建新用户
                new_user = models.MyUser.objects.create()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.mobile = mobile
                new_user.email = email
                new_user.sex = sex
                new_user.is_active = False
                new_user.save()
                send_register_email(email, "create")
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'authapp/create.html', locals())


def logout(request):
    if not request.session.get('is_login', None):  # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect("/login/")

def ForgetPwd(request):
#    if request.session.get('is_login', None):
#        return redirect("/index/")
    if request.method == "POST":
        forget_form = ForgetForm(request.POST)
        #message = "请检查邮箱格式"
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            user_email = models.MyUser.objects.filter(email=email)
            if user_email:
                send_register_email(email, "forget")
                return redirect('/login/')
            else:
                message = "系统为找到该邮箱，请核对后输入！"
        #return render(request, 'authapp/login.html', locals())
    forget_form = ForgetForm()
    return render(request, 'authapp/forgetpwd.html', locals())


def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode()) # update方法只接收bytes类型
    return h.hexdigest()

def userinfo(requst):
    username = requst.GET.get("username")
    user ={}
    resdata = {}
    logger.debug("用户:%s,查询扩展信息." % (username))
    if (username is None):
        username = request.user.username
        user = User.objects.get(username=username)
        resdata = ResData('userinfo-rep', '0', True, '用户信息展示', user)
    else:
        user = models.MyUser.objects.get(username=username)
        if user is None:
            resdata = ResData('userinfo-rep', '0', False, '没有找到用户%s' % (username), '')
            logger.error("用户：%s，显示失败" % (username))
        else:
            resdata = ResData('userinfo-rep', '0', True, '用户信息展示', user)
    currentPage = PageInit('userinfo', resdata)
    return render(request, currentPage.template, currentPage.__dict__)