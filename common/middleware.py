from django.utils.deprecation import MiddlewareMixin

from common import errors
from libs.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        """
        自定义认证中间间
        :param request:
        :return:
        """
        WHITE_LIST = [
            '/api/user/login',
            '/api/user/verify-phone'
        ]
        if request.path in WHITE_LIST:
            return

        uid = request.session.get('uid')

        if not uid:
            return render_json(code=errors.LOGIN_REQUIRED_ERR)

        request.user = User.objects.get(pk=uid)


        #
        # token = request.META.get('X-AUTH-TOKEN')
        #
        # if not token:
        #     return render_json(code=errors.LOGIN_REQUIRED_ERR)
