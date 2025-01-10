import requests
from functools import wraps
import config
debug = config.config["system"]["debug"]

# 自定义一个修改请求的装饰器
def request_proxy(func):
    @wraps(func)
    def wrapper(url, *args, **kwargs):
        # 修改User-Agent头部
        headers = kwargs.get('headers', {})
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

        if "defaultPage.action" in url:
            '''
            GET /eams/stdElectCourse!defaultPage.action?electionProfile.id=1690 HTTP/1.1
            Host: eamis.nankai.edu.cn
            Connection: keep-alive
            sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: "macOS"
            Upgrade-Insecure-Requests: 1
            User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
            Sec-Fetch-Site: same-origin
            Sec-Fetch-Mode: navigate
            Sec-Fetch-User: ?1
            Sec-Fetch-Dest: document
            Referer: https://eamis.nankai.edu.cn/eams/stdElectCourse.action
            Accept-Encoding: gzip, deflate, br, zstd
            Accept-Language: zh-CN,zh;q=0.9
            Cookie: srv_id=xxx; JSESSIONID=xxx.std6
            '''
            # 修改Referer头部
            headers['Referer'] = 'https://eamis.nankai.edu.cn/eams/stdElectCourse.action'
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
            headers['Sec-Fetch-Site'] = 'same-origin'
            headers['Sec-Fetch-Mode'] = 'navigate'
            headers['Sec-Fetch-User'] = '?1'
            headers['Sec-Fetch-Dest'] = 'document'
            headers['Accept-Encoding'] = 'gzip, deflate, br, zstd'
            headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
            headers['Upgrade-Insecure-Requests'] = '1'
            headers['sec-ch-ua'] = '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"'
            headers['sec-ch-ua-mobile'] = '?0'
            headers['sec-ch-ua-platform'] = '"macOS"'
            

        kwargs['headers'] = headers

        # 加入webvpn功能（正在开发中）
        if config.config['system']['webvpn'] and isinstance(url, str) and "example.com" in url:
            url = url.replace("example.com", "mycustompage.com")

        kwargs['verify'] = False  # 关闭SSL验证

        # 代理设置
        #kwargs['proxies'] = {"https": "socks5://127.0.0.1:8083"}
        
        # 调用原始请求函数
        return func(url, *args, **kwargs)
    return wrapper

# 代理requests.get
@request_proxy
def requests_get(url, **kwargs):
    if debug:
        print("GET", url)
        a = requests.get(url, **kwargs)
        print(a.status_code, a.text[:10], ' ... ', a.text[-10:])
        return a
    else:
        return requests.get(url, **kwargs)
        

# 代理requests.post
@request_proxy
def requests_post(url, data=None, **kwargs):
    if debug:
        print("POST", url, data)
        a = requests.post(url, data=data, **kwargs)
        print(a.status_code, a.text[:10], ' ... ', a.text[-10:])
        return a
    else:
        return requests.post(url, data=data, **kwargs)


if __name__ == "__main__":
    response = requests_get("https://www.baidu.com")
    print(response.text)
    
    response = requests_post("https://www.baidu.com", data={"key": "value"})
    print(response.text)