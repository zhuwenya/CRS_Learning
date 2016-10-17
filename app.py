import web
import hashlib
import xml.dom.minidom as minidom
import backend
from backend import *
import time

Recommend_Agent=recommend_agent()
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
       
        print(Recommend_Agent.num)
        if Recommend_Agent.num==0:
            data=web.data()
            Recommend_Agent.num=1
            web.header('Content-Type', 'text/xml')
            return self.process_zero_message()          
        elif(Recommend_Agent.num==1):
            data = web.data()
            Recommend_Agent.num=2
            web.header('Content-Type', 'text/xml')
            return self.process_first_message(data)
        elif(Recommend_Agent.num==2):
            data = web.data()
            Recommend_Agent.num=3
            web.header('Content-Type', 'text/xml')
            return self.process_second_message(data)
        else:
            data = web.data()
            web.header('Content-Type', 'text/xml')
            return self.process_message(data)

    def process_zero_message(self):
        def get_tag(node, name):
            return root.getElementsByTagName(name)[0].childNodes[0].data
        root = minidom.parseString(message)
        toUser = get_tag(root, 'ToUserName')
        fromUser = get_tag(root, 'FromUserName')
        msgType = 'text'
        response = self.Recommend_Agent.get_zero_response()
        createTime = int(time.time())
        return wechat.render.response(fromUser, toUser, createTime, response)

    def process_first_message(self,message):
        def get_tag(node, name):
            return root.getElementsByTagName(name)[0].childNodes[0].data
        root = minidom.parseString(message)
        toUser = get_tag(root, 'ToUserName')
        fromUser = get_tag(root, 'FromUserName')
        msgType ='text'
        response = Recommend_Agent.get_first_response()
        createTime = int(time.time())
        return wechat.render.response(fromUser, toUser, createTime, response)

    def process_second_message(self):
        def get_tag(node, name):
            return root.getElementsByTagName(name)[0].childNodes[0].data
        root = minidom.parseString(message)
        toUser = get_tag(root, 'ToUserName')
        fromUser = get_tag(root, 'FromUserName')
        msgType = 'text'
        response = self.Recommend_Agent.get_zero_response()
        createTime = int(time.time())
        return wechat.render.response(fromUser, toUser, createTime, response)
    def process_message(self, message):
        def get_tag(node, name):
            return root.getElementsByTagName(name)[0].childNodes[0].data
        root = minidom.parseString(message)
        toUser = get_tag(root, 'ToUserName')
        fromUser = get_tag(root, 'FromUserName')
        msgType = get_tag(root, 'MsgType')

        if msgType == u'text':
            content = get_tag(root, 'Content')
            #response="nihao"
            response =Recommend_Agent.get_response(content)
        else:
            response = '{} is not supported yet.'.format(msgType.capitalize())
        createTime = int(time.time())
        return wechat.render.response(fromUser, toUser, createTime, response)


if __name__ == "__main__":
    urls = ('/wechat', 'wechat')
    app = web.application(urls, globals())
    app.run()
