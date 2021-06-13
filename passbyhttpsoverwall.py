import requests
import json
import time
import random
import threading
from lxml import etree

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip,deflate",
}

def check_proxy(ip,port):
    try:
        time.sleep(random.random()*12)
        address=requests.get("https://www.cip.cc/",headers=headers,proxies={"https": "{}:{}".format(ip,port)},timeout=15)
        address.encoding="gb2312"
        cip=etree.HTML(address.content)
        pre=cip.xpath("//div[@class='data kq-well']/pre/text()")[0].split("\n")

        if pre[1].find("中国")<0:
            print("{}:{}\n{}\n{}".format(ip,port,pre[1],pre[2]))
    except:
        pass

def get_7yip(page):
    try:
        for i in range(1,51):
            rasp=requests.get("https://www.7yip.cn/free/?action=china&page={}".format(page),headers=headers,timeout=15)
            rasp.encoding="gb2312"
            html=etree.HTML(rasp.content)
            trs=html.xpath("//table[@class='table table-bordered table-striped']/tbody/tr")[1:]

            for tr in trs:
                proxy=tr.xpath("td/text()")
                check_proxy(proxy[0],proxy[1])
    except:
        pass

def get_66ip(page):
    try:
        rasp=requests.get("http://www.66ip.cn/areaindex_{}/1.html".format(page),headers=headers,timeout=15)
        rasp.encoding="gb2312"
        html=etree.HTML(rasp.content)
        trs=html.xpath("//table[@bordercolor='#6699ff']/tr")[1:]

        for tr in trs:
            proxy=tr.xpath("td/text()")
            check_proxy(proxy[0],proxy[1])
    except:
        pass

def get_36ip(stype):
    try:
        rasp=requests.get("http://www.ip3366.net/free/?stype=1&page=1",headers=headers,timeout=15)
        rasp.encoding="gb2312"
        html=etree.HTML(rasp.content)
        count=html.xpath("//font[@color='#FF0000']/text()")[-1]
        pages=int(int(count)/15)+2

        for j in range(1,pages):
            rasp=requests.get("http://www.ip3366.net/free/?stype={}&page={}".format(stype,j),headers=headers,timeout=15)
            rasp.encoding="gb2312"
            html=etree.HTML(rasp.content)
            trs=html.xpath("//table[@class='table table-bordered table-striped']/tbody/tr")
            for tr in trs:
                proxy=tr.xpath("td/text()")
                check_proxy(proxy[0],proxy[1])
    except:
        pass

def get_89ip(proxys):
    for proxy in [p.strip().split(':') for p in proxys]:
        check_proxy(proxy[0],proxy[1])

def get_fatezero(proxys):
    for proxy in [json.loads(p) for p in proxys]:
        check_proxy(proxy["host"],proxy["port"])

if __name__ == '__main__':
    print('''
  ______               _____                     
 |  ____|             |  __ \                    
 | |__ _ __ ___  ___  | |__) | __ _____  ___   _ 
 |  __| '__/ _ \/ _ \ |  ___/ '__/ _ \ \/ / | | |
 | |  | | |  __/  __/ | |   | | | (_) >  <| |_| |
 |_|  |_|  \___|\___| |_|   |_|  \___/_/\_\\__, |
                                            __/ |
                                           |___/ 
''')

    num_7yip=51
    thread_list_7yip = [threading.Thread(target=get_7yip, args=(i,)) for i in range(1,num_7yip)]

    num_66ip=35
    thread_list_66ip = [threading.Thread(target=get_66ip, args=(i,)) for i in range(1,num_66ip)]

    num_36ip=3
    thread_list_36ip = [threading.Thread(target=get_36ip, args=(i,)) for i in range(1,num_36ip)]

    try:
        rasp_89ip=requests.get("http://api.89ip.cn/tqdl.html?api=1&num=800&port=&address=&isp=",headers=headers,timeout=15)
        rasp_89ip.encoding="gb2312"
        html_89ip=etree.HTML(rasp_89ip.content)
        text_89ip=html_89ip.xpath("//text()")
        num_89ip=int(len(text_89ip)/20)
        thread_list_89ip = [threading.Thread(target=get_89ip, args=(text_89ip[num_89ip*20:num_89ip*20+20],)) for i in range(1,num_89ip)]
    except:
        pass

    try:
        rasp_fatezero=requests.get("http://proxylist.fatezero.org/proxy.list",headers=headers,timeout=15)
        rasp_fatezero.encoding="gb2312"
        text_fatezero=rasp_fatezero.text.split("\n")[:-1]
        num_fatezero=int(len(text_fatezero)/20)
        thread_list_fatezero = [threading.Thread(target=get_fatezero, args=(text_fatezero[num_fatezero*20:num_fatezero*20+20],)) for i in range(0,num_89ip)]
    except:
        pass

    for t in thread_list_7yip:
        t.start()
    for t in thread_list_66ip:
        t.start()
    for t in thread_list_36ip:
        t.start()
    for t in thread_list_89ip:
        t.start()
    for t in thread_list_fatezero:
        t.start()

    for t in thread_list_7yip:
        t.join()
    for t in thread_list_66ip:
        t.join()
    for t in thread_list_36ip:
        t.join()
    for t in thread_list_89ip:
        t.join()
    for t in thread_list_fatezero:
        t.join()