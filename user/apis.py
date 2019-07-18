from django.core.cache import cache
from django.http import JsonResponse

from common import errors, cache_keys
from common.utils import is_phone_num
from libs.http import render_json
from user import logics
from user.froms import ProfileForm
from user.models import User


def verify_phone(request):
    """
    1)验证手机格式
    2）生成验证码
    3）保存验证码
    4）发送验证码


    :param request:
    :return:
    """

    phone_num = request.POST.get('phone_num')
    print(phone_num)

    if is_phone_num(phone_num):

        # 生成和发送验证码
        if logics.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(errors.SMS_SEND_ERR)
    else:
        return render_json(errors.PHONE_NUM_ERR)


def login(request):
    """
    登录和注册接口


    :param request:
    :return:

    """
    phone_num = request.POST.get('phone_num', '')
    code = request.POST.get('code', '')
    phone_num = phone_num.strip()
    code = code.strip()

    cache_code = cache.get(cache_keys.VERIFY_CODE_CACHE_PREFIX.format(phone_num))

    if cache_code != code:
        return render_json(code=errors.VERIFY_CODE_ERR)

    # user, created = User.objects.get_or_create(phonenum=phone_num)

    try:
        user = User.objects.get(pk=1)
    except User.DoesNotExist:
        user = User.objects.create()

    request.session['uid'] = user.id

    #token认证方式
    # token =user.get_or_create_token()
    # data ={'token':token}
    # return render_json(data=data)

    return render_json(data=user.to_dict())


def set_profile(request):
    user = request.user

    form = ProfileForm(data=request.POST, instance=user.profile)

    if form.is_valid():  # 判断表单是否验证通过
        form.save()
        return render_json()
    else:
        return render_json(data=form.errors)


def get_profile(request):
    user = request.user

    return render_json(data=user.profile.to_dic(exclued=['auto_play']))