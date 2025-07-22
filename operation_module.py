"""
运营Agent计时器,每日早9:30左右,下午 14:30左右,随机选择时间进行
"""
import time
import schedule
import multiprocessing
import json
from wxauto import WeChat
from sever_bot import sever_bot
import os # 确保该模块存在且包含所需函数
import sqlite3
 
wx = WeChat()

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

def get_random_number_token():
        # 这里实现获取最新随机值的逻辑
        # 示例代码，需要根据实际情况修改
        conn = None 
        try:
            db_path = os.path.abspath('random_number.db')
            conn = sqlite3.connect(db_path)
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

def setup_schedule():
    #group_list = ['12136']  # 确认群名称存在
    group_list = get_group_names()

    # 微博热搜任务
    newstime = "09:30"
    @schedule.repeat(schedule.every().day.at(newstime))
    def news_job():
        try:
            news_content = sever_bot.news_task()
            print("news_content:", news_content)  # 打印 news_content 的值
            
            for who in group_list:
                try:
                    wx.SendMsg(msg=news_content, who=who)
                    print(f"消息已发送至 {who}")
                except Exception as e:
                    print(f"向 {who} 发送消息时出错: {e}")
        except Exception as e:
            print(f"微博热搜任务失败: {str(e)}")
 
    pic_holiday_time = "14:30"
    # 随机图片任务
    @schedule.repeat(schedule.every().day.at(pic_holiday_time))
    def pic_job():
        try:
            token = get_random_number_token()
            result = sever_bot.conditional_pic_task() 
            print("received_result:", result)  # 打印 result 的值
            if isinstance(result, list) and len(result) == 3:
                task_type, file_name, message = result

                if task_type == 'pic_task':
                    # 对应之前的 picresult, new_image = result
                    print("received_pic_result:", message)
                    print("received_image_path:", file_name)
                    
                    base_dir = f'./static{token}'
                    #这一步是替换掉static
                    filepath = os.path.relpath(file_name, base_dir)
                    pic_path = f'wxauto文件/{filepath}'
                    
                    for who in group_list:
                        try:
                            wx.SendMsg(msg=message, who=who)
                            wx.SendFiles(filepath=pic_path, who=who)
                            print(f"消息已发送至 {who}")
                        except Exception as e:
                            print(f"向 {who} 发送消息时出错: {e}")
                elif task_type == 'holiday_task':
                    # 对应之前的 pic_name, post_quesiton = result
                    print("received_pic_name:", file_name)
                    print("received_post_quesiton:", message)
                    pic_path = os.path.join('post_pic', file_name)
                    for who in group_list:
                        try:
                            wx.SendMsg(msg=message, who=who)
                            wx.SendFiles(filepath=pic_path, who=who)
                            print(f"消息已发送至 {who}")
                        except Exception as e:
                            print(f"向 {who} 发送消息时出错: {e}")

        except Exception as e:
            print(f"执行任务时出错: {e}")
 
    print("已调度任务:")
    print(f"- 微博热搜: 每天:", newstime)
    print(f"- 随机图片: 每天:", pic_holiday_time)
 
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
 
if __name__ == "__main__":
    # 单进程版本（推荐先测试）
    setup_schedule()
    run_scheduler()
 
    # 多进程版本（需要解决调度器同步问题）
    # if __name__ == '__main__':
    #     processes = []
    #     for _ in range(multiprocessing.cpu_count()):
    #         p = multiprocessing.Process(target=run_scheduler)
    #         p.start()
    #         processes.append(p)
    #     for p in processes:
    #         p.join()