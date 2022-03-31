COMMAND = "!hyp"

def func(msg, command_list):
    if msg.text == "!hyp players":
        _all_modes = hypixel.getJSON("counts")
        _all_player = _all_modes["playerCount"]
        _all_modes = _all_modes["games"]
        _all_players = []
        for i in _all_modes:
            _all_players.append(_all_modes[i]["players"])
        
        temp_msg = ""
        temp_list = []
        for i in _all_modes.items():
            temp_list.append(i)
        for i in range(len(_all_modes)):
            try:
                temp_msg += "{}: {} ({}%)\n".format(temp_list[i][0], _all_players[i], round((_all_players[i]/_all_player)*100, 2))
            except Exception as e:
                print(e)
        print(temp_msg)
        msg.fastReply("[CQ:image,file=base64://{}]".format(text2image(temp_msg)))
        return
    
    if command_list[0] == "!hyp":
        if len(command_list) == 1:
            msg.fastReply("格式貌似有点问题?\n访问 https://lingbot.guimc.ltd/#/Commands 找一找你想要的功能罢")
            return

        # 获取玩家信息
        try:
            player1 = hypixel.Player(command_list[1])
        except hypixel.PlayerNotFoundException:
            msg.fastReply("貌似没有这个玩家?\n访问 https://lingbot.guimc.ltd/#/Commands 找一找你想要的功能罢")
            return
        pI = player1.getPlayerInfo()
        print(pI)
        if "lastLogin" not in pI:
            pI["lastLogin"] = 0
        if 'karma' not in pI:
            pI["karma"] = "0"
        playerSkin = requests.get("https://crafatar.com/renders/body/" + pI["uuid"])

        lastLogout = 0
        if "lastLogout" in player1.JSON:
            lastLogout = player1.JSON["lastLogout"]
        
        onlineMode = None
        try:
            _onlineStatus = hypixel.getJSON("status", uuid=pI["uuid"])["session"]
            _isOnline = _onlineStatus["online"]
            if _isOnline:
                onlineMode = "Online: {} - {} ({})".format(_onlineStatus["gameType"], _onlineStatus["mode"], _onlineStatus["map"])
            else:
                onlineMode = "Offline"
        except:
            pass

        pmsg = """注: 当前为测试版本 不代表最终体验
---查询结果---
玩家名称: [{rank}]{name}
等级: {level}
Karma(人品值): {karma}
上次登陆: {last_login}
上次登出: {lastLogout}[{onlineMode}]
首次登陆: {first_login}""".format(
            rank = player1.getRank()["rank"].replace(" PLUS", "+"),
            name = pI["displayName"],
            level = player1.getLevel(),
            karma = pI["karma"],
            last_login = datetime.datetime.utcfromtimestamp(pI["lastLogin"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            first_login = datetime.datetime.utcfromtimestamp(pI["firstLogin"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            onlineMode = onlineMode,
            lastLogout = datetime.datetime.utcfromtimestamp(lastLogout / 1000).strftime("%Y-%m-%d %H:%M:%S"))

        if playerSkin.status_code == 200:
            pmsg = "[CQ:image,file=base64://" + base64.b64encode(playerSkin.content).decode() + "]\n" + pmsg

        try:
            sbplayer = hypixel.getJSON('skyblock/profiles', uuid=pI['uuid'])
            profile_id = sbplayer["profiles"][0]["profile_id"]
            sbprofile = sbplayer["profiles"][0]["members"][profile_id]
            finished_quests = 0
            for i in sbprofile["quests"]:
                if sbprofile["quests"][i]["status"] == "COMPLETE":
                    finished_quests += 1
            pmsg += """\n---SkyBlock---
Profile ID: {profile_id}
上次保存: {last_save}
第一次进入: {first_join}
Coins: {coin_purse}
已经完成的任务: {finished_quests}
进入过的区域: {visited_zones}个
死亡次数: {death_count}""".format(profile_id=profile_id,
                          last_save=datetime.datetime.utcfromtimestamp(sbprofile["last_save"] / 1000).strftime(
                              "%Y-%m-%d %H:%M:%S"),
                          first_join=datetime.datetime.utcfromtimestamp(sbprofile["first_join"] / 1000).strftime(
                              "%Y-%m-%d %H:%M:%S"),
                          coin_purse=sbprofile["coin_purse"],
                          finished_quests=finished_quests,
                          visited_zones=len(sbprofile["visited_zones"]),
                          death_count=sbprofile["death_count"])
        except:
            print(traceback.format_exc())
        msg.fastReply(pmsg)