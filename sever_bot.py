import requests
import sqlite3
import time
import aiohttp
import urllib3
from requests.exceptions import ConnectionError
 
class ChatAPIClient:
    def __init__(self, base_url="https://service.hotblaz.com/api"):
        self.base_url = base_url
        self.token = self.get_random_number_token()  # 获取初始token
 
    def get_random_number_token(self):
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
 
    def fetch_latest_storename(self):
        url = f"{self.base_url}/fetch_latest_storename?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def get_access_token(self):
        url = f"{self.base_url}/get_access_token?token={self.token}"
        response = requests.post(url)
        data = response.json()
        # 假设返回的数据中包含新的token
        self.token = data.get('token', self.token)  # 更新token
        return data
 
    def get_latest_image_in_directory(self, directory):
        url = f"{self.base_url}/get_latest_image_in_directory?token={self.token}"
        response = requests.post(url, json={"directory": directory})
        return response.json()
 
    def string_similarity(self, str1, str2):
        url = f"{self.base_url}/string_similarity?token={self.token}"
        response = requests.post(url, json={"str1": str1, "str2": str2})
        return response.json()
 
    def extract_fullmenu_items(self, menu_text):
        url = f"{self.base_url}/extract_fullmenu_items?token={self.token}"
        response = requests.post(url, json={"menu_text": menu_text})
        return response.json()
 
    def extract_menu_items(self, menu_text):
        url = f"{self.base_url}/extract_menu_items?token={self.token}"
        response = requests.post(url, json={"menu_text": menu_text})
        return response.json()
 
    def char_similarity(self, key_word, content):
        url = f"{self.base_url}/char_similarity?token={self.token}"
        response = requests.post(url, json={"key_word": key_word, "content": content})
        return response.json()
 
    def should_store_user(self):
        url = f"{self.base_url}/should_store_user?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def random_number_court(self, sender, random_token):
        url = f"{self.base_url}/random_number_court?token={self.token}"
        response = requests.post(url, json={"sender": sender, "content": random_token})
        return response.json()
 
    def is_in_holiday_mode(self):
        url = f"{self.base_url}/is_in_holiday_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def non_zero_columns(self):
        url = f"{self.base_url}/non_zero_columns?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def check_game_response(self, non_zero_columns, content, sender):
        url = f"{self.base_url}/check_game_response?token={self.token}"
        response = requests.post(url, json={"non_zero_columns": non_zero_columns, "content": content, "sender": sender})
        return response.json()
 
    def usually_reply_content(self, sender, content):
        url = f"{self.base_url}/usually_reply_content?token={self.token}"
        response = requests.post(url, json={"sender": sender, "content": content})
        return response.json()
 
    def protectresult(self, content):
        url = f"{self.base_url}/protectresult?token={self.token}"
        response = requests.post(url, json={"content": content})
        return response.json()
 
    def complaint_supervise(self, content):
        url = f"{self.base_url}/complaint_supervise?token={self.token}"
        response = requests.post(url, json={"content": content})
        return response.json()
 
    def do_with_complain(self, complaint_supervise, content, sender):
        url = f"{self.base_url}/do_with_complain?token={self.token}"
        response = requests.post(url, json={"complaint_supervise": complaint_supervise, "content":content, "sender": sender})
        return response.json()
 
    def do_with_protection(self, protectresult, sender):
        url = f"{self.base_url}/do_with_protection?token={self.token}"
        response = requests.post(url, json={"protectresult": protectresult, "sender": sender})
        return response.json()
 
    def check_reward(self, clear_content):
        url = f"{self.base_url}/check_reward?token={self.token}"
        response = requests.post(url, json={"clear_content": clear_content})
        return response.json()
 
    def check_sender_match(self, sender, token):
        url = f"{self.base_url}/check_sender_match?token={self.token}"
        response = requests.post(url, json={"sender": sender, "token":token})
        return response.json()
 
    def set_user_setup_mode(self):
        url = f"{self.base_url}/set_user_setup_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def set_user_menu_mode(self):
        url = f"{self.base_url}/set_user_menu_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def set_user_table_mode(self):
        url = f"{self.base_url}/set_user_table_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def set_user_op_mode(self):
        url = f"{self.base_url}/set_user_op_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def set_user_opholiday_mode(self):
        url = f"{self.base_url}/set_user_opholiday_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def stop_setup_mode(self):
        url = f"{self.base_url}/stop_setup_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def stop_op(self):
        url = f"{self.base_url}/stop_op?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def start_op(self):
        url = f"{self.base_url}/start_op?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def quit_admin(self):
        url = f"{self.base_url}/quit_admin?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def get_user_setup_mode(self):
        url = f"{self.base_url}/get_user_setup_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def get_user_menu_mode(self):
        url = f"{self.base_url}/get_user_menu_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def get_user_table_mode(self):
        url = f"{self.base_url}/get_user_table_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def get_user_op_mode(self):
        url = f"{self.base_url}/get_user_op_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def get_user_opholiday_mode(self):
        url = f"{self.base_url}/get_user_opholiday_mode?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def menu_check(self, filename):
        url = f"{self.base_url}/menu_check?token={self.token}"
        response = requests.post(url, json={"filename": filename})
        return response.json()
 
    def admin_chat_answer(self, sender, content):
        url = f"{self.base_url}/admin_chat_answer?token={self.token}"
        response = requests.post(url, json={"sender": sender, "content": content})
        return response.json()
 
    def price_chat_answer(self, content):
        url = f"{self.base_url}/price_chat_answer?token={self.token}"
        response = requests.post(url, json={"content": content})
        return response.json()
 
    def insert_into_menu_db(self, menu_items):
        url = f"{self.base_url}/insert_into_menu_db?token={self.token}"
        response = requests.post(url, json={"menu_items": menu_items})
        return response.json()
 
    def fetch_menu_from_db(self):
        url = f"{self.base_url}/fetch_menu_from_db?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def delete_from_menu_db_by_similarity(self, name_to_delete):
        url = f"{self.base_url}/delete_from_menu_db_by_similarity?token={self.token}"
        response = requests.post(url, json={"name_to_delete": name_to_delete})
        return response.json()
 
    def menu_chat_answer(self, content):
        url = f"{self.base_url}/menu_chat_answer?token={self.token}"
        response = requests.post(url, json={"content": content})
        return response.json()
 
    def update_menu_items(self, reply_content):
        url = f"{self.base_url}/update_menu_items?token={self.token}"
        response = requests.post(url, json={"reply_content": reply_content})
        return response.json()
 
    def order_table_answer(self, content):
        url = f"{self.base_url}/order_table_answer?token={self.token}"
        response = requests.post(url, json={"content": content})
        return response.json()
 
    def insert_order_table(self, order_table_result):
        url = f"{self.base_url}/insert_order_table?token={self.token}"
        response = requests.post(url, json={"order_table_result": order_table_result})
        return response.json()
 
    async def result_pic(self, corrected_path):
        url = f"{self.base_url}/result_pic?token={self.token}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"corrected_path": corrected_path}, timeout=aiohttp.ClientTimeout(total=630)) as response:
                try:
                    return await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    # 处理非 JSON 响应
                    text = await response.text()
                    print(f"非 JSON 响应: {text}")
                    return None

        '''
        max_retries = 3  # 最大重试次数
        retries = 0
        while retries < max_retries:
            try:
                response = requests.post(url, json={"corrected_path": corrected_path}, timeout=(30, 300))
                return response.json()
            except (ConnectionResetError, urllib3.exceptions.ProtocolError, ConnectionError) as e:
                print(f"网络连接错误: {e}，正在重试 ({retries + 1}/{max_retries})...")
                retries += 1
                time.sleep(2)  # 等待 2 秒后重试
        print("达到最大重试次数，无法完成请求。")
        return {}
        '''
        '''
        url = f"{self.base_url}/get_real_plan_pic?token={self.token}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"sender": sender}, timeout=aiohttp.ClientTimeout(total=630)) as response:
                try:
                    return await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    # 处理非 JSON 响应
                    text = await response.text()
                    print(f"非 JSON 响应: {text}")
                    return None
        '''

        '''
        response = requests.post(url, json={"corrected_path": corrected_path}, timeout=(30, 300))
        return response.json()
        '''
 
    def pic_chat_answer(self, midlecontent):
        url = f"{self.base_url}/pic_chat_answer?token={self.token}"
        response = requests.post(url, json={"midlecontent": midlecontent})
        return response.json()
 
    def can_send_private_message(self):
        url = f"{self.base_url}/can_send_private_message?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def can_send_private_word_message(self):
        url = f"{self.base_url}/can_send_private_word_message?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def get_qunfa_message(self):
        url = f"{self.base_url}/get_qunfa_message?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    async def get_real_plan_pic(self, sender):
        '''
        url = f"{self.base_url}/get_real_plan_pic?token={self.token}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"sender": sender}, timeout=aiohttp.ClientTimeout(total=630)) as response:
                return await response.json()
        '''
        url = f"{self.base_url}/get_real_plan_pic?token={self.token}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"sender": sender}, timeout=aiohttp.ClientTimeout(total=630)) as response:
                try:
                    return await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    # 处理非 JSON 响应
                    text = await response.text()
                    print(f"非 JSON 响应: {text}")
                    return None

 
    def can_regenerate(self):
        url = f"{self.base_url}/can_regenerate?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def chat_time(self, new_content):
        url = f"{self.base_url}/chat_time?token={self.token}"
        response = requests.post(url, json={"new_content": new_content})
        return response.json()
 
    def insert_holiday_time(self, insert_time):
        url = f"{self.base_url}/insert_holiday_time?token={self.token}"
        response = requests.post(url, json={"insert_time": insert_time})
        return response.json()

    '''
    def send_weekly_holidays(self):
        url = f"{self.base_url}/send_weekly_holidays?token={self.token}"
        response = requests.post(url)
        return response.json()
    '''
 
    def update_game_table(self, pickresult):
        url = f"{self.base_url}/update_game_table?token={self.token}"
        response = requests.post(url, json={"pickresult": pickresult})
        return response.json()
 
    def copy_my_content(self, new_content):
        url = f"{self.base_url}/copy_my_content?token={self.token}"
        response = requests.post(url, json={"new_content": new_content})
        return response.json()
 
    def set_holiday_realtime(self):
        url = f"{self.base_url}/set_holiday_realtime?token={self.token}"
        response = requests.post(url)
        return response.json()
 
    def holiday_set(self, content, sender):
        url = f"{self.base_url}/holiday_set?token={self.token}"
        response = requests.post(url, json={"content": content, "sender": sender})
        return response.json()
 
    def help_agent(self, content):
        url = f"{self.base_url}/help_agent?token={self.token}"
        response = requests.post(url, json={"content": content})
        return response.json()
 
    def customer_agent(self, content, sender):
        try:
            url = f"{self.base_url}/customer_agent?token={self.token}"
            response = requests.post(url, json={"content": content, "sender": sender})
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                print(f'服务器返回的内容不是有效的JSON格式: {response.text}')
                return None
        except requests.exceptions.RequestException as e:
            print(f'请求发生错误: {e}')
            return None

    def news_task(self):
        url = f"{self.base_url}/news_task?token={self.token}"
        response = requests.post(url, timeout=600)
        return response.json()

    def conditional_pic_task(self):
        url = f"{self.base_url}/conditional_pic_task?token={self.token}"
        response = requests.post(url, timeout=600)
        return response.json()
    
        '''
        # 第一步：获取任务状态
        response = requests.post(url, timeout=(10, 30))
        if response.status_code != 202:  # 202 Accepted表示任务已接收
            return "任务创建失败", None
        
        task_id = response.headers.get("X-Task-ID")
        
        # 第二步：轮询任务结果
        poll_url = f"{self.base_url}/api/task_result/{task_id}"
        for _ in range(30):  # 最多轮询30次（建议配置化）
            poll_resp = requests.get(poll_url, timeout=(10, 30))
            if poll_resp.status_code == 200:
                data = poll_resp.json()
                if data["status"] == "completed":
                    return data["result"]["picresult"], data["result"]["full_url"]
                elif data["status"] == "failed":
                    raise Exception(f"任务失败: {data['error']}")
            time.sleep(10)  # 轮询间隔
        
        raise TimeoutError("任务执行超时")
        '''
    def send_weekly_holidays(self):
        url = f"{self.base_url}/send_weekly_holidays?token={self.token}"
        response = requests.post(url, timeout=600)
        return response.json()

    def delete_from_menu_db(self):
        url = f"{self.base_url}/delete_from_menu_db?token={self.token}"
        response = requests.post(url)
        return response.json()

    def store_qunfa(self, airesult):
        url = f"{self.base_url}/store_qunfa?token={self.token}"
        response = requests.post(url, json={"airesult": airesult})
        return response.json()

    def can_send_group_message():
        url = f"{self.base_url}/can_send_group_message?token={self.token}"
        response = requests.post(url)
        return response.json()

    def get_token(self):
        url = f"{self.base_url}/regis_token"
        response = requests.post(url)
        return response.json()


# 初始化客户端
sever_bot = ChatAPIClient()