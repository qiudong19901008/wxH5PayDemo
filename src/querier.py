from config import Config
from signer import Signer
from helper import Helper

import requests

class Querier:
  '''
    该类是用来查询订单状态的, h5支付跳回原页面有三种情况, 有两种是失败的, 所以跳回原页面应该引导用户查询订单状态
    1. 跳转微信链接超时5秒,返回原页面,支付失败
    2. 用户主动取消支付, 返回原页面, 支付失败
    3. 用户支付成功, 返回原页面, 支付成功

    查询后我们只需要关注一个字段 trade_state ,只要该字段是 SUCCESS ,就代表支付成功
  '''

  queryUrl = 'https://api.mch.weixin.qq.com/pay/orderquery'

  def isOk(out_trade_no):
    params = {
      'appid':Config.appid,
      'mch_id':Config.mch_id,
      'out_trade_no':out_trade_no,
      'nonce_str':Helper.getNonceStr(),
    }
    params['sign'] = Signer.getSignature(params,Config.key)
    res = requests.post(
      url = Querier.queryUrl,
      headers = {'Content-Type': 'application/xml'},
      data = Helper.dictToXml(params),
    )
    if(res.status_code != 200):
      return False
    res.encoding = "utf-8"  
    dictRes = Helper.xmlToDict(res.text)
    if(dictRes['xml']['return_code'] != 'SUCCESS' or  dictRes['xml']['result_code'] != 'SUCCESS' or dictRes['xml']['trade_state'] != 'SUCCESS'):
      return False
    #支付成功
    return True


