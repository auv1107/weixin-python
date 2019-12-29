# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from flask import Flask, jsonify, request, url_for
from weixin import Weixin, WeixinError

app = Flask(__name__)
app.debug = True

# 具体导入配
# 根据需求导入仅供参考
app.config.update(dict(WEIXIN_APP_ID='', WEIXIN_MCH_ID='',
                       WEIXIN_MCH_KEY='', WEIXIN_NOTIFY_URL=''))

# 初始化微信
weixin = Weixin()
weixin.init_app(app)


# 或者
# weixin = Weixin(app)

@app.route("/pay/app_api")
def pay_app_api():
    """微信网页支付请求发起"""
    try:
        out_trade_no = weixin.nonce_str
        raw = weixin.app_api(body=u"测试", out_trade_no=out_trade_no, total_fee=1)
        return jsonify(raw)
    except WeixinError, e:
        print e.message
        return e.message, 400


@app.route("/pay/notify")
def pay_notify():
    """
    微信异步通知
    """
    data = weixin.to_dict(request.data)
    if not weixin.check(data):
        return weixin.reply("签名验证失败", False)
    # 处理业务逻辑
    return weixin.reply("OK", True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9900)
