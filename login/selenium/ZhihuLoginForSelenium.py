from time import sleep
import base64
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

class ZhihuLoginSpire():
    def seleniumLogin(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        browser = webdriver.Chrome()
        browser.get(url="https://www.zhihu.com/")
        session = requests.session()
        session.headers.clear()
        #切换到登陆
        browser.find_element_by_css_selector(".SignContainer-switch span").click()
        #输入账号和密码
        browser.find_element_by_css_selector(".SignFlowInput .SignFlow-accountInput .Input").send_keys("15659067707")
        browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper .Input").send_keys("123321wsc");
        #查看是否有验证码
        captcha_element = browser.find_element_by_xpath("//form[@class='SignFlow']/div[3]//img")
        captcha_base64 =captcha_element.get_attribute('src')
        print(captcha_base64)
        ##存在验证码
        if captcha_base64 !="data:image/jpg;base64,null":
            img_base64=captcha_base64.split(",")[-1]
            img_data=base64.b64decode(img_base64)
            image = Image.open(BytesIO(img_data))
            image.show()
            captcha_type=captcha_element.get_attribute('class')
            if captcha_type =='Captcha-englishImg':
                captcha = input('请输入图片中的验证码：')
                browser.find_element_by_name("captcha").send_keys(captcha)
                
        click_btn1 = browser.find_element_by_xpath('//button[@type="submit"]') #登录
        ActionChains(browser).click(click_btn1).perform()
        sleep(2)
        print(browser.title)

if __name__ == '__main__':
    zhihu = ZhihuLoginSpire()
    zhihu.seleniumLogin()
