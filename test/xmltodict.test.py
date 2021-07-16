import xmltodict
with open("a.xml") as fd:
  doc = xmltodict.parse(fd.read())
  print(doc['xml']['return_code'])



'''
<xml>
<return_code><![CDATA[SUCCESS]]></return_code>
<return_msg><![CDATA[OK]]></return_msg>
<result_code><![CDATA[SUCCESS]]></result_code>
<mch_id><![CDATA[mch_id]]></mch_id>
<appid><![CDATA[appid]]></appid>
<nonce_str><![CDATA[kxMMSHeWuTL3YGkJ]]></nonce_str>
<sign><![CDATA[BEC6F77702B8F6DA9B3F0A0F5B638692]]></sign>
<prepay_id><![CDATA[wx15164617651443432306cab3a7b6d50000]]></prepay_id>
<trade_type><![CDATA[MWEB]]></trade_type>
<mweb_url><![CDATA[https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?prepay_id=wx15164617651443432306cab3a7b6d50000&package=1258281822]]></mweb_url>
</xml>
'''

# python xmltodict.test.py