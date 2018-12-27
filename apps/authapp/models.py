from django.db import models
import datetime

# Create your models here.
class MyUser(models.Model):
    """
    用户表
    """
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    mobile = models.CharField(u'手机', max_length=32,default=None,blank=True,null=True)
    department = models.CharField(u'部门', max_length=32, default=None, blank=True, null=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    is_active= models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.username

class EmailVerifyRecord(models.Model):
    """
    邮箱验证码表
    """
    register = "register"
    forget = "forget"
    send_type_choices = (
        (register, "注册"),
        (forget, "找回密码"),
    )
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, unique=True, verbose_name="邮箱")
    send_type = models.CharField(max_length=8, choices=send_type_choices, verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.code, self.email)