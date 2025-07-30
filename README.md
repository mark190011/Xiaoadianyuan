# Xiaoadianyuan 小a店员
## 🔍前言 Introduction
基于wxauto开发的 ，应用UIAutoanimation, Context上下文工程和逻辑链的自主vx回复和活动系统ai Agent.  
An ai agent system developed based on wxauto, which applies UIAutoanimation, utilizes Context engineering, and implements logical chains for autonomous vx reply functionality and activity systems.

> 主要服务于餐饮创业者及其它线下/线上店铺场景。   
> Xiaoadianyuan mainly serves catering entrepreneurs and other offline/online store scenarios.

### 📚文件结构 File Structure
```
main:.
├─holiday_pic
├─image
├─pcm
├─picstore
├─post_pic
├─sessions
├─static
├─target
├─wxauto
├─wxauto文件
└─__pycache__
│
│  start_schedule.py
│  bot_start.py
│  holiday_module.py
│  operation_module.py
│  set_database.py
│  config_set.py
│  Turn_Screen.py
│  random_number.db
│  README.md
│  requirements.txt
│  xiaoadianyuan.ico
```
## 💻开始 Start
***请使用vx3.9.12   
***wxauto内部分功能已修改，请勿使用原生wxauto包替换本项目内文件   
***Some internal functions of wxauto have been modified. Please do not replace the files in this project with the original wxauto package.
### 安装依赖 Prerequisites
python > 3.10

```powershell
 pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#建议使用国内镜像，最近通用库很慢
```

### 初始设置 Initial Setup
sqlite3:https://www.sqlite.org/download.html

```python
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
```
- 运行设置
- Apply the settings
```powershell
 python config_set.py
```
### 启动bot StartBot
```powershell
 python start_schedule.py

#第一次启动会自动获得token
#A token will be automatically obtained upon the first launch.

#请将监控账号，群昵称改为"小a店员"
```

## 🎈功能介绍 Features

- 管理员设置/AdminAgent

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/AdminAgent.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/HelpAgent.jpg" width="300">
- 可学习的顾客chat/CustomerAgent

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/CostomerAgent.jpg" width="300">

- 群内氛围和投诉保护/Protect

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Protect_Rules.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Protect_Complaint.jpg" width="300">

- 线索捕获/CustomerLeads

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/CostomLeads1.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/CostomLeads2.jpg" width="300">

- 菜单识别/MenuRead

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Menuread_Pic.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Menuread_Handwright.jpg" width="300">

 > 可识别图片菜单和手写菜单    
 > It can recognize both cellphone menu images and handwritten menus.
- 图片识别/话术生成/PicRead

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Picread_Wordgen.jpg" width="300">
- 日常运营/DailyOP

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Hotpoint.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/DailyOP_Pic.jpg" width="300">

 > 可自动搜索每日热点，生成话题/每日自主选择不同的运营图片，形成话题    
 > It can automatically search for daily hot topics, generate discussion themes, and independently select different operational images each day to form engaging topics.
- 活动运营/HolidayOP

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/HolidayOP.jpg" width="300">

 > 自动生成活动方案，自动生成活动海报，按照日期自动执行    
 > It can automatically generate activity plans, create activity posters, and execute them automatically according to the scheduled dates.

### 项目架构 Project Structure
![Image text](https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/prog_structure.png)

## 🏠其它 Other

### 版本记录 Release Notes
- 2025/7/22 基础版本发布 July 22, 2025 – Base Version Released
>用户回复 User Reply    
>管理员设置 Administrator Settings    
>菜单识别/图片描述 Menu Recognition / Image Description    
>群保护 Group Protection

- 2025/7/23 活动运营模块更新 July 23, 2025 – Update to the Activity Operations Module
>每日热点话题 Daily Hot Topics    
>图片运营 Visual Content Management    
>节日活动运营 Holiday Event Operations    

- 2025/7/30 功能更新 July 30, 2025 – Function Enhancement
>增加防止熄屏功能 Enable Keep-Screen-On Functionality        
>用户可设置群内Bot昵称 Allow Users to Set Bot Names Within Groups    

### 交流 Community
欢迎大家提出建议和改进意见：mark@hotblaz.com   
We welcome your suggestions and ideas for improvement. Please feel free to contact us at mark@hotblaz.com.
### API/MCP
其它版本，更多功能和调用详情，请登录[API/MCP文档](https://c191evo3qj.apifox.cn/328099878e0)    
For other versions, more features, and detailed usage instructions, please visit [API/MCP files](https://c191evo3qj.apifox.cn/328099878e0).
### 免责声明 Disclaimer
代码仅用于技术的交流学习使用，请勿用于非法用途和商业用途！如因此产生任何法律纠纷，均与作者无关！   
The code is provided solely for technical exchange and learning purposes. Please refrain from using it for any illegal or commercial activities. The author shall not be held liable for any legal disputes arising from such usage.

### 证书 License

[MIT LICENSE](LICENSE)

