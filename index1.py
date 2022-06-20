# -*- coding: UTF-8 -*-

import os
import requests
import requests as req
import json
import time
import random

global access_token_list

app_num = os.getenv("APP_NUM")
if app_num == '':
    app_num = '1'
access_token_list = ['fengshaopeng']*int(app_num)

# 配置选项，自由选择
config_list = {'每次轮数': 1,
               '是否启动随机时间': 'N', '延时范围起始': 60, '结束': 120,
               '是否开启随机api顺序': 'Y',
               '是否开启各api延时': 'N', 'api延时范围开始': 2, 'api延时结束': 5,
               '是否开启各账号延时': 'N', '账号延时范围开始': 60, '账号延时结束': 120,

               'summary': 'Office365API调用提醒',
               'contentType': 1
               }
# '是否开启备用应用':'N','是否开启测试':'N'
api_list = [r'https://graph.microsoft.com/v1.0/me/',
            r'https://graph.microsoft.com/v1.0/users',
            r'https://graph.microsoft.com/v1.0/me/people',
            r'https://graph.microsoft.com/v1.0/groups',
            r'https://graph.microsoft.com/v1.0/me/contacts',
            r'https://graph.microsoft.com/v1.0/me/drive/root',
            r'https://graph.microsoft.com/v1.0/me/drive/root/children',
            r'https://graph.microsoft.com/v1.0/drive/root',
            r'https://graph.microsoft.com/v1.0/me/drive',
            r'https://graph.microsoft.com/v1.0/me/drive/recent',
            r'https://graph.microsoft.com/v1.0/me/drive/sharedWithMe',
            r'https://graph.microsoft.com/v1.0/me/calendars',
            r'https://graph.microsoft.com/v1.0/me/events',
            r'https://graph.microsoft.com/v1.0/sites/root',
            r'https://graph.microsoft.com/v1.0/sites/root/sites',
            r'https://graph.microsoft.com/v1.0/sites/root/drives',
            r'https://graph.microsoft.com/v1.0/sites/root/columns',
            r'https://graph.microsoft.com/v1.0/me/onenote/notebooks',
            r'https://graph.microsoft.com/v1.0/me/onenote/sections',
            r'https://graph.microsoft.com/v1.0/me/onenote/pages',
            r'https://graph.microsoft.com/v1.0/me/messages',
            r'https://graph.microsoft.com/v1.0/me/mailFolders',
            r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
            r'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
            r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
            r"https://graph.microsoft.com/v1.0/me/messages?$filter=importance eq 'high'",
            r'https://graph.microsoft.com/v1.0/me/messages?$search="hello world"',
            r'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top',
            ]


class Foo(object):  # 计数器
    _count = 0  # 不要直接操作此变量，也尽量避免访问它

    @property
    def count(self):
        return Foo._count

    @count.setter
    def count(self, num):
        Foo._count = num


class api(object):

    # 数据初始化
    def __init__(self):
        super().__init__()
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'
                        }
        self.header_wechar = {
            'Content-Type': 'application/json'}

    # 微软access_token获取
    def getmstoken(self, client_id, client_secret, ms_token):
        data = {'grant_type': 'refresh_token',
                'refresh_token': ms_token,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': 'http://localhost:53682/'
                }
        html = req.post(
            'https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=self.headers)
        jsontxt = json.loads(html.text)

        print(jsontxt)

        access_token = jsontxt['access_token']
        return access_token

    # # 更新微软refresh_token
    # def updata(self):
    #     t1 = int(time.time())
    #     t2 = int(t1/86400)
    #     if t2 % 7 == 0:
    #         tokenlist.updatarun(t2)
    #     else:
    #         pass

    # 调用函数
    def runapi(self, apilist, a, c):
        access_token = access_token_list[a-1]
        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }
        f1 = Foo()  # 实例化计数器
        for a in range(len(apilist)):
            try:
                if req.get(api_list[apilist[a]], headers=headers).status_code == 200:
                    print('第'+str(apilist[a])+"号api调用成功")

                    if config_list['是否开启各api延时'] != 'N':
                        time.sleep(random.randint(
                            config_list['api延时范围开始'], config_list['api延时结束']))
                else:
                    print('第'+str(apilist[a])+"号api调用失败")
                    if c == 1:  # 仅统计一轮错误次数
                        f1.count = f1.count + 1
            except:
                print("pass")
                pass

    def getaccess(self):
        # 一次性获取access_token，降低获取率
        for a in range(1, int(app_num)+1):

            if a == 1:
                client_id = os.getenv('CLIENT_ID')
                client_secret = os.getenv('CLIENT_SECRET')
                ms_token = os.getenv('MS_TOKEN')
                access_token_list[a-1] = self.getmstoken(
                    client_id, client_secret, ms_token)
            else:
                client_id = os.getenv('CLIENT_ID_'+str(a))
                client_secret = os.getenv('CLIENT_SECRET_'+str(a))
                ms_token = os.getenv('MS_TOKEN_'+str(a))
                access_token_list[a-1] = self.getmstoken(
                    client_id, client_secret, ms_token)

    def fixlist(self):
        # 随机api序列
        fixed_api = [0, 1, 5, 6, 20, 21]
        # 保证抽取到outlook,onedrive的api
        ex_api = [2, 3, 4, 7, 8, 9, 10, 22, 23, 24, 25,
                  26, 27, 13, 14, 15, 16, 17, 18, 19, 11, 12]
        # 额外抽取填充的api
        fixed_api.extend(random.sample(ex_api, 6))
        random.shuffle(fixed_api)
        return fixed_api

    # 出现失败情况时发送通知信息
    def sendmessage(self, i):
        a = 12-i
        local_time = time.strftime('%Y-%m-%d %H:%M:%S')

        barkurl = os.getenv("url_bark") + \
            "Office365API调用存在失败情况，失败个数为{}，成功个数为{}。调用结束时间为{}".format(
                i, a, local_time)

        body = {
            "appToken": os.getenv("appToken"),
            # 信息内容
            "content": "Office365API调用存在失败情况，\n失败个数为{}，成功个数为{}。\n调用结束时间为{}。\n若非本人操作请尽快登录腾讯云服务器进行查看管理。\n腾讯云管理链接如下。".format(i, a, local_time),
            "summary": config_list['summary'],
            "contentType": int(config_list['contentType']),
            # "topicIds": config['topicIds'],
            "uids": [os.getenv("UID")],
            "url": os.getenv("url")
        }

        urla = os.getenv("url_wechat")
        requests.get(barkurl)
        s = requests.session()
        s.post(urla, headers=self.header_wechar,
               data=json.dumps(body), verify=False)

    def run(self):
        # 实际运行
        self.getaccess()
        print('共'+str(config_list['每次轮数'])+'轮')
        for c in range(1, config_list['每次轮数']+1):
            if config_list['是否启动随机时间'] == 'Y':
                time.sleep(random.randint(
                    config_list['延时范围起始'], config_list['结束']))
            for a in range(1, int(app_num)+1):
                if config_list['是否开启各账号延时'] == 'Y':
                    time.sleep(random.randint(
                        config_list['账号延时范围开始'], config_list['账号延时结束']))
                if a == 1:
                    print('\n'+'应用/账号 '+str(a)+' 的第'+str(c)+'轮' +
                          time.asctime(time.localtime(time.time()))+'\n')
                    if config_list['是否开启随机api顺序'] == 'Y':
                        print("已开启随机顺序,共12个api")
                        apilist = self.fixlist()
                        self.runapi(apilist, a, c)
                    else:
                        print("原版顺序,共10个api")
                        apilist = [5, 9, 8, 1, 20, 24, 23, 6, 21, 22]
                        self.runapi(apilist, a, c)
                else:
                    print('\n'+'应用/账号 '+str(a)+' 的第'+str(c)+'轮' +
                          time.asctime(time.localtime(time.time()))+'\n')
                    if config_list['是否开启随机api顺序'] == 'Y':
                        print("已开启随机顺序,共12个api")
                        apilist = self.fixlist()
                        self.runapi(apilist, a, c)
                    else:
                        print("原版顺序,共10个api")
                        apilist = [5, 9, 8, 1, 20, 24, 23, 6, 21, 22]
                        self.runapi(apilist, a, c)

        f2 = Foo()
        if f2.count != 0:
            #self.sendmessage(f2.count)
            pass


# def main_handler(event, context):
#     api().run()
#     api().updata()
#     local_time = time.strftime('%Y-%m-%d %H:%M:%S')
#     print("执行完成，完成时间{}".format(local_time))


if __name__ == "__main__":
    api().run()
    # api().updata()
    local_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print("执行完成，完成时间{}".format(local_time))
