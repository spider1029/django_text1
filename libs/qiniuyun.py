# -*- coding: utf-8 -*-

from qiniu import Auth, put_file, etag

from common import config


def upload(file_name, file_path):

    """
    本地文件上传至七牛云
    :param file_name:
    :param file_path:
    :return:
    """
    # 构建鉴权对象
    qn_auth = Auth(config.QN_access_key, config.QN_secret_key)

    # 要上传的空间
    bucket_name = config.QN_bucket_name

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(bucket_name, file_name, 3600)

    # 要上传文件的本地路径
    ret, info = put_file(token, file_name, file_path)

    return ret, info


