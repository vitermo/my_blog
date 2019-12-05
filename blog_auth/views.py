from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import forms
from .models import User
from django.contrib.auth.models import User
from .forms import UserLoginForm,UserRegisterForm

# Create your views here.

# 用户登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)

        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # print(data)
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request,user)
                return redirect('blog_index')
            else:
                return HttpResponse('账户名或者密码错误，请重新输入～')
        else:
            return HttpResponse('账户或密码不合法！')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form':user_login_form}
        return render(request,'blog_auth/login.html',context)
    else:
        return HttpResponse('请求方式不合法！')

# 删除
@login_required(login_url='blog_auth/login')
def user_delete(request,id):

    User.objects.filter(id=id).delete()

    return redirect("blog_index")

# 退出
def user_logut(request):
    logout(request)
    return redirect('blog_index')

# 注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():  # 验证提交数据的合法性
            valid_data = user_register_form.cleaned_data
            username = valid_data.get("username")
            # 判断帐号是否已存在
            if User.objects.filter(username=username):
                # 如果存在，给form中的username字段添加一个错误提示。
                user_register_form.add_error("username", "帐号已存在")
                return render(request, "blog_auth/register.html", {"user_register_form": user_register_form})
            else:
                # 帐号可用，去掉多余密码，在数据库创建记录
                del valid_data["password2"]
                new_user = User.objects.create_user(**valid_data)  # 创建普通用户
                login(request,new_user)
                return redirect("blog_index")
        else:
            # 数据验证不通过，返回页面和错误提示，保留数据
            return render(request, "blog_auth/register.html", {"user_register_form": user_register_form})
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'blog_auth/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")