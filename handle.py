# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import time
import os
from lxml import etree
import koutu
import text

class Handle(object):

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "q10viking"

            list = [token, timestamp, nonce]
            list.sort()
            s = list[0] + list[1] + list[2]
            hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return echostr
        except (Exception) as Argument:
            return Argument

    def POST(self):
        str_xml = web.data()  # 获得post来的数据
        print(str_xml)
        xml = etree.fromstring(str_xml)  # 进行XML解析
        print(xml)
        msgType = xml.find("MsgType").text
        print(msgType)
        fromUser = xml.find("FromUserName").text
        print(fromUser)
        toUser = xml.find("ToUserName").text
        print(toUser)
        if msgType == 'text':
            content = text.main(xml)
            return self.render.reply_text(fromUser, toUser, int(time.time()), content)
        elif msgType == 'image':
            # 取得图片的url
            img_url = xml.find("PicUrl").text
            # 服务器存放文件的路径
            imgForder = os.path.join(self.app_root, 'koutu')
            # 下载用户上传的图片
            path = koutu.download_img(img_url, imgForder)

            print(path)
            # 获取素材的mediaID
            mediaId = koutu.get_media_ID(path)

            return self.render.reply_image(fromUser, toUser, int(time.time()), mediaId)
            pass
        else:
            pass
