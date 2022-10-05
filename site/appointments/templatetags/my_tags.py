from django import template
from django.http import QueryDict
from django.template.defaulttags import register

register = template.Library()

@register.simple_tag
def my_relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url

@register.simple_tag
def my_paginator(key, total_pages='', current_page='')->None|int:
    d = {'key':'val'}
    'ну короче тут можно логику нормальную прописать со страницами'
    return d.get(key)

@register.simple_tag
def remove_date(url:QueryDict, field_to_remove:str):
    query = dict(url)
    query.pop(field_to_remove,'')

    res_url = ''
    for k,v in query.items():
        s = f'&{k}={v[0]}'
        res_url += s

    print('res_url--',res_url)
    return res_url

