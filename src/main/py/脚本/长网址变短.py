import requests
import pyshorteners as psn

import contextlib
from urllib.parse import urlencode
from urllib.request import urlopen
import sys


def long_to_short(url):
    url = psn.Shortener().chilpit.short(url)
    return url


def short_to_long(url):
    res = requests.head(url)
    return res.headers.get("location")

def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' +urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')


if __name__ == '__main__':
    long_link = "https://baijiahao.baidu.com/s?id=1742210929462953021&wfr=spider&for=pc"

    #short_link = long_to_short(long_link)  # 长链接 转 短链接
    #print(f"长链接转为短链接：{short_link}")

    print(make_tiny(long_link))

