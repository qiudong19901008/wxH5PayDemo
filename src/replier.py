from signer import Signer
import string
from numbers import Number
import xmltodict
from config import Config
from helper import Helper
import requests

class Replier:



  '''当用户付款成功后, 微信会发送回调通知给我们, 我们应该回复微信
  
  为了避免别人假冒微信, 我们必须进行一下操作:
  1. 签名验证
  2. 校验订单金额是否一致
  '''

  def getReplyMsg(weixinXml:str,fee:Number):
    isWeixinNotify = Signer.checkSignature(weixinXml,Config.key)
    if not isWeixinNotify:
      return ''
    weixinFee = Helper.xmlToDict(weixinXml)['xml']['total_fee']
    #检测金额是否一致
    if int(weixinFee) != fee:
      return ''
    replyMap = {
      'return_code':'SUCCESS',
      'return_msg':'OK',
    }
    return Helper.dictToXml(replyMap)
    
