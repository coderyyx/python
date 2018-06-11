# -*- coding: utf-8 -*-
import requests
import urllib
import threading

thread_lock = threading.BoundedSemaphore(value=10)
# url:https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%A0%A1%E8%8A%B1&start=0&limit=1000
def get_page(url):
    page = requests.get(url)
    content = page.content
    # decode
    content = content.decode('utf-8')
    return content

def findall_from_response(page,startpart,endpart):
    all_string = []
    end = 0
    while page.find(startpart,end) != -1:
        start = page.find(startpart,end) + len(startpart)
        end = page.find(endpart,start)
        string = page[start:end]
        all_string.append(string)
    return all_string

def pages_from_duitang(label):
    pages = []
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=1000'
    # label = urllib.parse.quote(label)
    label = urllib.quote(label)
    for index in range(0,3600,100):
        u = url.format(label,index)
        print(u)
        page = get_page(u)
        pages.append(page)
    return pages


def pic_urls_form_pages(pages):
    pic_urls = []
    for page in pages:
        urls = findall_from_response(page,'path":"','"')
        pic_urls.extend(urls)
    return pic_urls


def download_pics(url,n):
    r = requests.get(url)
    path = 'pics/' + str(n) + '.jpg'
    with open(path,'wb') as f:
        f.write(r.content)
    thread_lock.release()

def main(kw):
    pages = pages_from_duitang(kw)
    pic_urls = pic_urls_form_pages(pages)
    n = 0
    for url in pic_urls:
        n += 1
        print('正在下载{}张'.format(n))
        thread_lock.acquire()
        t = threading.Thread(target=download_pics,args=(url,n))
        t.start()

main('校花')