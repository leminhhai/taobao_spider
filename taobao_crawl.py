# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:54:20 2018

@author: Lynn
"""

import re
import requests
import json

def openurl(keyword,page):
    params = {'q':keyword,'sort':'sale-desc','s':str(page*44)} #字典中第二项是按销量排序
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    url = "https://s.taobao.com/search"
    res = requests.get(url,params=params, headers=headers)
    return res

def get_items(res):
    g_page = re.search(r'g_page_config = (.*?);\n', res.text)
    g_page_json = json.loads(g_page.group(1))
#    p_items = g_page_json['mods']['itemlist']['data']['auctions']
#    p_items = g_page_json['mods']['nav']['data']['common']
    p_items = g_page_json['mods']['grid']['data']['spus']    
    result = []
    for each in p_items:
        dict_items = dict.fromkeys(('title','pic_url','price','importantKey','month_sales','cmt_count','url'))
        dict_items['title'] = each['title']
        dict_items['pic_url'] = each['pic_url']
        dict_items['price'] = each['price']
        dict_items['importantKey'] = each['importantKey']
        dict_items['month_sales'] = each['month_sales']
        dict_items['cmt_count'] = each['cmt_count']
        dict_items['url'] = each['url']
        result.append(dict_items) 
    return result
 
def sale_num(items):
    count = 0
    for each in items:
        count += int(each['price'])
    return count

def main():
    keyword = input("请输入需要搜索销量的商品：")
    print(type(keyword))
    page_num = 3
    total_sale_num = 0
    for page in range(page_num):
        res = openurl(keyword,page)
        item = get_items(res)
        total_sale_num += sale_num(item)
    print('总销量为:',total_sale_num)
    
    
if __name__ == "__main__":
    main()

















