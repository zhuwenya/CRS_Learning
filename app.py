import web
import hashlib
import xml.dom.minidom as minidom
import backend
from backend import *
import time
import manage_user
from manage_user import *
import json

f=open('/home/ubuntu/Collect_Data/CRS_Learning/data/wechat_data.txt','w')
User_Management=Manage_User()
def get_tag(node, name):
    return root.getElementsByTagName(name)[0].childNodes[0].data

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
        Recommend_Agent.num=1
        web.header('Content-Type', 'text/xml')
        root = minidom.parseString(data)
        toUser = get_tag(root, 'ToUserName')
        fromUser = get_tag(root, 'FromUserName')
        msgType = get_tag(root, 'MsgType')
        content = get_tag(root, 'Content')
        createTime = int(time.time())
        Recommend_Agent=User_Management.obtain_user_instance(fromUser,createTime)
        if Recommend_Agent.num==0:
            response = Recommend_Agent.get_first_response()
            response="欢迎来到对话推荐系统,CRS向您推荐咖啡等其他饮品"+"友情提示：如果您想离开此系统，请输入q"+'\n'+'开始体验'+'\n'+response
        else:
            if msgType == u'text':
                content = get_tag(root, 'Content')
                #response="nihao"
                response =Recommend_Agent.get_response(content)
            else:
                response = '{} is not supported yet.'.format(msgType.capitalize())
        User_Management.clean_user()
        data={fromUser:content,toUser:response:'time',createTime}
        json_str = json.dumps(data)
        f.write(json_str)
        f.write('\n')
        return wechat.render.response(fromUser, toUser, createTime, response)


if __name__ == "__main__":
    urls = ('/wechat', 'wechat')
    app = web.application(urls, globals())
    app.run()
