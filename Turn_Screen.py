import ctypes
import time
import screen_brightness_control as sbc  # 推荐库
 
def prevent_sleep_and_dim_screen():
    # 防止屏幕关闭
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000002 | 0x00000001)
    
    # 降低亮度（30%）
    try:
        sbc.set_brightness(30)
    except Exception as e:
        print(f"亮度调整失败: {e}")
 
    try:
        print("程序运行中... 按 Ctrl+C 退出")
        while True:
            time.sleep(1)
    finally:
        # 恢复设置
        sbc.set_brightness(100)  # 恢复亮度
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # 允许屏幕关闭
 
if __name__ == "__main__":
    prevent_sleep_and_dim_screen()