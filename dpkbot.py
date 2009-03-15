#!/usr/bin/python
# -*- coding: utf-8 -*-
from jabberbot.jabberbot import JabberBot
import random
import xmpp
import datetime
import time
from modules import gtools, weather
import codecs

JID='dpk_bot@jabber.kiev.ua'
password='bogdankos'

room_name='dpk@conference.jabber.com.ua'

class DpkJabberBot(JabberBot):
    """This is a jabber bot for the DPK conference, based on JabberBot"""
    
    def __init__(self, jid, password, res = None):
        """Initializes the jabber bot and sets up commands."""
        #super(jid, password, res=res)
        JabberBot.__init__(self,jid,password,res= res)
        self.comid={'ping':{},'version':{}}

    def iqHandler(self, conn, iq_node):
        print "iq received!"
        ns=iq_node
        #version=ns.getTagAttr('query','version')
        version=ns.getTagData('id')
        print unicode(version)+"o-la-la"
        self.send(room_name,'iq request received!')

    def connect( self):
        if not self.conn:
            conn = xmpp.Client( self.jid.getDomain(), debug = [])
            
            if not conn.connect():
                self.log( 'unable to connect to server.')
                return None
            
            if not conn.auth( self.jid.getNode(), self.password, self.res):
                self.log( 'unable to authorize with server.')
                return None
            
            conn.RegisterHandler( 'message', self.callback_message)
            conn.RegisterHandler('iq', self.iqHandler)
            conn.sendInitPresence()
            
            room= room_name+"/Чудик-Юдик"
            print "Joining " + room

            conn.send(xmpp.Presence(to=room))

            self.conn = conn
        return self.conn

    def callback_message( self, conn, mess):
        """Messages sent to the bot will arrive here. Command handling + routing is done in this function."""
        type=mess.getType()
        if type == "chat":
            JabberBot.callback_message(self,conn,mess)
        elif type == "groupchat":
            print unicode(mess.getFrom())+ ': '+ unicode(mess.getBody())
            text = mess.getBody()
            if not text:
                return

            if ' ' in text:
                command, args = text.split(' ',1)
            else:
                command, args = text,''

            cmd=command.lower()
            
            if self.commands.has_key(cmd):
                reply=self.commands[cmd](mess,args)
            else:
                reply=''

            if reply:
                self.send(room_name, reply, mess)

    #def log(self,s):
        #f=codecs.open('dpkbot.log','w','UTF-8')
        #f.write(unicode(s))
        #f.close()

    def bot_srvinfo(self, mess, args):
        """Отображает информацию о сервере"""
        version = open('/proc/version').read()
        return '%s' %(version,)

    def bot_time(self, mess, args):
        """Отображает текущее время сервера"""
        return unicode(datetime.datetime.now())

    def bot_fpnh(self,mess, args):
        """Недокументированная возможность"""
        return u"ЗОБАНЮ ВСЕХ !!!111!111адинадинадин"
    
    def bots_version(self,mess,args):
        if args == '':
            user=mess.getFrom()
            print unicode(user)+") :( :("
        else:
            user=args
            print unicode(user)+":)"
        iq=xmpp.Iq(typ=set, queryNS='jabber:iq:version', attrs={'id':'vers_11'}, to=user, frm=JID, payload=[], xmlns='jabber:iq:version', node=None)
        print "iq sent!"

    def bot_ping(self,mess,args):
        """Пинг себя или пользователя. Использование: ping [пользователь]"""
        if not args:
            user=mess.getFrom()
        else:
            user=room_name+'/'+args.strip()

        self.log(u"Пингуем "+unicode(user))
        iq=xmpp.Iq('get')
        id='ping'+unicode(random.randrange(1, 1000))
        iq.setID(id)
        iq.addChild('query', {}, [], 'jabber:iq:version')
        iq.setTo(user)
        t0=time.time()
        self.comid['ping'][id]=t0
        #self.comid['ping'][id]['time']=t0
        self.conn.SendAndCallForResponse(iq,self.handler_ping_answ,{'t0':t0,'mess':mess,'user':user})
        return ''

    def handler_ping_answ(self, coze, res, t0, mess,user):
        try:
            id=res.getID()
            #user=mess.getFrom()
            if unicode(user).count(room_name) >= 1:
                dummy,user=unicode(user).split('/')
                send_to=room_name
            else:
                send_to=unicode(user)
            if id in self.comid['ping']:
                #self.log(u'id в comid найден')
                #t0=self.comid['ping'][id]
                del self.comid['ping'][id]
            else:
                self.log(u"Ашипка при получении результата пинга :( - неправильный id")
                return
            if res:
                if res.getType() == 'result':
                   t=time.time()
                   rep=u'Понг от '
                   if user:
                       rep+=unicode(user)+' '
                   elif user == unicode(mess.getFrom()):
                       rep+= u'тебя '
                   rep+=unicode(round(t-t0, 3))+u' секунд'
                else:
                   rep= u'не пингуецо'
            self.log(rep)
            #mess=xmpp.Message(room_name, "ir fs!f", mess)
            #self.conn.send(mess)
            #self.send(room_name,"ir ff")
            self.log(send_to)
            self.send(send_to,rep, mess)
        except:
            print "пошли вы..."

    def bot_weather(self,mess,args):
        if not args:
            return u'Ну и что тебе от меня надо?'
        try:
            a=weather.weather(args)
            return a
        except:
            return u'Погода сломалась...'
    
    def bot_google(self,mess,args):
        results=gtools.google_search(args)
        if results:
            return results
        else:
            return u'нету ничего :('

    def bot_srvuptime(self,mess,args):
        """Показывает аптайм сервера"""    
        from math import floor
        up,dummy=open('/proc/uptime').read().split(' ')
        up=float(up)
        all_hours=up/3600
        nf_days=all_hours/24
        days=floor(nf_days)
        nf_hours=24*(nf_days-days)
        hours=floor(nf_hours)
        nf_minutes=60*(nf_hours-hours)
        minutes=floor(nf_minutes)
        res=u'Аптайм сервера '+unicode(int(days))+u' дней '+unicode(int(hours))+u' часов '+unicode(int(minutes))+u' минут'
        return res

bot=DpkJabberBot(JID,password)
bot.serve_forever()
