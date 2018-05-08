#code:utf-8
import requests
from bs4 import BeautifulSoup
import json
import time

total_video = 0
host = 'https://www.kuaishou.com'
filename = "urls.txt"
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection":"keep-alive",
    "Cookie":"",
    "Host":"www.kuaishou.com",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
}
def download(userid,count):
    url = 'http://www.gifshow.com/user/' + str(userid)    #主播主界面
    resp = requests.get(url,allow_redirects=False)    #禁用重定向，获取被重定向之前的头部信息来获取主播id
    soup = BeautifulSoup(resp.text, 'html.parser')
    principalId = resp.headers['Location'].split('/')[4]   #获取重定向后的主播id
    s = json.dumps({'principalId':principalId,'count':count})  #请求主体用json形式传输，否则会报400错误
    json_url = 'https://live.kuaishou.com/feed/profile'
    resp = requests.post(json_url,data=s)
    soup = BeautifulSoup(resp.text, 'html.parser')
    myjson = json.loads(str(soup))
    with open(filename,"a+") as f:
        for i in range (0,count):
            photoId = myjson['list'][i]['photoId']    #解析json获取photoid
            live_url = host + '/photo/' + principalId + '/' + photoId     #某个具体视频的id = host + 主播id + photoid
            video_url = get_video_url(live_url)
            if (video_url != None):
                f.write(video_url+"\n")
#            time.sleep(5)      #沉睡五秒，否则将无法获取到视频url，可能有反爬机制
    f.close()

def get_video_url(live_url):
    resp = requests.get(live_url,headers=headers)       #此处必须要加请求头，否则请求到的数据为None
    soup = BeautifulSoup(resp.text, 'html.parser')
    video_div = soup.find('div', {'class': 'video'})
    if (video_div != None):
        video_url = video_div.find_all('video')
        global total_video    #把total_video声明为全局变量
        total_video = total_video + 1
        print ('已爬取' + str(total_video) + '个视频url')
        return video_url[0].attrs['src']
    else:
        return None

if __name__ == '__main__':
    download(16860628,125)   #用户id和需要下载的视频数量
    print ('爬取完毕，总共爬取了' + str(total_video) + '个视频url')
