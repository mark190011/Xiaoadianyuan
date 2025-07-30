##config_set.py

from set_database import set_admincode, set_groupname, set_group_nickname
import os

#1.设置4位管理员码，用于认证管理员vx身份，设置和控制小a店员功能

admincode = '4050'
#这里'****'为你设置的管理员码
#Here, "****" represents a 4-digit administrator code set by the developer.
admin_result = set_admincode(admincode)
print(admin_result)

#2.新添加需要监控的群名

groupname = '12136'
#其中"****"为你在群设置中, 复制的"群聊名称”,  包括vx群名内的表情包，特殊字符等
#Here, "****" refers to the "group chat name" that you have copied from the group settings, including emojis, special characters, etc., within the vx group name.
group_result = set_groupname(groupname)
print(group_result)

#3.设置群内监控的机器人昵称

nickname = '小a店员'
#其中"****"为你在群内, 设置的监控机器人vx昵称，当其它群内用户@nickname时，机器人才会回复
#Where '****' is the vx nickname of the monitoring bot you set up in the group. The bot will only reply when other group members @ the nickname.
#不设置的状态下，默认为"小a店员"，请手动在微信内修改vx群昵称为"小a店员"
nickname_result = set_group_nickname(nickname)
print(nickname_result)


