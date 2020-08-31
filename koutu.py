# coding: utf8
from removebg import RemoveBg
import requests
import time
import json

# 抠图
def download_img(img_url, imgForder):
    print (img_url)
    header = {"Authorization": "Bearer " + "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"} # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
    r = requests.get(img_url, headers=header, stream=True)
    print(r.status_code) # 返回状态码
    path = imgForder + '/' + str(time.time()) + '.png'
    if r.status_code == 200:
        open(path, 'wb').write(r.content) # 将内容写入图片
        print("done")
        rmbg = RemoveBg("Ugo6aVuLVgBgnfiv5k6Snj8k", "error.log")  # 引号内是你获取的API
        rmbg.remove_background_from_img_file(path)  # 图片地址
    return path + "_no_bg.png"

# 获取素材的mediaID
def get_media_ID(path):
    img_url='https://api.weixin.qq.com/cgi-bin/material/add_material'
    payload_img={
        'access_token':get_token(),
        'type':'image'
    }
    data ={'media':open(path,'rb')}
    r=requests.post(url=img_url,params=payload_img,files=data)
    dict =r.json()
    return dict['media_id']

# 获取access_token
def get_token():
    payload_access_token={
        'grant_type':'client_credential',
        'appid':'wxff2397ecd36364e4',
        'secret':'62e6b6857aba174a6c36622db3e97832'
    }
    token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    r=requests.get(token_url,params=payload_access_token)
    dict_result= (r.json())
    return dict_result['access_token']
