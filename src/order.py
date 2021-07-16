from typing import Dict
from flask import request
import random
import string
from numbers import Number
from dicttoxml import dicttoxml
import xmltodict
import requests

from config import Config
from signer import Signer
from helper import Helper

class Order:
  ''' 
  该类只是下单用, 只实现了h5下单
  '''

  unifiedOrderUrl = 'https://api.mch.weixin.qq.com/pay/unifiedorder' #统一下单接口

  def h5Order(out_trade_no:string,body:string,total_fee:Number):
    '''h5下单参数, 都是必填项
    
    Args:
      out_trade_no: 我们自己内部订单号
      body: 商品描述信息
      total_fee: 总金额, 单位分 
    '''
    h5Xml = Order.assembleH5OrderXml(out_trade_no,body,total_fee)
    # 调用统一下单接口
    redirectUrl = Order.realH5OrderThenGetRedirectUrl(h5Xml)
    return redirectUrl

  def assembleH5OrderXml(out_trade_no:str,body:str,total_fee:Number):
    '''把参数组装成h5xml
    
    Args:
      out_trade_no: 我们自己内部订单号
      body: 商品描述信息
      total_fee: 总金额, 单位分
    '''
    params = {
      'appid': Config.appid, #公众号id
      'mch_id' : Config.mch_id, #商户号id
      'notify_url' : Config.notify_url, #回调通知url
      'out_trade_no' : out_trade_no,#我们自己内部的订单号, 这个要保存, 以后查单时需要
      'body' : body, # 商品描述
      'nonce_str' : Helper.getNonceStr(), #随机字符串
      'spbill_create_ip' : Helper.getCustomerIp(), #客户下单ip, 必须获取真实ip
      'total_fee' : total_fee, #总金额, 单位分
      'trade_type' : 'MWEB' #下单类型, MWEB表示h5
    }
    # 参数添加签名
    params['sign'] = Signer.getSignature(params,Config.key)
    # 把请求参数转为xml格式
    return Helper.dictToXml(params)


  def realH5OrderThenGetRedirectUrl(h5Xml):
    '''真实下单并获取mweb_url

    下单后会获得mweb_url字段, 该字段用来跳转进微信

    Args:
      h5Xml: h5下单用的xml
    '''
    res = requests.post(
      url = Order.unifiedOrderUrl,
      headers = {'Content-Type': 'application/xml'},
      data = h5Xml,
    )
    if(res.status_code != 200):
      return ''
    res.encoding = "utf-8"  
    dictRes = Helper.xmlToDict(res.text)
    print(dictRes)
    if(dictRes['xml']['return_code'] != 'SUCCESS' or  dictRes['xml']['result_code'] != 'SUCCESS'):
      return ''
    #请求成功返回跳转链接
    return dictRes['xml']['mweb_url']


  