##config_set.py

from set_database import set_admincode, set_groupname
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