from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Error
import json
import requests
import time
from urllib.parse import urlparse
import os
import threading
import schedule
from datetime import datetime
import re
from wxauto import WeChat
from contextvars import ContextVar
from context_vars import token_var
from sever_bot import sever_bot

wx = WeChat()

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

def send_weekly_holidays():
    holiday_op_result = sever_bot.send_weekly_holidays()
    wx.SendMsg(msg=holiday_op_result, who=get_admin())
#send_weekly_holidays()

def schedule_weekly_holidays():
    print("开始调度每周节假日任务")
    schedule.every().friday.at("14:30").do(send_weekly_holidays)
    
    # 添加每周五 17:30 执行 sever_bot.stop_setup_mode() 的任务
    schedule.every().friday.at("17:30").do(sever_bot.stop_setup_mode)
    
    # 移除原有的阻塞逻辑
    
# 在独立线程中运行调度任务
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 启动调度线程
if __name__ == "__main__":
    schedule_weekly_holidays()
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
