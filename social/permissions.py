from common import errors
from user.models import User



def has_perm(perm_name):
    """
    权限检查装饰器
    :param perm_name:
    :return:
    """
    def decorator(view_fun):
        def wapper(request, *args, **kwargs):

            if request.user.vip.has_perms(perm_name):
                return view_fun(request, *args, **kwargs)
            else:
                raise errors.VipPermError

        return wapper
    return decorator
