try:
    import weechat
except:
    exit(0)


KLINETRACE_UNTIL = None


def klinetrace_cmd_cb(data, buffer, args):
    global KLINETRACE_UNTIL

    KLINETRACE_UNTIL = args
    weechat.command("", "/quote ETRACE")
    return weechat.WEECHAT_RC_OK


def etrace_modifier_cb(userdata, modifier, servername, raw_irc_msg):
    global KLINETRACE_UNTIL

    itable = weechat.info_get_hashtable("irc_message_parse", {
        "message": raw_irc_msg,
        "server": servername
    })
    args = itable['arguments'].split(' ')
    user_nick = args[3]
    user_host = args[6]
    if not KLINETRACE_UNTIL:
        return raw_irc_msg
    if KLINETRACE_UNTIL == user_nick:
        KLINETRACE_UNTIL = None
        return raw_irc_msg
    weechat.command('', '/quote kline 10080 *@%s :bots' % (user_host))
    return raw_irc_msg


if __name__ == '__main__':
    if weechat.register("klinetrace", "kaniini", "0.1", "WTFPL", "A crude botnet removal tool.", "", ""):
        weechat.hook_command("klinetrace",
                             "A crude botnet removal tool.", "last_known_good_client", "", "", "klinetrace_cmd_cb", "")
        weechat.hook_modifier("irc_in_709", "etrace_modifier_cb", "")
