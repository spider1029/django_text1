"""

业务状态码，错误码


"""

OK=0
#用户系统
PHONE_NUM_ERR = 2001        #手机验证失败
SMS_SEND_ERR = 2002         #验证码发送失败
VERIFY_CODE_ERR = 2003      #验证码错误
LOGIN_REQUIRED_ERR = 2004   #用户认证错误
AVATAR_UPLOAD_ERR = 2005    #保存用户头像失败


#社交系统

SDI_ERR = 3001              #SID返还失败
SWIPE_ERR = 3002            #滑动错误


class LogicException(Exception):
    """
    自定义逻辑异常类
    调用通过参数，传递错误码
    """
    def __init__(self, code):
        self.code = code


class LogicError(Exception):
    code = None


# class SwipeError(LoginError):
#     code =3002


def gen_logic_error(name, code):
    return type(name, (LogicError,), {'code': code})


SidError = gen_logic_error('SidError', 3001)
SwipeError = gen_logic_error('SwipeError', 3002)
SwipeLimitError = gen_logic_error('SwipeLimitError', 3003)   # 滑动次数错误


# vip系统
VipPermError = gen_logic_error("VipPermError", 4001)   #权限错误