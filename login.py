from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
import json
import warnings
warnings.filterwarnings("ignore")
from mylog import *

class eamis_account:
    def __init__(self, username, password, is_password_encrypted=False, profileId=[]):
        self.username = username
        self.profileId = profileId # 待选课的profileId集合
        if not is_password_encrypted:
            self.password = self.encrypt(password)
        else:
            self.password = password
        self.cookies = None
        self.status = self.test_login()
        if self.status:
            info_log("account "+username+" right password")
        elif self.status == None:
            error_log("account "+username+" network error")
        else:
            error_log("account "+username+" wrong password")
    def encrypt(self, password):
        key = "8bfa9ad090fbbf87e518f1ce24a93eee".encode('utf-8')
        iv = "fbfae671950f423b58d49b91ff6a22b9".encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv[:16])
        encrypted_hex = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size)).hex()
        return encrypted_hex
    def verify(self):
        if not self.status:
            error_log("verify "+self.username+" failed:wrong password")
            return False
        url = 'https://eamis.nankai.edu.cn/'
        responce = requests.get(url, verify=False)
        eamis_cookies = responce.cookies

        url = 'https://eamis.nankai.edu.cn/eams/home.action'
        responce = requests.get(url, cookies=eamis_cookies, verify=False, allow_redirects=False)
        eamis_cookies.update(responce.cookies)
        # eamis_cookies.set('semester.id', "4262", domain='eamis.nankai.edu.cn')

        url = 'https://eamis.nankai.edu.cn' + responce.headers.get('Location')
        responce = requests.get(url, cookies=eamis_cookies, verify=False, allow_redirects=False)

        url = responce.headers.get('Location')
        responce = requests.get(url, verify=False, allow_redirects=False)
        iam_cookies = responce.cookies

        url = 'https://iam.nankai.edu.cn/api/v1/login?os=web'
        data = {"login_scene":"feilian","account_type":"userid","account":self.username,"password":self.password}
        response = requests.post(url, json=data, verify=False, cookies=iam_cookies)
        iam_cookies.update(response.cookies)
        try:
            url = 'https://iam.nankai.edu.cn' + response.json().get('data').get('next').get('link')
        except:
            error_log("verify " + self.username + " failed:"+response.json()["message"])
            return False
        response = requests.get(url, verify=False, cookies=iam_cookies, allow_redirects=False)

        url = response.headers.get('Location')
        response = requests.get(url, verify=False, allow_redirects=True, cookies=eamis_cookies)
        self.cookies = eamis_cookies
        info_log("update verify cookies, username:"+self.username)

        requests.get('https://eamis.nankai.edu.cn/eams/stdElectCourse.action', cookies=self.cookies, verify=False)
        for i in self.profileId:
            requests.get('https://eamis.nankai.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id='+i, cookies=self.cookies, verify=False)
        return True
    def test_login(self):
        loginurl = "https://iam.nankai.edu.cn/api/v1/login?os=web"
        headers = {
            "Content-Type": "application/json"
        }
        data = {"login_scene":"feilian","account_type":"userid","account":self.username,"password":self.password}
        try:
            response = requests.post(loginurl, headers=headers, data=json.dumps(data))
        except Exception as e:
            error_log("network error:"+str(e))
            return None
        '''
        right_response = {"code":0,"action":"","message":"","data":{"result":"success","next":{"action":"GoToLink","can_skip":true}}}
        wrong_response = {"code":10110001,"action":"alert","message":"用户名或密码错误，请再次输入，如确认无误可联系管理员排查。(10110001)"}
        '''
        response = response.json()
        if response["code"] == 0:
            info_log("test login " + self.username + " success")
            return True
        else:
            error_log("test login " + self.username + " failed:"+response["message"])
            return False
    def get_cookies(self):
        return self.cookies
    

if __name__ == '__main__':
    username = 'admin'
    password = '123456'
    account = eamis_account(username, password)
    account.verify()