# -*- coding: utf-8 -*-
import urllib
from xml.dom import minidom
## Вычисление города
def weather(city):
    xx = urllib.quote_plus(city.encode('cp1251'))
    u = urllib.urlopen('http://search.gismeteo.ua/?town=%s&req=findtown'%xx)
    dd = u.read()
    x = dd.find('http://www.gismeteo.ua/towns/')
    idx = dd[x:dd.find('.htm',x)].split('/')[-1].strip()
    if idx:
    	ret = u'Погода:\n'
    	r = urllib.urlopen('http://informer.gismeteo.ua/rss/%s.xml'%idx)
    	dom = minidom.parse(urllib.urlopen('http://informer.gismeteo.ua/rss/%s.xml'%idx))
    	for x in dom.getElementsByTagName('item'):
    		ret += '%s: %s\n'%(x.getElementsByTagName('title')[0].firstChild.data.strip(),x.getElementsByTagName('description')[0].firstChild.data.strip())
    	return ret
    else: 
        u = urllib.urlopen('http://search.gismeteo.ru/?town=%s&req=findtown'%xx)
        dd = u.read()
        x = dd.find('http://www.gismeteo.ru/towns/')
        idx = dd[x:dd.find('.htm',x)].split('/')[-1].strip()
        if idx:
        	ret = u'Погода:\n'
        	r = urllib.urlopen('http://informer.gismeteo.ru/rss/%s.xml'%idx)
        	dom = minidom.parse(urllib.urlopen('http://informer.gismeteo.ru/rss/%s.xml'%idx))
        	for x in dom.getElementsByTagName('item'):
        		ret += '%s: %s\n'%(x.getElementsByTagName('title')[0].firstChild.data.strip(),x.getElementsByTagName('description')[0].firstChild.data.strip())
        	return ret
        else:
            return u'Город "'+parameters+ u'" не найден =('

