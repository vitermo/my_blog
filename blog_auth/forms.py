from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    """定义注册帐号的form组件"""
    username = forms.CharField(
        label="用户名",
        max_length=18,
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
            "max_length": "用户名最长不超过18位"
        },
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        min_length=6,
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
            "min_length": "密码不能少于6位"
        }
    )

    password2 = forms.CharField(
        min_length=6,
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
            "min_length": "密码不能少于6位"
        }
    )

    email = forms.CharField(
        label="邮箱",
        error_messages={
            "required": "内容不能为空",
            "invalid": "格式错误",
        },
        validators=[RegexValidator(r"^\w+@\w+\.com$", "邮箱格式不正确")]
    )

    # phone = forms.CharField(
    #     label="电话",
    #     error_messages={
    #         "required": "内容不能为空",
    #         "invalid": "格式错误",
    #     },
    #     validators=[RegexValidator(r"^[0-9]{4,11}$", "请输入正确的号码")]
    # )

    class Meta:
        model = User
        fields = ('username','email')

    # 定义局部钩子
    def clean_password(self):
        # 校验密码的合法性，不能为纯数据
        password = self.cleaned_data.get("password")
        if password.isdecimal():
            raise ValidationError("密码不能为纯数字！")
        return password

    def clean_password2(self):
        # 校验密码的合法性，不能为纯数据
        r_password = self.cleaned_data.get("password2")
        if r_password.isdecimal():
            raise ValidationError("密码不能为纯数字！")
        return r_password

    # 定义全局钩子
    def clean(self):
        # 校验两次密码输入是否一致
        if self.cleaned_data.get("password") != self.cleaned_data.get("password2"):
            self.add_error("password2", "两次密码输入不一致！")
        else:
            return self.cleaned_data

    # 重写init方法，来批量设置标签的样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})