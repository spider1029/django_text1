import datetime

from django.core.cache import cache
from django.db import models


# Create your models here.


class User(models.Model):
    SEXS = (
        (0, '未知'),
        (1, '男'),
        (2, '女')
    )

    LOCATIONS = (
        ('gz', '广州'),
        ('bj', '北京'),
        ('sh', '上海'),
        ('hz', '杭州'),
        ('cd', '成都'),
        ('sz', '深圳'),
    )

    phonenum = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=16)
    sex = models.IntegerField(choices=SEXS, default=0)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avatar = models.CharField(max_length=256, )
    location = models.CharField(max_length=16, choices=LOCATIONS, default='gz')

    @property
    def age(self):
        today = datetime.date.today()
        brithday = datetime.date(self.birth_year, self.birth_month, self.birth_day)

        return (today - brithday).days // 365

    def to_dict(self):
        return {
            'uid': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'avatar': self.avatar,
            'location': self.location,
            'age': self.age

        }

    def get_or_create_token(self):
        key = 'token{}', format(self.id)

        token = cache.get(key)

        if not token:
            token = 'token......123123123123'
            cache.set(key, token, 24 * 60)

        return token

    class Meta:
        db_table = "users"
