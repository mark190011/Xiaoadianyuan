# Xiaoadianyuan 小a店员
## 前言
基于wxauto开发的 ，应用UIAutoanimation, Context上下文工程和逻辑链的自主vx回复和活动系统Agent.    
An agent system developed based on wxauto, which applies UIAutoanimation, utilizes Context engineering, and implements logical chains for autonomous vx reply functionality and activity systems.

主要服务于餐饮创业者及其它线下/线上店铺场景。    
Xiaoadianyuan mainly serves catering entrepreneurs and other offline/online store scenarios.

### 文件架构
main:.
├─apache-maven-3.9.9
├─flask_session
├─holiday_pic
├─image
├─pcm
├─picstore
├─post_pic
├─sessions
├─static
├─target
├─utils
├─wxauto
├─wxauto文件
└─__pycache__
│
│  bot_start.py
│  holiday_module.py
│  operation_module.py
│  random_number.db
│  README.md
│  requirements.txt
│  xiaoadianyuan.ico

## 开始
***请使用vx3.9.12

### 安装依赖
python > 3.10

powershell
 pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#建议使用国内镜像，最近通用库很慢

### 设置管理员码
powershell
 sqlite3 random_number.db "INSERT INTO random_number_set (value) VALUES ('****');"
#其中"****"为开发者设置的4位管理员码

sqlite3:https://www.sqlite.org/download.html
### 启动bot
powershell
 python start_schedule.py
#第一次启动会自动获得token

## 功能介绍

- 管理员设置/AdminAgent

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/AdminAgent.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/HelpAgent.jpg" width="300">
- 可学习的顾客chat/CostomerAgent

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/CostomerAgent.jpg" width="300">

- 群内氛围和投诉保护/Protect

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Protect_Rules.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Protect_Complaint.jpg" width="300">

- 线索捕获/CostomerLeads

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/CostomLeads1.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/CostomLeads2.jpg" width="300">

- 菜单识别/MenuRead

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Menuread_Pic.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Menuread_Handwright.jpg" width="300">
 可识别图片菜单和手写菜单    It can recognize both cellphone menu images and handwritten menus.
- 图片识别/话术生成/PicRead

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Picread_Wordgen.jpg" width="300">
- 日常运营/DailyOP

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/Hotpoint.jpg" width="300">    <img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/DailyOP_Pic.jpg" width="300">
 可自动搜索每日热点，生成话题/每日自主选择不同的运营图片，形成话题    It can automatically search for daily hot topics, generate discussion themes, and independently select different operational images each day to form engaging topics.
- 活动运营/HolidayOP

<img src="https://github.com/mark190011/Xiaoadianyuan/blob/main/img_folder/HolidayOP.jpg" width="300">
 自动生成活动方案，自动生成活动海报，按照日期自动执行    It can automatically generate activity plans, create activity posters, and execute them automatically according to the scheduled dates.

### 项目架构
![Image text](https://github.com/mark190011/Xiaoadianyuan/blob/main/prog_structure.png)

