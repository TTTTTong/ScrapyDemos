from requests import get
from fake_useragent import UserAgent

ua = UserAgent()

url_content = get("https://www.baidu.com/",
                  proxies={"http": '221.228.17.172:8181', "https": '221.228.17.172:8181'},
                  timeout=20,
                  headers={
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding': 'gzip, deflate, compress',
                      'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ru;q=0.4',
                      'Cache-Control': 'max-age=0',
                      'Connection': 'keep-alive',
                      'User-Agent': ua.random
                  })

# if int(url_content.status_code) == int(200):
#     print('-=-=')
print(url_content.status_code)

