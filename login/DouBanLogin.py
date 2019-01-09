from urllib import request

from PIL import Image
import requests


class DouBanLoginForOld(object):
    # 构造器
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'host': 'accounts.douban.com',
            'Origin': 'https://www.douban.com',
            'Referer': 'https://www.douban.com/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2843.400',
            'Connection': 'keep-alive'
        }
        self.session.headers.update(self.headers)
        self.picture = None
        self.captcha = None
        self.captcha_image = None
        self.url = "https://www.douban.com/accounts/login"
        self.form_email = None
        self.form_password = None
        self.iscaptcha = None
        self.captcha_token = None

    # 获得验证码
    def getcaptcha(self):
        response = self.session.get("https://www.douban.com/j/misc/captcha")
        set =  response.json()
        if set.get('r') == False:
            self.iscaptcha = 1
            self.captcha_tzoken =set.get('token')
            request.urlretrieve("https://www.douban.com/misc/captcha?id=" + set.get('token') + "&size=s", '验证码.jpg')
            image = Image.open('验证码.jpg')
            image.show()
            self.captcha = input("请输入验证码")
        else:
            self.iscaptcha = 0

    # 模拟登录
    def login(self):
        if self.iscaptcha == 1:
            data = {
                'form_email': '15659067707',
                'form_password': '123321wsc',
                'captcha-solution' : self.captcha,
                "captcha-id": self.captcha_token
            }
        else:
            data = {
                'form_email': '15659067707',
                'form_password': '123321wsc',
            }
        response = self.session.post(self.url,data,headers=self.headers)
        print(response.text)

if __name__ == '__main__':
    douban = DouBanLoginForOld()
    douban.getcaptcha()
    douban.login()