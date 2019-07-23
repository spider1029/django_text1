from django.db import models

# Create your models here.
from django.db.models import Q

from common import errors
from common.errors import LogicException


class Swiped(models.Model):
    """
    滑动记录
    """
    MARKS=(
        ('like','喜欢'),
        ('dislike','不喜欢'),
        ('superlike','超级喜欢'),
    )
    uid = models.IntegerField()
    sid = models.IntegerField()
    mark = models.CharField(max_length=16, choices=MARKS)
    create_at = models.DateField(auto_now_add=True)

    @classmethod
    def swipe(cls, uid, sid,mark):
        """
        创建滑动记录
        :param uid:
        :param sid:
        :param mark:
        :return:
        """
        marks = [m for m, _ in cls.MARKS]

        if mark not in marks:
            raise LogicException(errors.SWIPE_ERR)

        # cls.objects.update_or_create(uid=uid, sid=sid, mark=mark)

        if cls.objects.filter(uid=uid, sid=sid).exists():
            return False
        else:
            cls.objects.create(uid=uid, sid=sid, mark=mark)
            return True


    @classmethod
    def is_like(cls,uid,sid):

        return cls.objects.filter(uid=uid, sid=sid, mark__in=['like','superlike']).exists()


    class Meta:
        db_table='swiped'


class Friend(models.Model):
    """
    好友关系表

    """
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()


    @classmethod
    def make_friends(cls, uid1, uid2):
        """
        创建好友关系
        :param uid1:
        :param uid2:
        :return:
        """
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)

        return cls.objects.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def cancel_friend(cls, uid1, uid2):
        """
        撤销好友关系
        :param uid:
        :param sid:
        :return:
        """
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)

        return cls.objects.filter(uid1=uid1, uid2=uid2).delete()
    @classmethod
    def friend_list(cls, uid):
        fid_list=[]

        friend = cls.objects.filter(Q(uid1=uid) | Q(uid2=uid))

        for f in friend:
            fid = f.uid1 if uid == f.uid2 else f.uid2
            fid_list.append(fid)

        return fid_list


    class Meta:
        db_table = 'friend'















