import web
import hashlib
import xml.dom.minidom as minidom
import backend
import time

class wechat:
    render = web.template.render('templates/')

    def __init__(self):
        self.Recommend_Agent=recommend_agent()
        self.num=0

    def GET(self):
        # For developer verification
        get_params = web.input()
        token = "topcoderjimmy"
        signature = get_params.signature
        timestamp = get_params.timestamp
        nonce = get_params.nonce
        echostr = get_params.echostr

        array = [token, timestamp, nonce]
        array.sort()
        checkstr = hashlib.sha1(''.join(array)).hexdigest()
        return echostr if checkstr == signature else 'Fail'

    def POST(self):
        if self.num==0:
            return self.process_first_message()
            self.num+=1
        else:
            data = web.data()
            web.header('Content-Type', 'text/xml')
            return self.process_message(data)

    def process_first_message(self):
        def get_tag(node, name):
            return root.getElementsByTagName(name)[0].childNodes[0].data
        root = minidom.parseString(message)
        toUser = get_tag(root, 'ToUserName')
        fromUser = get_tag(root, 'FromUserName')
        #msgType = get_tag(root, 'MsgType')
        response = self.Recommend_Agent.get_first_response()
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
            response = self.Recommend_Agent.get_response(content)
        else:
            response = '{} is not supported yet.'.format(msgType.capitalize())
        createTime = int(time.time())
        return wechat.render.response(fromUser, toUser, createTime, response)


if __name__ == "__main__":
    urls = ('/wechat', 'wechat')
    app = web.application(urls, globals())
    app.run()
