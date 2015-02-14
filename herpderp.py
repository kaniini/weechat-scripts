try:
    import weechat
except:
    exit(0)

import random

herps = ['herp', 'HERP', 'Herp',
         'derp', 'DERP', 'Derp']

def derpify_token(tok):
    pos = None
    if tok == tok.lower(): pos = 0
    elif len(tok) > 1 and tok == tok.upper(): pos = 1
    else: pos = 2
    if random.choice(['herp', 'derp']) == 'derp': pos += 3
    return herps[pos]

def derpify(msg):
    return ' '.join([derpify_token(tok) for tok in msg.split()])

# XXX - this should be more configurable.
derpify_targets = [
    # ramnet
    '*!*@*.gavlcmta01.gsvltx.tl.dh.suddenlink.net',

    # shitro
    '*!*theriwolf@*.lightspeed.jcvlfl.sbcglobal.net',

    # some troll probably from tumblr i see everywhere
    '*!*kitsuhana@*.boisestate.edu',
    '*!*kitsuhana@*.bois.qwest.net',
]

def should_derpify(hostmask):
    return 1 in [weechat.string_match(hostmask, target, 0) for target in derpify_targets]    

def privmsg_modifier_cb(userdata, modifier, servername, raw_irc_msg):
    itable = weechat.info_get_hashtable("irc_message_parse", {
        "message": raw_irc_msg,
        "server": servername
    })
    if not should_derpify(itable['host']):
        return raw_irc_msg
    message = itable['arguments'].split(' ', 1)[1]
    if message[0] == ':':
        message = message[1:]
    outmsg = ':{0} PRIVMSG {1} :{2}'.format(itable['host'], itable['arguments'].split(' ')[0], derpify(message))
    return outmsg

if __name__ == '__main__':
    if weechat.register("herpderp", "kaniini", "0.1", "WTFPL", "Selectively replaces text with herp-derp.", "", ""):
        weechat.hook_modifier("irc_in_privmsg", "privmsg_modifier_cb", "")
