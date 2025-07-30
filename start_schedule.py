import subprocess
import multiprocessing
import time

def run_script(script_name):
    """运行独立的 Python 脚本"""
    subprocess.run(["python", script_name])

def start_schedules():
    """启动调度进程（可被其他程序调用）"""
    scripts = [
        {"name": "operation_module.py", "count": 1},
        {"name": "holiday_module.py", "count": 1},
        {"name": "Turn_Screen.py", "count": 1},
        {"name": "bot_start.py", "count": 1}
    ]

    processes = []

    try:
        for script_info in scripts:
            for _ in range(script_info["count"]):
                process = multiprocessing.Process(
                    target=run_script,
                    args=(script_info["name"],)
                )
                processes.append(process)
                process.start()

        print("All schedule processes started successfully")
        return processes  # 返回进程列表，方便管理

    except Exception as e:
        print(f"Error starting schedules: {e}")
        return []

if __name__ == "__main__":
    processes = start_schedules()
    try:
        for process in processes:
            process.join()  # 阻塞等待（通常调度程序不会退出）
    except KeyboardInterrupt:
        print("\nReceived interrupt, terminating processes...")
        for process in processes:
            if process.is_alive():
                process.terminate()
        print("All processes terminated")