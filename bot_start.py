
# 监听机器人，除了这个，其它全留给服务器的bot
from wxauto import WeChat

# 标准库
import time
import sqlite3
import re
import glob
import os
import datetime
import json
from collections import Counter
import tkinter as tk
import threading
import asyncio
import aiofiles
import base64
import concurrent.futures
#import start_schedule

#################服务器机器人######################
from sever_bot import sever_bot

#start_schedule.start_schedules()
################环境变量除了监听机器人，都留给服务器Bot,如果需要调整的话，后边再调整############################
wx = WeChat()
######################函数定义全部给服务器bot################################################

#friend_infos = wx.GetAllFriends()
#group_info = wx.GetAllRecentGroups()

#friend_list = [friend['remark'] if friend['remark'] is not None else friend['nickname'] for friend in friend_infos]

# 定义获取 friend_list 的函数

###############################################以下是获取好友列表，留给客户端bot#################
# 定义显示遮罩层的函数
def get_group_names():
    try:
        # 连接数据库
        conn = sqlite3.connect('random_number.db')
        cursor = conn.cursor()
        # 查询 group_name 列的所有值
        cursor.execute('SELECT group_name FROM group_name')
        results = cursor.fetchall()
        # 将结果转换为列表
        group_names = [item[0] for item in results]
        return group_names
    except Exception as e:
        print(f'获取群名时出错: {e}')
        return []
    finally:
        if conn:
            conn.close()

def show_mask():
    try:
        print('开始创建遮罩层窗口...')
        root = tk.Tk()
        # 设置窗口置顶
        root.wm_attributes('-topmost', True)
        print('窗口已创建，设置置顶属性。')
        # 设置窗口大小和位置
        root.geometry('400x200+500+300')
        # 隐藏标题栏
        root.overrideredirect(True)
        # 设置半透明
        # 假设原有的透明度设置如下，将 alpha 值调小以减小透明度
        # 例如从 0.5 减小到 0.2
        root.attributes('-alpha', 0.65)
        # 创建提示标签，修改字体和颜色
        label = tk.Label(root, text='正在启动监听，请勿移动鼠标。。', font=('微软雅黑', 16), fg='darkblue')
        label.pack(pady=50)
        print('提示标签已创建。')
        # 设置 10 秒后自动关闭
        root.after(10000, root.destroy)
        print('已设置 10 秒后自动关闭。')
        # 保持窗口更新
        root.mainloop()
    except Exception as e:
        print(f'创建遮罩层时发生错误: {e}')

def get_random_number_token():
        # 这里实现获取最新随机值的逻辑
        # 示例代码，需要根据实际情况修改
        try:
            conn = sqlite3.connect('random_number.db')
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM random_number ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            if result:
                return str(result[0])  # 确保返回的是字符串类型
            else:
                return "default_token"  # 如果没有记录，返回一个默认token
        except Exception as e:
            print(f"数据库查询出错: {e}")
            return "default_token"  # 出错时返回默认token
        finally:
            if conn:
                conn.close()

def get_random_number():
        # 这里实现获取最新随机值的逻辑
        # 示例代码，需要根据实际情况修改
        try:
            conn = sqlite3.connect('random_number.db')
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM random_number_set ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            if result:
                return str(result[0])  # 确保返回的是字符串类型
            else:
                return "default_token"  # 如果没有记录，返回一个默认token
        except Exception as e:
            print(f"数据库查询出错: {e}")
            return "default_token"  # 出错时返回默认token
        finally:
            if conn:
                conn.close()

def get_group_nickname():
        # 这里实现获取最新随机值的逻辑
        # 示例代码，需要根据实际情况修改
        try:
            conn = sqlite3.connect('random_number.db')
            cursor = conn.cursor()
            cursor.execute('SELECT nickname FROM group_nickname ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            if result:
                return str(result[0])  # 确保返回的是字符串类型
            else:
                return "default_token"  # 如果没有记录，返回一个默认token
        except Exception as e:
            print(f"数据库查询出错: {e}")
            return "default_token"  # 出错时返回默认token
        finally:
            if conn:
                conn.close()

def store_admin(sender):
    try:
        # 连接到数据库
        conn = sqlite3.connect('random_number.db')
        cursor = conn.cursor()

        # 查找最新一行的 id
        cursor.execute('SELECT MAX(id) FROM random_number')
        max_id = cursor.fetchone()[0]

        if max_id is not None:
            # 更新最新一行的 admin_name 列
            update_query = 'UPDATE random_number SET admin_name = ? WHERE id = ?'
            cursor.execute(update_query, (sender, max_id))
            conn.commit()
            print('数据更新成功')
        else:
            print('表中没有数据，无法更新')

    except sqlite3.Error as e:
        print(f'数据库错误: {e}')
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def get_admin():
    try:
        # 连接到数据库
        conn = sqlite3.connect('random_number.db')
        cursor = conn.cursor()

        # 从最新一行获取 admin_name 列的数据
        query = "SELECT admin_name FROM random_number ORDER BY rowid DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()

        # 关闭数据库连接
        conn.close()

        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

async def get_friend_list():
    friend_list = []
    # 创建线程池执行器
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        try:
            # 假设设置 15 秒的执行时间，可按需修改
            friend_infos = await asyncio.wait_for(loop.run_in_executor(pool, wx.GetAllFriends), timeout=45)           
            print("friend_infos:", friend_infos)
            '''
            new_friends = [friend['remark'] if friend['remark'] is not None else friend['nickname'] for friend in friend_infos]
            # 避免重复添加相同好友
            for friend in new_friends:
                if friend not in friend_list:
                    friend_list.append(friend)
            '''
        except asyncio.TimeoutError:
            print("wx.GetAllFriends 执行超时")
            
    #sreturn friend_list
    
'''
def get_friend_list():
    
    friend_list = []
    while True:
        friend_infos = wx.GetAllFriends()
        #time.sleep(15)   
        if not friend_infos:
            break        
        new_friends = [friend['remark'] if friend['remark'] is not None else friend['nickname'] for friend in friend_infos]
        # 避免重复添加相同好友
        for friend in new_friends:
            if friend not in friend_list:
                friend_list.append(friend)

        # 检查是否有新的好友

    friend_infos = wx.GetAllFriends()
    friend_list = [friend['remark'] if friend['remark'] is not None else friend['nickname'] for friend in
                   friend_infos]   
    return friend_list
'''

def run_boxed(func, timeout):
    '''
    result = [None]  # 用列表包装结果以便线程修改
    thread = threading.Thread(target=lambda: result.__setitem__(0, func()))
    thread.start()
    thread.join(timeout)  # 等待指定时间
    return result[0] if not thread.is_alive() else None
    #return result[0] if not thread.is_alive()
    #return result[0]
    '''

    result = [None]  # 用于存储所有输出结果的列表
    thread = threading.Thread(target=lambda: result.__setitem__(0, func()))
    thread.start()
    start_time = time.time()
    while thread.is_alive() and (time.time() - start_time) < timeout:
        if result[0]:  # 仅当 results 非空时打印
            print("Real-time results:", result[0])
        time.sleep(0.1)
    
    # 等待线程结束或超时
    thread.join(timeout)
    return result[0] if not thread.is_alive() else result[0]

async def get_postpic(sender):
    result = await sever_bot.get_real_plan_pic(sender)
    if result is None:
        print("未获取到有效数据")
        return
    # 从结果中提取所需信息
    holidayresult = result.get("holidayresult")
    filename = result.get("filename")
    file_base64 = result.get("file_content")
    print("filename:", filename, "holidayresult:", holidayresult)
    # 确保目标文件夹存在
    target_folder = "post_pic"
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    file_path = os.path.join(target_folder, filename)
    print("file_path:", file_path)
    try:
        # 解码 Base64 数据并保存文件
        file_content = base64.b64decode(file_base64)
        with open(file_path, "wb") as f:
            f.write(file_content)
        print("文件保存成功")
    except Exception as e:
        print(f"文件保存失败: {e}") 
    
    print('文件已保存到:', file_path) 
    
    '''
    with open(file_path, 'wb') as f:
        print("open filepath...")
        f.write(response.content)
    '''

    '''
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    '''
    wx.SendFiles(filepath=file_path, who=get_admin())
    wx.SendMsg(msg=holidayresult, who=get_admin())


running = False
main_loop = False


def get_main_loop(): 
    global main_loop
    return main_loop

def set_main_loop(value): 
    global main_loop
    main_loop = value

def get_running(): 
    global running
    return running

def set_running(value): 
    global running
    running = value

def get_token():
    conn = sqlite3.connect('random_number.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(value) FROM random_number WHERE value IS NOT NULL AND value != ""')
    if cursor.fetchone()[0] > 0:
        return

    # 若没有值，执行 sever_bot.get_token()
    token = None
    try:
        token = sever_bot.get_token()
    except ImportError:
        print('无法导入 sever_bot 模块')
    except Exception as e:
        print(f'调用 sever_bot.get_token() 时出错: {e}')

    cursor.execute('INSERT INTO random_number (value) VALUES (?)', (token,))

    cursor.execute('SELECT admin_name FROM random_number WHERE value = ?', (token,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute('INSERT INTO random_number (value) VALUES (?)', (token,))
    #第一次登录用户，存储管理员码 和 空用户名
    else:
        admin_name = result[0]
        cursor.execute('INSERT INTO random_number (admin_name, value) VALUES (?, ?)', (admin_name, token))
    #登录过用户，在数据库最新一行存储管理员码 和 用户名，代表当前登录用户状态
    conn.commit()
    conn.close()
    print("token:", token)
#增加一个运行参数，同时增加一个完成调用listenlist代码，当运行参数为真的时候，不进行重启，当运行参数和完成参数
#同时为假的时候，再进行重启
get_token()

def start_bot():
    ################################全局变量#########################################################

    ####验证存储的微信名######################

    token = get_random_number_token()

    # 创建并启动线程来显示遮罩层
    mask_thread = threading.Thread(target=show_mask)
    mask_thread.start()

    # 初始获取一次 friend_list
    set_running(True)
    '''
    friend_list = get_friend_list()
    '''

    '''
    async def get_friend():
        tempresult = await get_friend_list()
        return tempresult
    friend_list = asyncio.run(get_friend())
    '''
    #friend_infos = wx.GetAllFriends()


    friend_infos = run_boxed(wx.GetAllFriends, 20)
    time.sleep(22)


    start_time = time.time()
    timeout = 600  # 30秒超时
    
    # 轮询等待直到friends有值或超时
    
    while friend_infos is None:
        if time.time() - start_time > timeout:
            raise TimeoutError("等待好友列表超时")
        time.sleep(0.1)  # 短
    
    friend_list = [friend['remark'] if friend['remark'] is not None else friend['nickname'] for friend in friend_infos]
    #print("friends:", friend_infos)
    print("friends:", friend_list)
    '''
    if friends is not None:
        print("获取到好友列表:", friends)
    else:
        print("操作超时")
    '''
    
    
    #print("friend_infos:", friend_infos)


    #print(friend_list)

    '''
    group_list = [
        '🙈SDKs',
    ]
    '''

    group_list = get_group_names()
    print("group_list:", group_list)

    # 修改选中代码，合并 friend_list 和 pretype_list 到 listen_list
    listen_list = friend_list + group_list
    #listen_list = group_list
    print("listen_list", listen_list)

    # 增加微信窗口加载等待时
    # 定义时间间隔为 2 小时，单位：秒
    ##################===============##################
    interval = 2 * 60 * 60
    #interval = 25
    ##################=======================#########
    last_update_time = time.time()

    for i in listen_list:
        try:
            wx.AddListenChat(who=i, savepic=True)
        except (LookupError, TypeError) as e:
            print(f"为 {i} 添加监听失败，错误信息: {e}")

    wait = 1  # 设置1秒查看一次是否有新消息
    '''
    global main_loop
    main_loop = True
    '''

    set_main_loop(True)
    ########################################主程序####################################################
    while get_main_loop():
        print("监听中...")
        # 检查是否到了更新时间
        if time.time() - last_update_time >= interval:
            friend_list = get_friend_list()  
            listen_list = friend_list + group_list
            print("Updated listen_list", listen_list)
            last_update_time = time.time()

        msgs = wx.GetListenMessage()
        for chat in msgs:
    
            should_store_user = sever_bot.should_store_user()
            #is_in_setup_mode = True
            print("should_store_user:", should_store_user)

            who = chat.who              # 获取聊天窗口名（人或群名）
            one_msgs = msgs.get(chat) 
            # 获取消息内容
            # 回复收到
            should_skip_else = False
            for msg in one_msgs:
                msgtype = msg.type       # 获取消息类型
                content = msg.content
                sender = msg.sender
                from_whom = sender + " " + "in" + " " + who # 这里可以将msg.sender改为msg.sender_remark，获取备注名
                print(f'<{from_whom.center(10, "-")}>：{msg.content}')


                #random_number = db_utils.get_random_number_from_second_db()
                random_number = get_random_number()
                if content == random_number:
                # 第一次输入randomnumber会被储存，之后的会循环检查上一次的name，继续储存上一次的name；如果没有第一次被random储存的name，后边的name都不会被储存；
                    random_token = get_random_number_token()
                    store_admin(sender)
                    reply_content = "您好，管理员\n\n" + \
                            "请输入'设置'开启设置模式\n\n" + \
                            "\n\n" + \
                            "--------------------------\n\n" + \
                            "设置模式下，您可设置：\n\n" + \
                            "'店铺信息（必须设置）、菜单、订位、运营、学习等'\n\n" + \
                            "输入'退出管理员'退出管理员模式\n\n"

                    sever_bot.random_number_court(sender, random_token)

                    chat.SendMsg(reply_content)
                    should_skip_else = True
                    continue

                # 当msg.content中包含微信图片_ 时，提取 微信图片_ 和之后的部分，赋予filename
                

            # ===================================================
            # 处理消息逻辑（如果有）
            # 
            # 处理消息内容的逻辑每个人都不同，按自己想法写就好了，这里不写了
            # 
            # ===================================================
            
            # 确保 msgtype 和 content 已经被正确赋值
            if 'msgtype' not in locals() or 'content' not in locals():
                continue

            if msgtype == 'friend':
                if who in group_list:

                    is_in_holiday_mode = sever_bot.is_in_holiday_mode()
                    print("holiday_mode:", is_in_holiday_mode)

                    if is_in_holiday_mode:
                        
                        #这里是一个条件判断和响应器，如果不行，可以多拆
                        non_zero_columns = sever_bot.non_zero_columns()

                        ##################获取游戏类型代码############################
                        print("non_zero_columns:", non_zero_columns)
                        # 返回的 gameword....列名
                        # def check_game_response(non_zero_columns, content, nickname, send_msg, holiday_sys):
                        result_data = sever_bot.check_game_response(non_zero_columns, content, sender)
                        if result_data:
                            result, holidayresult, remind_info = result_data
                            
                            chat.SendMsg(result)
                            wx.SendMsg(msg=holidayresult, who=get_admin())
                            wx.SendMsg(msg=remind_info, who=get_admin())

                            print("Result:", result)
                            print("Holiday Result:", holidayresult)
                            print("Remind Info:", remind_info)
                            # if key_word in content:
                            # result = "恭喜" + nickname + "回答正确。获得" + "今天活动先到这里啦~再次感谢大家参与。再次参加活动，看通知哦"
                            # holiday_sys.set_holiday_mode(False, "holiday.db")
                            # latest_from_user_name = get_latest_from_user_name()
                            # print(latest_from_user_name)
                            # holidayresult = "今天活动获奖者：" + nickname

                    if not is_in_holiday_mode: 
                        group_nickname = get_group_nickname()                  
                        if f"@{group_nickname}" in content:
                            if not should_skip_else:
                                re_result, last_with_order = sever_bot.customer_agent(content, sender)
                                reply_content = re_result
                                if last_with_order is not None:
                                    wx.SendMsg(msg=last_with_order, who=get_admin())
                                chat.SendMsg(reply_content)

                            '''
                            usually_reply_content = sever_bot.usually_reply_content(sender, content)
                            chat.SendMsg(usually_reply_content) 
                            '''
    ##################################群保护###################################                
                    protectresult = sever_bot.protectresult(content)
                    protect_data = sever_bot.do_with_protection(protectresult, sender)
                    print("protect_data:", protect_data)                
                    if protect_data == "pass":
                        pass
                    elif isinstance(protect_data, list):
                        chat.SendMsg(protect_data[1])  # 发送元组第二个元素（字符串）
                        wx.SendMsg(msg=protect_data[0], who=get_admin())
                        print("protect_data 为字典")
                    elif isinstance(protect_data, str):
                        protect_remind_result = protect_data
                        chat.SendMsg(protect_data)
                        print("protect_data[0]:",protect_data[0])
                        print("protect_data 为字符串")
    #########################投诉模块#######################################
                    complaint_supervise = sever_bot.complaint_supervise(content)
                    complain_data = sever_bot.do_with_complain(complaint_supervise, content, sender)
                    print("complain_data:", complain_data)
                    if complain_data == "pass":
                        pass
                    elif isinstance(complain_data, list):
                        complaint_supervise_result, complaint_remind = complain_data
                        chat.SendMsg(complain_data[0])  # 发送元组第一个元素（字符串）
                        wx.SendMsg(msg=complain_data[1], who=get_admin())
                    else:
                        # 使用 continue 跳过当前循环
                        continue
    ####################核销模块##############
                elif "核销" in content:
                    clear_content = content.replace("核销", "").strip()
                    print("clear_content:", clear_content)
                    result = sever_bot.check_reward(clear_content)
                    should_skip_else = True
                    chat.SendMsg(result)
                                    
                elif should_store_user:
                    if sever_bot.check_sender_match(sender, token):
                    #设置命令操作
                        if content == '设置':                         # 使用 == 进行完全匹配
                            sever_bot.set_user_setup_mode()
                        elif content == '菜单':          
                            sever_bot.set_user_menu_mode()
                        elif content == '订位':
                            sever_bot.set_user_table_mode()
                        elif content == '运营':
                            sever_bot.set_user_op_mode()
                        elif content == '活动':
                            sever_bot.set_user_opholiday_mode()
                        elif content == '结束设置':  # 同样使用 == 进行完全匹配
                            sever_bot.stop_setup_mode()
                            reply_content = "已退出设置模式"
                            chat.SendMsg(reply_content)
                            should_skip_else = True
                            continue
                        elif content == '关闭运营':  # 同样使用 == 进行完全匹配
                            sever_bot.stop_op()
                        elif content == '开启运营':  # 同样使用 == 进行完全匹配
                            sever_bot.start_op()

                        elif content == '退出管理员': 
                            sever_bot.quit_admin() # 同样使用 == 进行完全匹配
                            sever_bot.stop_setup_mode()
                            reply_content = "已回到普通顾客模式"
                            chat.SendMsg(reply_content)
                            should_skip_else = True

                    #设置状态显示
                        is_in_setup_mode = sever_bot.get_user_setup_mode()
                        is_in_menu_mode = sever_bot.get_user_menu_mode()
                        is_in_table_mode = sever_bot.get_user_table_mode()
                        is_in_op_mode = sever_bot.get_user_op_mode()
                        is_in_opholiday_mode = sever_bot.get_user_opholiday_mode()

                        print("is_in_setup_mode:", is_in_setup_mode)
                        print("is_in_menu_mode:", is_in_menu_mode)
                        print("is_in_table_mode:", is_in_table_mode)
                        print("is_in_op_mode:", is_in_op_mode)
                        print("is_in_opholiday_mode:", is_in_opholiday_mode)

                    #设置查询字典       
                        response_dict = {
                            "设置": (
                                "已进入设置模式\n\n"
                                "直接输入：营业时间/店铺地址/店名（以上必须设置）/服务员人数/店主姓名/AI店员的工作时间等...\n\n"
                                "或：\n\n"
                                "输入'菜单' 进入菜单设置模式\n\n"
                                "输入'订位' 进入订位设置模式\n\n"
                                "输入'运营' 设定群、私信运营内容\n\n"
                                "作为人工智能，设置状态下您可以尝试文字教我任何顾客回复规则，更多功能待您发现...\n\n"
                                #"设置完成后，记得输入'结束设置'退出设置模式\n\n"
                                "----------------------------"
                                # "您也可以输入'帮忙'后,询问具体操作方式"  # 如果需要，可以取消注释
                            ),
                            "菜单": (
                                "请发送:\n\n" + \
                                "'新增'+'菜单内容'\n\n" + \
                                "或：\n\n" + \
                                "发送菜单图片自动识别录入\n\n" + \
                                "设置完成后，记得输入'结束设置'退出设置模式"
                            ),
                            "订位": (
                                "请发送每日可订位台数\n\n"
                                "设置完成后，记得输入'结束设置'退出设置模式"
                            ),
                            "运营": (
                                "1.发送10张以上菜品、店铺环境或任意图片,设定每日群内发送图片\n\n" + \
                                "2.发送图片+'生成文字',AI将编辑文字\n\n" + \
                                "3.生成文字后，发送'发顾客群',图片和文字将发在各个群内，每天限2次\n\n" + \
                                "4.生成文字后，发送'群发',图片和文字发给所有用户，每3天限1次\n\n" + \
                                "5.编辑文字+'文字发顾客群'/'文字群发',直接发送文字到群、私信\n\n" + \
                                "6.发送图片+您编辑的文字+'速发顾客群',图片和文字将发在各个群内，每天限2次\n\n" + \
                                "7.发送图片+您编辑的文字+'速群发',图片和文字发给所有用户，每3天限1次\n\n" + \
                                "8.发送'活动',查看或设置近期活动\n\n" + \
                                "（请将发送命令，包含在您编辑的文字中）" + \
                                "设置完成后，记得输入'结束设置'退出设置模式"
                            )
                        }

                        # 根据内容获取对应的结果，如果内容不在字典中，则执行else部分的逻辑
                        if content in response_dict:
                            reply_content = response_dict.get(content)
                            chat.SendMsg(reply_content)
                            break

                    #具体设置内容项
                        if is_in_setup_mode :
                            if content == "菜单":
                                reply_content = "请发送:\n\n" + \
                                        "'新增'+'菜单内容'\n\n" + \
                                        "或：\n\n" + \
                                        "发送菜单图片自动识别录入\n\n" + \
                                        "设置完成后，记得输入'结束设置'退出设置模式"

                            elif content == "订位":
                                reply_content = "请发送每日可订位台数(初始值为5)\n\n" + \
                                        "设置完成后，记得输入'结束设置'退出设置模式"

                            elif content == "运营":
                                reply_content = "请发送：\n\n" + \
                                        "1.（必要）直接发送10张以上菜品、店铺环境或任意图片,设定每日群内容图片\n\n" + \
                                        "2.发送图片+'生成文字'，AI将生成文本内容\n\n" + \
                                        "3.生成文字后，发送'发顾客群'，AI将同时把图片和文字发在各个群内，每天限2次\n\n" + \
                                        "4.生成文字后，发送'群发'，AI将同时把图片和文字私信发给所有用户，每3天限1次\n\n" + \
                                        "5.编辑文字+'文字发顾客群'/'文字群发',直接发送文字到群、私信\n\n" + \
                                        "6.发送图片+您编辑的文字+'速发顾客群',图片和文字将发在各个群内，每天限2次\n\n" + \
                                        "7.发送图片+您编辑的文字+'速群发',图片和文字发给所有用户，每3天限1次\n\n" + \
                                        "8.发送'活动',查看或设置近期活动\n\n" + \
                                        "（请将发送命令，包含在您编辑的文字中）\n\n" + \
                                        "设置完成后，记得输入'结束设置'退出设置模式"
                                
                                chat.SendMsg(reply_content)
                                should_skip_else = True

                            #####################管理员模式##################################
                            
                            else:      
                                reply_content = sever_bot.admin_chat_answer(sender, content) + "\n\n" + \
                                        "----------------------\n\n" + \
                                        "继续输入：营业时间/店铺地址/店名（以上必须设置）/服务员人数/店主姓名/AI店员的工作时间等...\n\n" + \
                                        "输入'菜单'进入菜单设置\n\n" + \
                                        "输入'订位'进入订位设置\n\n" + \
                                        "输入'运营'进入运营设置\n\n" + \
                                        "输入'活动'进入活动设置\n\n" + \
                                        "输入'结束设置'退出设置模式"
                                # db_utils.store_user_and_message(result, )
                                chat.SendMsg(reply_content)
                                print(reply_content)
                                                    
                        elif is_in_menu_mode:
                            if "微信图片_" in msg.content:
                                filepath = msg.content
                                match = re.search(r'微信图片_.*?\.jpg', filepath)
                                if match:
                                    filename = match.group()
                                print("filename:",filename) 
                                reply_content = sever_bot.menu_check(filename) 
                                chat.SendMsg(reply_content) 

                            elif "新增" in content:
                                content = content.replace("新增", "")
                                content = content.replace(":", "")
                                # result = chat_api.menu_chat_answer(content) + tails
                                priceresult = sever_bot.price_chat_answer(content)
                                menu_items = sever_bot.extract_fullmenu_items(priceresult)
                                sever_bot.insert_into_menu_db(menu_items)
                                reply_content = "设置菜单成功！请继续输入菜单，或输入'结束设置'，结束菜单设置"
                                chat.SendMsg(reply_content)

                            elif content == "查看菜单":
                                # 从menu.db读取全部内容
                                menu_content = sever_bot.fetch_menu_from_db()
                                reply_content = menu_content + "\n\n----------------------\n输入'删+准确菜名' 删除菜品\n\n输入'复制菜单'+ '文字菜单内容'，将完全复制您的菜单，并删除之前的菜单内容。建议先输入'查看菜单'获取当前菜单内容后再使用\n\n输入'查看菜单'查看全部菜单内容\n\n输入'结束设置'退出设置"
                                chat.SendMsg(reply_content)

                            elif content == "结束设置":
                                # 从menu.db读取全部内容，并附加"菜单设置结束"
                                menu_content = sever_bot.fetch_menu_from_db()
                                reply_content = menu_content + "\n\n菜单设置结束"
                                chat.SendMsg(reply_content)

                            elif "复制菜单" in content:
                                # 从menu.db读取全部内容，并附加"菜单设置结束"
                                content = content.replace("复制菜单", "")
                                content = content.replace(":", "")
                                sever_bot.delete_from_menu_db()
                                menu_items = sever_bot.extract_fullmenu_items(content)
                                sever_bot.insert_into_menu_db(menu_items)
                                reply_content = "设置菜单成功！请继续输入菜单，或输入'结束设置'，结束菜单设置"
                                chat.SendMsg(reply_content)

                            elif content == "订位":
                                reply_content = "请发送每日可定位台数(初始值为5)\n\n" + \
                                        "设置完成后，记得输入'结束设置'退出设置模式"
                                chat.SendMsg(reply_content)

                            elif content == "运营":
                                reply_content = "请发送：\n\n" + \
                                        "1.发送10张以上菜品、店铺环境或任意图片,设定每日群内容图片\n\n" + \
                                        "2.发送图片+'临时图片',AI将编辑文字，同时将图片和文字发在各个群内，每天限1次\n\n" + \
                                        "3.发送图片+'群发图片',AI将编辑文字，同时将图片和文字发给所有用户，每3天限1次\n\n" + \
                                        "4.发送'活动',查看近期活动\n\n" + \
                                        "设置完成后，记得输入'结束设置'退出设置模式"
                                chat.SendMsg(reply_content)

                            elif content.startswith("删"):
                                # 尝试从content中提取要删除的菜单项名称
                                # 这里假设"删"后面紧跟着要删除的名称，且名称中不包含空格
                                # 这是一个非常简单的解析，实际应用中可能需要更复杂的逻辑
                                name_to_delete = content.split("删", 1)[-1].strip()
                                print("name_to_delete:", name_to_delete)  # 打印提取的名称，用于调试
                                if name_to_delete:

                                    delete_success = sever_bot.delete_from_menu_db_by_similarity(name_to_delete)
                                    print("delete_success:", delete_success)
                                    #print("delete_success:", delete_success)
                                    if delete_success:
                                        print("delete")
                                        reply_content = sever_bot.fetch_menu_from_db()
                                        chat.SendMsg(reply_content)  # 如果删除了项，则获取新的菜单
                                    else:
                                        reply_content = "请输入 -删+准确菜名。"  # 如果没有删除任何项，则显示错误消息
                                        print("no menu to delate")
                                        chat.SendMsg(reply_content)
                                else:
                                    reply_content = "请输入 删+准确菜名。"  # 如果名称为空，也显示错误消息
                                    print("no menu name")
                                    chat.SendMsg(reply_content)

                                print(reply_content)

                            else:
                                filename = ""
                                reply_content = sever_bot.menu_chat_answer(content)
                                print(reply_content)
                                chat.SendMsg(reply_content)

                            sever_bot.update_menu_items(reply_content)

                            '''

                            elif content not in response_dict:
                                reply_content = chat_api.help_agent(content)
                                # result = chat_api.user_chat_answer(content)
                                print(reply_content)
                                print(content)

                            '''

                        elif is_in_table_mode:
                            if content == "结束设置":
                                # 从menu.db读取全部内容，并附加"菜单设置结束"
                                reply_content = "订位设置结束"
                                chat.SendMsg(reply_content)
                            else:
                                order_table_result = sever_bot.order_table_answer(content)
                                sever_bot.insert_order_table(order_table_result)
                                reply_content = order_table_result + "\n\n----------------------\n输入'结束设置'退出设置"
                                print(reply_content)
                                chat.SendMsg(reply_content)

                        elif is_in_op_mode:                           
                            if content == "生成文字" or content == "重新生成":                           
                                file_store = f'static{token}'
                                latest_image = sever_bot.get_latest_image_in_directory(file_store)
                                print(latest_image)
                                async def get_pic_describ(latest_image):
                                    tempresult = await sever_bot.result_pic(latest_image)
                                    return tempresult
                                tempresult = asyncio.run(get_pic_describ(latest_image))
                                print("tempresult:",tempresult)
                                midlecontent = tempresult['description']
                                print(midlecontent)
                                teal = "\n\n---------------------\n" + \
                                    "回复'发顾客群'或'群发'直接发送生成的文字和图片\n\n" + \
                                    "或者 发送您修改的内容+'速发顾客群'或'速群发'发送图片和内容（请将发送命令，包含在您编辑的文字中）\n\n" + \
                                    "发送'重新生成'重新生成文字\n\n" + \
                                    "发送'结束设置'退出设置"
                                airesult = sever_bot.pic_chat_answer(midlecontent)
                                reply_content = airesult + teal
                                chat.SendMsg(reply_content)
                                sever_bot.store_qunfa(airesult)
                            elif "速发顾客群" in content:
                                if sever_bot.can_send_group_message():
                                    real_content = content.replace("速发顾客群", "").strip()
                                    print(f"从 content 中提取的消息内容: {real_content}")   
                                    msg = real_content
                                    file_store = f'static{token}'
                                    latest_image = sever_bot.get_latest_image_in_directory(file_store)
                                    print(latest_image)
                                    match = re.search(r'微信图片_.*?\.jpg', latest_image)
                                    if match:
                                        filename = match.group()
                                    local_path = f"wxauto文件\{filename}"
                                    group_list = [
                                        '🙈SDKs',
                                    ]
                                    for who in group_list:
                                        try:
                                            wx.SendMsg(msg=msg, who=who)
                                            wx.SendFiles(filepath=local_path, who=who)
                                            print(f"消息已发送至 {who}")
                                        except Exception as e:
                                            print(f"向 {who} 发送消息时出错: {e}")                                                                                                
                                    reply_content = "消息发送中\n\n" + \
                                            "发送'结束设置'退出设置"
                                    chat.SendMsg(reply_content)

                                else:
                                    reply_content = "文字发顾客群功能每天只能使用 2 次，请稍后再试。\n\n" + \
                                            "发送'结束设置'退出设置"                                    
                                    chat.SendMsg(reply_content)

                            elif "速群发" in content:
                                if sever_bot.can_send_private_word_message():
                                    real_content = content.replace("速发顾客群", "").strip()
                                    print(f"从 content 中提取的消息内容: {real_content}")
                                    file_store = f'static{token}'
                                    latest_image = sever_bot.get_latest_image_in_directory(file_store)
                                    print(latest_image)
                                    match = re.search(r'微信图片_.*?\.jpg', latest_image)
                                    if match:
                                        filename = match.group()
                                    local_path = f"wxauto文件\{filename}"
                                    msg = real_content
                                    friend_list = get_friend_list()
                                    print(friend_list)
                                    for who in friend_list:
                                        try:
                                            wx.SendMsg(msg=msg, who=who)
                                            wx.SendFiles(filepath=local_path, who=who)
                                            print(f"消息已发送至 {who}")
                                        except Exception as e:
                                            print(f"向 {who} 发送消息时出错: {e}")
                                    reply_content = "消息发送中\n\n" + \
                                            "发送'结束设置'退出设置"
                                    chat.SendMsg(reply_content)                            
                                else:
                                    reply_content = "群发功能每 3 天只能使用 1 次，请稍后再试。\n\n" + \
                                            "发送'结束设置'退出设置"
                                    chat.SendMsg(reply_content)

                            elif "文字群发" in content:
                                if sever_bot.can_send_private_word_message(): 
                                    real_content = content.replace("文字群发", "").strip()
                                    print(f"从 content 中提取的消息内容: {real_content}")
                                    msg = real_content
                                    friend_list = get_friend_list()
                                    print(friend_list)
                                    for who in friend_list:
                                        try:
                                            wx.SendMsg(msg=msg, who=who)
                                            print(f"消息已发送至 {who}")
                                        except Exception as e:
                                            print(f"向 {who} 发送消息时出错: {e}")
                                    reply_content = "消息发送中\n\n" + \
                                            "发送'结束设置'退出设置"
                                    chat.SendMsg(reply_content)
                                else:
                                    reply_content = "文字群发功能每 3 天只能使用 1 次，请稍后再试。\n\n" + \
                                            "发送'结束设置'退出设置"
                                    chat.SendMsg(reply_content)

                            elif "文字发顾客群" in content:
                                if sever_bot.can_send_group_message():
                                    real_content = content.replace("文字发顾客群", "").strip()
                                    print(f"从 content 中提取的消息内容: {real_content}")
                                    msg = real_content
                                    group_list = [
                                        '🙈SDKs',   
                                    ]

                                    for who in group_list:
                                        try:
                                            wx.SendMsg(msg=msg, who=who)
                                            print(f"消息已发送至 {who}")
                                        except Exception as e:
                                            print(f"向 {who} 发送消息时出错: {e}")
                                                                                                        
                                    reply_content = "消息发送中\n\n" + \
                                            "发送'结束设置'退出设置"
                                    chat.SendMsg(reply_content)
                                else:
                                    reply_content = "文字发顾客群功能每天只能使用 2 次，请稍后再试。\n\n" + \
                                            "发送'结束设置'退出设置"
                                        
                                    chat.SendMsg(reply_content)

                            elif content == "发顾客群":
                                if sever_bot.can_send_group_message():
                                    qunfa_message = sever_bot.get_qunfa_message()
                                    file_store = f'static{token}'
                                    latest_image = sever_bot.get_latest_image_in_directory(file_store)
                                    match = re.search(r'微信图片_.*?\.jpg', latest_image)
                                    if match:
                                        filename = match.group()
                                    local_path = f"wxauto文件\{filename}"
                                    msg = qunfa_message
                                    group_list = [
                                        '🙈SDKs',   
                                    ]

                                    for who in group_list:
                                        try:
                                            wx.SendMsg(msg=msg, who=who)
                                            wx.SendFiles(filepath=local_path, who=who)
                                            print(f"消息已发送至 {who}")
                                        except Exception as e:
                                            print(f"向 {who} 发送消息时出错: {e}")                                                                                               
                                    reply_content = "消息发送中\n\n" + \
                                            "发送'结束设置'退出设置"
                                    chat.SendMsg(reply_content)
                                else:
                                    reply_content = "发顾客群功能每天只能使用 2 次，请稍后再试。\n\n" + \
                                            "发送'结束设置'退出设置"

                            elif content == "群发":
                                if sever_bot.can_send_private_word_message():
                                    qunfa_message = sever_bot.get_qunfa_message()
                                    file_store = f'static{token}'
                                    latest_image = sever_bot.get_latest_image_in_directory(file_store)
                                    match = re.search(r'微信图片_.*?\.jpg', latest_image)
                                    if match:
                                        filename = match.group()
                                    local_path = f"wxauto文件\{filename}"
                                    msg = qunfa_message
                                    friend_list = get_friend_list()
                                    print(friend_list)

                                    for who in friend_list:
                                        try:
                                            wx.SendMsg(msg=msg, who=who)
                                            wx.SendFiles(filepath=local_path, who=who)
                                            print(f"消息已发送至 {who}")
                                        except Exception as e:
                                            print(f"向 {who} 发送消息时出错: {e}")
                                    reply_content = "消息发送中\n\n" + \
                                            "发送'结束设置'退出设置"
                                    chat.SendMsg(reply_content)
                                else:
                                    reply_content = "群发功能每 3 天只能使用 1 次，请稍后再试。\n\n" + \
                                            "发送'结束设置'退出设置"

                        elif is_in_opholiday_mode:
                            if content == "重新生成":
                                try:
                                    # 尝试获取当前事件循环
                                    loop = asyncio.get_running_loop()
                                    # 如果在异步上下文中，使用 create_task
                                    task = loop.create_task(get_postpic(sender))
                                    loop.run_until_complete(task)
                                except RuntimeError:
                                    # 如果不在异步上下文中，使用 asyncio.run
                                    asyncio.run(get_postpic(sender))                                            
                                if sever_bot.can_regenerate():
                                    try:
                                    # 尝试获取当前事件循环
                                        loop = asyncio.get_running_loop()
                                        # 如果在异步上下文中，使用 create_task
                                        task = loop.create_task(get_postpic(sender))
                                        loop.run_until_complete(task)
                                    except RuntimeError:
                                        # 如果不在异步上下文中，使用 asyncio.run
                                        asyncio.run(get_postpic(sender))    
                                    #sever_bot.get_real_plan_pic(sender)
                                    
                                else:
                                    reply_content = "海报重新生成功能每天只能使用 2 次，请稍后再试。"
                                    chat.SendMsg(reply_content)

                            elif content == "生成海报":
                                ################测试代码################
                                '''
                                try:
                                    # 尝试获取当前事件循环
                                    loop = asyncio.get_running_loop()
                                    # 如果在异步上下文中，使用 create_task
                                    task = loop.create_task(get_postpic(sender))
                                    loop.run_until_complete(task)
                                except RuntimeError:
                                    # 如果不在异步上下文中，使用 asyncio.run
                                    asyncio.run(get_postpic(sender))
                                '''

                                if sever_bot.can_regenerate():
                                    try:
                                        loop = asyncio.get_running_loop()
                                        # 如果在异步上下文中，使用 create_task
                                        task = loop.create_task(get_postpic(sender))
                                        loop.run_until_complete(task)
                                    except RuntimeError:
                                        # 如果不在异步上下文中，使用 asyncio.run
                                        asyncio.run(get_postpic(sender))                                
                                else:
                                    reply_content = "海报生成功能每天只能使用 2 次，请稍后再试。"
                                    chat.SendMsg(reply_content)

                            elif "修改优惠" in content:
                                new_content = content.replace("修改优惠", "").strip()
                                db_utils.insert_holiday_reward(new_content)
                                reply_content = "修改成功" + "\n" + "--------------------" + \
                                        "\n\n" + "回复'修改时间'+ 开始日期、结束日期,修改相关内容（命令请包含在编辑的文字中）" + \
                                        "\n\n" + "回复'复制我的方案' + \n活动形式: 到店活动/猜字谜/猜数字/猜成语/趣味游戏抢答\n活动详情：...(请按照格式发送内容)" + \
                                        "\n\n" + "若设置结束，请回复方案'1/2/3'，选择活动内容方案，生成活动海报" + "\n\n"
                                chat.SendMsg(reply_content)

                            elif "修改时间" in content:
                                new_content = content.replace("修改时间", "").strip()
                                insert_time = sever_bot.chat_time(new_content)
                                time_result = sever_bot.insert_holiday_time(insert_time)
                                reply_content = time_result + "\n" + "--------------------" + \
                                        "\n\n" + "回复'修改优惠' + 优惠内容,修改相关内容（命令请包含在编辑的文字中）" + \
                                        "\n\n" + "回复'复制我的方案' + \n活动形式: 到店活动/猜字谜/猜数字/猜成语/趣味游戏抢答\n活动详情：...(请按照格式发送内容)" + \
                                        "\n\n" + "若设置结束，请回复方案'1/2/3'，选择活动内容方案，生成活动海报" + "\n\n"
                                chat.SendMsg(reply_content)

                            elif "重新生成方案" in content:
                                holiday_op_result = sever_bot.send_weekly_holidays()
                                wx.SendMsg(msg=holiday_op_result, who=get_admin())

                            elif "复制我的方案" in content:
                                new_content = content.replace("复制我的方案", "").strip()
                                sever_bot.copy_my_content(new_content)
                                reply_content = "修改成功" + "\n" + "--------------------" + \
                                        "\n\n" + "回复'修改时间'+ 开始日期、结束日期,'修改优惠' + 优惠内容,修改相关内容（命令请包含在编辑的文字中）" + \
                                        "\n\n" + "若设置结束，请回复'生成海报'，生成活动海报" + "\n\n"
                                chat.SendMsg(reply_content)

                            # 检查content是否等于"确认方案"
                            elif content == "确认方案":
                                sever_bot.set_holiday_realtime()
                                ###############从时间记录，录入实际执行时间#############
                                print("from_user_name_ori:", sender)
                                # db_utils.get_real_plan_pic(from_user_name)
                                reply_content = "方案已确认"
                                chat.SendMsg(reply_content)
                                #db_utils.set_user_setup_mode(from_user_name, False, )
                                sever_bot.stop_setup_mode()
                            # else:
                            # result = chat_api.table_chat_answer(content)
                            # print(result)
                            else:
                                arabic_numbers_pattern = r'[1-9]\d*'  # 匹配一个或多个阿拉伯数字（不包括0开头的数字，但0本身可以单独存在）
                                # 注意：如果你想要匹配0开头的数字（如001），可以使用 r'0*\d+'
                                chinese_numbers_pattern = r'[一二三四五六七八九十百千万亿]+'  # 匹配一个或多个连续的汉字数字
                                # 编译正则表达式模式
                                arabic_numbers_regex = re.compile(arabic_numbers_pattern)
                                chinese_numbers_regex = re.compile(chinese_numbers_pattern)
                                # 检查content是否包含阿拉伯数字或汉字数字
                                contains_arabic_number = bool(arabic_numbers_regex.search(content))
                                contains_chinese_number = bool(chinese_numbers_regex.search(content))

                                if contains_arabic_number or contains_chinese_number:
                                    pickresult = sever_bot.holiday_set(content, sender)
                                    print("pickresult:", pickresult)
                                    activity_content = pickresult[0][1] 
                                    sever_bot.update_game_table(activity_content)

                                    #db_utils.get_real_plan_pic(sender)
                                    
                                    '''
                                    if db_utils.can_generate():
                                        db_utils.get_real_plan_pic(sender)
                                    else:
                                        reply_content = "海报生成功能每天只能使用 2 次，请稍后再试。"
                                    '''
                        
                        else:
                            if not should_skip_else:
                                # 原 else 分支代码
                                reply_content = sever_bot.help_agent(content)
                                # result = chat_api.user_chat_answer(content)
                                print(reply_content)
                                chat.SendMsg(reply_content)

                        #if not should_skip_else:
                            #chat.SendMsg(reply_content)

    ############################这是setmode内，判断不是管理员时的一般回复############                        
                    elif not sever_bot.check_sender_match(sender, token):
                        if not should_skip_else:
                            re_result, last_with_order = sever_bot.customer_agent(content, sender)
                            reply_content = re_result
                            if last_with_order is not None:
                                wx.SendMsg(msg=last_with_order, who=get_admin())
                            chat.SendMsg(reply_content)

    ####################下边是通用一般状态下的普通顾客回复##################
                else:
                    if not should_skip_else:
                        re_result, last_with_order = sever_bot.customer_agent(content, sender)
                        reply_content = re_result
                        if last_with_order is not None:
                            wx.SendMsg(msg=last_with_order, who=get_admin())
                        chat.SendMsg(reply_content)
        
        time.sleep(wait)

        '''
        if should_stop():
                running = False
                break
        '''
def stop_bot():
    set_main_loop(False)
    set_running(False)


def is_running():
    result = get_main_loop()
    print("main_loop:", result)
    '''
    if not main_loop:
        main_loop = False
    '''
    return result


if __name__ == "__main__":
    start_bot()




