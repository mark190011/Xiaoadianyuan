import sqlite3
import os
 
def set_admincode(admincode):
    conn = None 
    try:
        db_path = os.path.abspath('random_number.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO random_number_set (value) VALUES (?)', (admincode,))
        conn.commit()  # 提交事务

        return f"管理员码已设置为{admincode}"
        
    except Exception as e:
        print(f"数据库操作出错: {e}")
        if conn:
            conn.rollback()  # 出错时回滚
        return f"设置管理员码失败: {str(e)}"
    finally:
        if conn:
            conn.close()

def set_groupname(groupname):
    conn = None 
    try:
        db_path = os.path.abspath('random_number.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO group_name (group_name) VALUES (?)', (groupname,))
        conn.commit()  # 提交事务

        return f"已添加监控群：{groupname}"
        
    except Exception as e:
        print(f"数据库操作出错: {e}")
        if conn:
            conn.rollback()  # 出错时回滚
        return f"群名设置失败: {str(e)}"
    finally:
        if conn:
            conn.close()