# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import importlib,sys
import requests
import re
import urllib
import ngender
from xpinyin import Pinyin

importlib.reload(sys)

ua=UserAgent()

# 所有文本的入口
def main(xml):
    content = xml.find("Content").text
    if '垃圾' in content:
        index = content.find('垃圾')
        print(content[index + 3:len(content)])
        content = whatisit(content[index + 3:len(content)])
    elif '猜性别' in content:
        index = content.find('猜性别')
        if ngender.guess(content[index + 4:len(content)])[0] == 'male':
            print("(仅供娱乐) 我猜" + content[index + 4:len(content)] + "是" + "一个帅气的男人!! ")
            content = "(仅供娱乐) 我猜" + content[index + 4:len(content)] + "是" + "一个帅气的男人!! "
        else:
            print("(仅供娱乐) 我猜" + content[index + 4:len(content)] + "是" + "一个漂亮的仙女~~~")
            content = "(仅供娱乐) 我猜" + content[index + 4:len(content)] + "是" + "一个漂亮的仙女~~~"
    elif "拼音" in content:
        index = content.find('拼音')
        print(content[index + 3:len(content)])
        content = pingyin(content[index + 3:len(content)])
    elif "翻译" in content:
        index = content.find('翻译')
        print(content[index + 3:len(content)])
        content = fanyi(content[index + 3:len(content)])
    else:
        content = autoReply(content)

    return content

# 查询垃圾
def whatisit(garbage):
    html = get_html('https://lajifenleiapp.com/sk/' + garbage + "?l=" + "大连")

    soup = BeautifulSoup(html, features='lxml')
    print(soup.select("h1")[1].text)
    return soup.select("h1")[1].text


# def get_html(url):
#     try:
#         page = urllib.request.urlopen(url)
#         htmlcode = page.read()
#         # print(htmlcode)
#         return htmlcode.decode('utf-8')
#     except Exception as e:
#         print(e)
#         return None

# 自动回复 利用爬虫 调用网站
def autoReply(txt):
    x = urllib.parse.quote(txt)
    url = "http://nlp.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=%7B%22sessionId%22%3A%22612c741805554d0985d3445ca34d82e9%22%2C%22robotId%22%3A%22webbot%22%2C%22userId%22%3A%22295d61c7759246189a4642921534d9df%22%2C%22body%22%3A%7B%22content%22%3A%22" + x + "%22%7D%2C%22type%22%3A%22txt%22%7D&ts=1593757519960"
    html = get_html(url)
    #取第二个content
    html1 = re.sub('content', 'X', html, 1)
    #取得回复的内容
    reply_list = re.findall(r'"content":"(.*)"', html1)
    #筛选内容
    aa = "emoticons"
    over = ""
    for ii in reply_list:
        resultArr = str(ii).split("\\r\\n")
        i = 0
        for result in resultArr:
            if aa not in result:
                over += result
            i = i + 1

    print(over)
    return over

# 获取网站所有内容
def get_html(url):
    try:
        headers = {"User-Agent": ua.random}
        # 请求网址
        response = requests.get(url=url, headers=headers)
        # # 响应体内容
        # print(response.text)
        return response.text
    except Exception as e:
        print(e)
        return None

# 汉字转拼音
def pingyin(param):
    p = Pinyin()
    result = p.get_pinyin(param, '')
    return result

# 翻译
def fanyi(msg):
    """定义一个函数，完成翻译功能"""
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': msg  # 将输入框输入的值，赋给接口参数
    }
    url = "http://fanyi.youdao.com/translate"
    try:
        r = requests.get(url, params=data)
        if r.status_code == 200:
            result = r.json()
            translate_result = result['translateResult'][0][0]["tgt"]
            print(translate_result)
    except Exception:
        print("翻译发生错误")

    return translate_result

