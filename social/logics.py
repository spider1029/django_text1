import datetime

from django.core.cache import cache
from django.test import TestCase

# Create your tests here.


from common import cache_keys, errors, config
from social.models import Swiped, Friend
from user.models import User


def recommend_users(user):
    today = datetime.date.today()

    max_year = today.year - user.profile.min_dating_age

    min_year = today.year - user.profile.max_dating_age

    swiped_user = Swiped.objects.filter(uid=user.id).only('sid')

    swiped_sid_list = [s.sid for s in swiped_user]

    rec_user = User.objects.filter(
        location=user.profile.location,
        sex=user.profile.dating_sex,
        birth_year__gte=min_year,
        birth_year__lte=max_year,
    ).exclude(id__in=swiped_sid_list)[10:20]

    print(rec_user.query)

    return rec_user


def like_someone(uid, sid):
    rec = Swiped.swipe(uid=uid, sid=sid, mark='like')

    if rec and Swiped.is_like(sid, uid):
        _, creater = Friend.make_friends(sid, uid)
        # 发送匹配好友成功的推送消息
        return creater
    else:
        return False


def superlike_someone(uid, sid):
    rec = Swiped.swipe(uid=uid, sid=sid, mark='superlike')

    if rec and Swiped.is_like(sid, uid):
        _, creater = Friend.make_friends(sid, uid)
        # 发送匹配好友成功的推送消息
        return creater
    else:
        return False


def rewind(user):
    """
    撤销上一次滑动操作
    撤销上一次好友关系
    :param user:
    :return:
    """

    key = cache_keys.SWIPE_LIMIT_PREFIX.format(user.id)

    swipe_times = cache.get(key, 0)

    if swipe_times >= config.SWIPE_LIMIT:
        raise errors.SwipeLimitError

    swipe = Swiped.objects.filter(uid=user.id).latest('created_at')

    if swipe.mark in ['like', 'superlike']:
        Friend.cancel_friend(swipe.uid, swipe.sid)

    swipe.delete()

    now_time = datetime.datetime.now()

    timeout = 86400 - now_time.hour * 3600 - now_time.minute * 60 - now_time.second

    cache.set(key, swipe_times + 1, timeout=timeout)



def liked_me(user):
    """
    查看喜欢过我的人
    过滤已经存在的好友
    :param user:
    :return:
    """

    friend_list = Friend.friend_list(user.id)
    swipe_list= Swiped.objects.filter(sid=user.id, mark__in=['like', 'superlike']).exclude(uid__in=friend_list).only('uid')

    liked_me_uid_list = [s.uid for s in swipe_list]

    return liked_me_uid_list