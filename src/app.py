from flask import Flask,render_template,request,redirect,Response
from order import Order
from replier import Replier
from helper import Helper
from querier import Querier

app = Flask(__name__)

out_trade_no = 'skjflk' #订单号
body = '测试商品' # 商品描述
total_fee = 2 # 商品价格

@app.route('/')
def index():
  return render_template('order.html')

# 下单接口
@app.route('/order')
def order():
  redirectUrl = Order.h5Order(out_trade_no=out_trade_no,body=body,total_fee=total_fee)
  #如果没有获得跳转链接, 则返回到错误页面
  if redirectUrl  == '':
    return render_template('error.html')
  #成功则重定向到微信
  return redirect(redirectUrl)

# 回复微信回调用接口
@app.route('/reply',methods = ["POST"])
def reply():
  wxXml = request.get_data(as_text=True)
  msg = Replier.getReplyMsg(weixinXml=wxXml,fee=total_fee)
  r = Response(response=msg, status=200, mimetype="application/xml")
  r.headers["Content-Type"] = "text/xml; charset=utf-8"
  return r

# 用户主动查询订单状态接口
@app.route('/checkOrderStatus')
def checkOrderStatus():
  isOk = Querier.isOk(out_trade_no)
  if not isOk:
    return render_template('error.html')
  #
  return render_template('success.html')


if __name__ == '__main__':
  app.run(debug=True,port=3000)