from typing import Dict
from flask import request
import random
import string
import xmltodict
from dicttoxml import dicttoxml


class Helper:

  '''
    帮助类, 一些通用方法存放的地方
  '''

  def getNonceStr(len=8):
    '''获取随机字符串

    Args: 
      len: 指定字符串长度
    '''
    return ''.join(random.sample(string.ascii_letters + string.digits, len))

  def getCustomerIp():
    '''获取客户端真实ip

    如果没使用nginx反代, 直接获取, 使用了则通过X-Forwarded-For属性获取, 该属性在nginx内设置
    '''
    if request.headers['X-Forwarded-For']:
        return request.headers['X-Forwarded-For']
    return request.remote_addr #nginx反代后,这个不是真实ip

  def xmlToDict(xml:str):
    return xmltodict.parse(xml)

  def dictToXml(params:Dict,root='xml'):
    return dicttoxml(params,custom_root=root,attr_type=False,cdata=True)
