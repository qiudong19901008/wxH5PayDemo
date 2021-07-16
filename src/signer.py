import string
from typing import Dict
import hashlib
from dicttoxml import dicttoxml
import xmltodict

class Signer:

  '''
  该类主要包含签名的方法:
  1. getSignature: 生成签名
  2. checkSignature: 验证微信传过来的签名
  '''


  def getSignature(params:Dict,apiKey:str):
    '''获取签名
    
    把传进来的字典按deeplink规则组合, 然后拼接上apikey, 最后通过md5加密转大写

    Args:
      params: 不包含商户号apiKey的参数
      apiKey: 商户号apiKey
    '''
    deeplink = Signer.getDeeplink(params)
    return Signer.md5(f'{deeplink}&key={apiKey}',convertToUpper=True)
  
  def checkSignature(weixinXml:str,apiKey:str):
    '''检验微信的签名
    
    微信传递给我们信息后, 必须验证这个签名, 防止坏人冒充微信

    Args:
      weixinXml: 微信传入的xml数据
      apiKey: 商户号apiKey
    '''
    params = xmltodict.parse(weixinXml)
    weixinSign = params['xml']['sign']
    sign = Signer.getSignature(params['xml'],apiKey)
    return True if weixinSign == sign else False

  def md5(str,convertToUpper=False):
    '''对字符串进行md5加密

    Args:
      str: 需要被加密的字符串
      convertToUpper: 是否转为大写, 默认不转
    '''
    md5 = hashlib.md5()
    md5.update(str.encode("utf8"))
    res = md5.hexdigest()
    return res.upper() if convertToUpper else res

  
  def getDeeplink(params:Dict):
    ''' 组装成需要被签名的参数, 注意不包含商户号apikey

    组装参数, 获得appid=wxd930ea5d5a258f4f&body=test&device_info=1000&mch_id=10000100&nonce_str=ibuaiVcKdpRxkhJA的字符串,
    经过了去除空值, 去除sign值的操作

    Args: 
      params: 不包含商户号apikey的其他参数
    '''
    deeplink = ''
    #去除空值 和 sign值
    for key in list(params.keys()):
          if not params.get(key) or key == 'sign':
              del params[key]
    #ascii排序并组装成格式: appid=wxd930ea5d5a258f4f&body=test&device_info=1000&mch_id=10000100&nonce_str=ibuaiVcKdpRxkhJA
    keys = sorted(list(params.keys()))
    for key in keys:
      deeplink+=f'{key}={params[key]}&'
    return deeplink[0:-1]