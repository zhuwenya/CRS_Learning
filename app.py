# -*- coding: UTF-8 -*-
import web
import hashlib
import xml.dom.minidom as minidom
import backend
from backend import *
import time
import manage_user
from manage_user import *
import json
import datetime


User_Management=Manage_User()

class wechat:
    render = web.template.render('templates/')

    def GET(self):
        # For developer verification
        get_params = web.input()
        token = "wechatwenya"
        signature = get_params.signature
        timestamp = get_params.timestamp
        nonce = get_params.nonce
        echostr = get_params.echostr

        array = [token, timestamp, nonce]
        array.sort()
        checkstr = hashlib.sha1(''.join(array)).hexdigest()
        return echostr if checkstr == signature else 'Fail'

    def POST(self):
        data=web.data()
        web.header('Content-Type', 'text/xml')
        def get_tag(node, name):
            return root.getElementsByTagName(name)[0].childNodes[0].data
        root = minidom.parseString(data)
        toUser = get_tag(root, 'ToUserName')
        fromUser = get_tag(root, 'FromUserName')
        msgType = get_tag(root, 'MsgType')
        content = get_tag(root, 'Content')
        content=content.encode('utf-8')
        createTime =int(time.time())
        Recommend_Agent=User_Management.obtain_user_instance(fromUser,createTime)
        if Recommend_Agent.num==0:
            response,action,product,feature= Recommend_Agent.get_first_response()
            response="欢迎来到对话推荐系统,CRS向您推荐咖啡等其他饮品"+"友情提示：如果您想离开此系统，请输入q"+'\n'+'开始体验'+'\n'+response
            Recommend_Agent.num=1
        else:
            if msgType == u'text':
                content = get_tag(root, 'Content')
                #response="nihao"
                response,action,product,feature=Recommend_Agent.get_response(content)
            else:
                response = '{} is not supported yet.'.format(msgType.capitalize())
        User_Management.update_user(fromUser,Recommend_Agent)
        #User_Management.clean_user()
        data={fromUser:content,toUser:response,'time':createTime,'action':action,'product':product,'feature':feature}
        f=open('/home/ubuntu/Collect_Data/CRS_Learning/CRS_Learning/data/wechat_data.txt','a')
        json_str = json.dumps(data)
        f.write(json_str)
        f.write('\n')
        f.close()
        return wechat.render.response(fromUser, toUser, createTime, response)


if __name__ == "__main__":
    urls = ('/wechat', 'wechat')
    app = web.application(urls, globals())
    app.run()
