import random

from django.core.mail import send_mail
from authapp.models import EmailVerifyRecord
from Hella.settings import EMAIL_FROM




def random_str(random_length=8):
    """
    生产随机字符串
    :param random_length:
    :return:
    """
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1

    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

def send_register_email(email, send_type="register"):
    """
    定义发送邮件的基础函数，此函数接受两个参数，
    :param email: 需要发送邮件的邮箱，
    :param send_type: 发送验证码类型，在EmailVerifyRecord模型中，"register" 代表注册, "forget" 代表找回密码
    :return:
    """
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 定义邮件标题和内容
    email_title = ""
    email_body = ""

    # 要对邮件的类型做判断, 注册邮件、找回密码邮件是不一样的
    if send_type == "register":
        # 如果是发送注册邮件, 按照以下逻辑处理
        email_title = "周大仙激活链接"
        email_body = "请点击下面的链接来激活你的账号：http://127.0.0.1:8000/active/%s" % code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    elif send_type == "forget":
        # 发送找回密码
        email_title="周大仙密码重置连接"
        email_body = "请点击下面链接来重置密码： http://127.0.0.1:8000/reset/%s" % code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass