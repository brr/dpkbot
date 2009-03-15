# -*- coding: utf-8 -*-
import urllib
import simplejson

def remove_html(text):
	nobold = text.replace('<b>', '').replace('</b>', '')
	nobreaks = nobold.replace('<br>', ' ')
	noescape = nobreaks.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	return noescape

def google_search(query):
    if not query:
        return u"Ну и че те надо, а?"
    
    try:
        qr=urllib.quote_plus(unicode(query).encode('utf-8'),'/')
        quer = urllib.urlencode({'q' : qr })
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&hl=ru&%s' %(quer)
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        results = json['responseData']['results']
        res=unicode(results[0]['title']) + ": " + unicode(results[0]['url'])+"\n"+unicode(results[0]['content'])
        res=remove_html(res)
        return res
    except:
        return "бяка ты :("



