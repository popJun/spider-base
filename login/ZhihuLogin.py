# 构造器
import requests
import base64
import hmac
import time

from PIL import Image


class ZhihuLoginForOld(object):
    # 构造器
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/signup?next=%2F',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
            'Connection': 'keep-alive',
            'X-Xsrftoken': 'iB8MUzYQ0FNkXdUMfSQIWU7Kyv980hdA'
        }
        self.session.headers.update(self.headers)
        self.picture = None
        self.signature = None
        self.picture_url = None
        pass

    # 图片解析
    def getCaptcha(self):
        messge = self.session.get(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en').json();
        print(messge)  # 用于查看是否需要验证码
        self.picture_url = self.session.put(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en').json();

        if (messge['show_captcha'] == 'false'):
            self.picture = ''
        else:
            with open('验证码.jpg', 'wb') as f:
                f.write(base64.b64decode(self.picture_url['img_base64']))
            image = Image.open('验证码.jpg')
            image.show();
            self.picture = input("请输入验证码")

    # 获得签名
    # function(e, t, n) {
    #    "use strict";
    #   function r(e, t) {
    # var n = Date.now(),
    # r = new i.a("SHA-1", "TEXT");
    # return r.setHMACKey("d1b964811afb40118a12068ff74a12f4", "TEXT"),
    # r.update(e),
    # r.update(s),
    # r.update("com.zhihu.web"),
    # r.update(String(n)),
    # u({
    # clientId: s,
    # grantType: e,
    # timestamp: n,
    # source: "com.zhihu.web",
    # signature: r.getHMAC("HEX")
    # },
    #    t)
    #    }
    def getsignature(self):
        signature = hmac.new("d1b964811afb40118a12068ff74a12f4".encode("utf-8"), digestmod='sha1');
        signature.update(b'password');
        signature.update(b'c3cef7c66a1843f8b3a9e6a1e3160e20')  # clientId
        signature.update(b'com.zhihu.web')
        signature.update(str(round(time.time() * 1000)).encode())  # 时间戳
        self.signature = signature.hexdigest()

    def login(self):
        data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'password',
            'timestamp': str(int(time.time() * 1000)),
            'source': 'com.zhihu.web',
            'signature': self.signature,
            'username': '15659067707',
            'password': '123321wsc',
            'captcha':self.picture,
            "lang": "cn",
            "ref_source": "homepage",
            "utm_source": ""
        }
        message = self.session.post(url='https://www.zhihu.com/api/v3/oauth/sign_in', headers=self.headers, data=data)
        message.encoding = 'utf-8'
        print(message.text)

    def target_url(self, url):
        text = self.session.get(url)
        return text.text

    def get_xsrf_dc0(self):
        response = self.session.get("https://www.zhihu.com/signup", headers=self.headers)
        return response.cookies["_xsrf"]


if __name__ == '__main__':
    zhihu = ZhihuLoginForOld()
    zhihu.getCaptcha()
    zhihu.getsignature()
    zhihu.login()
    with open('index.html', 'w',encoding='utf-8' ) as f:
        f.write(zhihu.target_url('https://www.zhihu.com/'))
