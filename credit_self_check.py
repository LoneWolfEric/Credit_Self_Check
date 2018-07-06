import requests
from bs4 import BeautifulSoup
import re
import time
import random

class CreditCheck():
    def __init__(self, account_num, password):
        self.account_num = account_num
        self.password = password
        self.s = requests.session()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'zhjw.scu.edu.cn',
            'Referer': 'http://zhjw.scu.edu.cn/loginAction.do',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Origin':'http://zhjw.scu.edu.cn',
        }

    # 登录教务处
    def login_in(self):
        url = 'http://zhjw.scu.edu.cn/loginAction.do'
        data = {
            'zjh': self.account_num,
            'mm': self.password
        }
        try:
            response = self.s.post(url, data = data, headers=self.headers)         # 登录教务处
        except ConnectionError:
            print('网络连接登录错误')
        except TimeoutError:
            print('访问超时登录错误')

        isError  = re.findall(r'<td class="errorTop">', response.content.decode('gbk'))
        if isError:                             # 判断账号密码是否正确
            print('账号或者密码错误，请重新输入！')
        else:
            print('登录成功')

    # 显示用户名称           
    def show_user_name(self):
        url = 'http://zhjw.scu.edu.cn/menu/s_top.jsp'
        user_info = self.s.get(url, headers = self.headers)     # 获取个人信息
        html = user_info.content.decode('gbk')
        user_name = re.findall(r'欢迎光临&nbsp;.{0,6}&nbsp;', html)
        try:
            user_name = user_name[0]
            num = user_name.rindex('&nbsp;')
            user_name = user_name[10: num]
            self.user_name = user_name
            print('你好，%s!' %(user_name))                             # 显示个人信息
        except  IndexError:
            print('获取信息失败')
    
    # 获取id
    def get_id(self):
        pattern = r'gradeLnAllAction.do\?type\=ln\&oper=fainfo\&fajhh=([0-9]{4})'
        url = 'http://202.115.47.141/gradeLnAllAction.do?type=ln&oper=fa'
        content = self.s.get(url=url, headers=self.headers).content.decode('GBK')
        id = re.findall(re.compile(pattern=pattern), content)[0]
        print('id', id)
        self.id = id

    # 获得学分信息
    def get_credit_info(self):
        url = 'http://202.115.47.141/gradeLnAllAction.do?type=ln&oper=lnfaqk&flag=zx'
        response = self.s.get(url, headers = self.headers)
        html = response.content.decode('gbk')
        print('---------------------')
        print(html)


def main():
    # account_num = str(input('请输入你的学号：'))
    # password = str(input('请输入你的教务处密码：'))
    # check = CreditCheck(account_num, password)
    check = CreditCheck('2016141442100', '081318')
    check.login_in()
    check.show_user_name()
    # check.get_id()
    check.get_credit_info()
   
if __name__ == '__main__':
    main()
