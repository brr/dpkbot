# -*- Coding: utf8 -*-

import xmpp
import random
def kick(userJID, room):
    """Kicks user from MUC"""

    #mJID=xmpp.Protocol.JID(moderJID)
    #uJID=xmpp.Protocol.JID(userJID)

    iq=xmpp.Iq('set')
    id='kick'+str(random.randrange(1,1000))
    iq.setID(id)
    iq.setTo(userJID)

    dummy,uNick=userJID.split('/')
    iq.T.query.NT.
