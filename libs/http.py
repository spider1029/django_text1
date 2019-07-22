from django.http import JsonResponse

from common import errors
from swiper import settings


def render_json(code=errors.OK, data=None):

    result = {
        'code': code,
    }
    if data:
        result['data'] = data


    if settings.DEBUG:
        json_dumps_params = {
            'ensure_ascii': False,
            'indent': 4
        }

    else:
        json_dumps_params = {
            'separators': (',', ':')
        }

    return JsonResponse(data=result, json_dumps_params=json_dumps_params)
