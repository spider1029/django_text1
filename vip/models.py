from django.db import models

# Create your models here.
from libs.orm import ModelToDictMixin


class Vip (models.Model, ModelToDictMixin):
    """
    会员
    """
    level = models.IntegerField(default=0,unique=True)
    name = models.CharField(max_length=192, unique=True)
    price = models.DecimalField(max_digits=5,decimal_places=2, default=0)

    @property
    def perms(self):
        """
        当前vip对应的权限
        :return:
        """
        if not hasattr(self,'_perms'):
            # 通过vip_id 从ip-permissions 关系表中获取对应的perm.id
            vips_perms = VipPermissions.objects.filter(vip_id=self.id).only('perm_id')
            perm_id_list = [p.perm_id for p in vips_perms]
            self._perms = Permission.objects.filter(id__in=perm_id_list)
        return self._perms


    def has_perms(self,perm_name):
        """
        检查当前vip拥有何种权限
        :param perm_name:
        :return:
        """
        perm_names = [p.name for p in self.perms]


        return perm_name in perm_names

    class Meta:
        db_table='vips'



class Permission(models.Model,ModelToDictMixin):
    """
    权限
    """
    name = models.CharField(max_length=32,unique=True)
    desctiption = models.CharField(max_length=512)

    class Meta:
        db_table="permissions"


class VipPermissions(models.Model):
    """
    会员，权限 关系表
    """
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()

    class Meta:
        db_table = 'vip_perimssions'




