# Update Oray IP
#
# Update Log:
# 2021-12-4 09:17:27 - Fix fake death state
#
# ByXiaoXie   Www.ByXiaoXie.Com

import time
import re
import base64
import urllib
from urllib import request

domainname = ""
username = ""
password = ""

user_info_str = username + ":" + password
user_info = base64.b64encode(user_info_str.encode())

headers = {
'Host': 'ddns.oray.com',
'Authorization': "Basic " + user_info.decode(),
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
}

def print_log(str):
    if not str.strip():
        return
    str = str.replace("\r","").replace("\n","")
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(now + "：" + str)

    with open("oray.log","a") as file:
            file.write(now + "：" + str + "\n")

def GetIp():
    try:
        req = request.Request("http://ipinfo.io/ip")
        conn = request.urlopen(req,timeout=10).read().decode('GBK')
        ipaddr = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',conn)
        ipaddress = ipaddr.group()
        return ipaddress
    except:
        print_log("Get IP Time Out!")
        return ""

def UpdateIP():
    try:
        while True:
            ipaddress = GetIp()
            if ipaddress != "":
                break
            else:
                time.sleep(5)
                ipaddress = GetIp()
        url = "http://ddns.oray.com/ph/update?hostname=" + domainname + "&myip=" + ipaddress
        req = request.Request(url,headers=headers)
        getpost = request.urlopen(req,timeout=10).read().decode('utf-8')
        print_log(getpost)
        
        return True
    except:
        print_log("Update Error!")
        return False

if __name__ == "__main__":
    while True:
        UpdateIP()
        time.sleep(120)