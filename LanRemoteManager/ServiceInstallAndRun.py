import ctypes
import sys
import subprocess
import win32service
import time
import os

ultraVnc_exe_path = f"{os.path.dirname(os.path.abspath(__file__))}{os.sep}x64{os.sep}winvnc.exe"

def is_admin():
    """检查管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_service_status(service_name):
    """检测服务存在及运行状态"""
    try:
        scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
        service = win32service.OpenService(scm, service_name, win32service.SERVICE_QUERY_STATUS)
        status = win32service.QueryServiceStatus(service)
        win32service.CloseServiceHandle(service)
        win32service.CloseServiceHandle(scm)
        return True, status[1] == win32service.SERVICE_RUNNING
    except Exception as e:
        if "1060" in str(e).lower():
            return False, False
        # raise


def install_service():
    """安装VNC服务"""
    try:
        result = subprocess.run(
            [ultraVnc_exe_path, "-install"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        print("服务安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装失败: {e.stderr}")
        return False


def ensure_service_running(service_name):
    """确保服务运行"""
    try:
        subprocess.run(
            [ultraVnc_exe_path, "-Startservice"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        print("服务启动命令已发送")

        # 等待服务状态更新
        for _ in range(5):
            exists, running = check_service_status(service_name)
            if running:
                print("服务已成功启动")
                return True
            time.sleep(1)
        print("警告：服务启动状态未确认")
        return False
    except Exception as e:
        print(f"启动失败: {str(e)}")
        return False


def main():
    SERVICE_NAME = "uvnc_service"

    # 提权检测
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        # sys.exit()

    # 服务状态检测
    exists, running = check_service_status(SERVICE_NAME)

    if not exists:
        print("未检测到服务，开始安装...")
        if install_service():
            # 安装后重新检测
            exists, running = check_service_status(SERVICE_NAME)
            if not exists:
                print("错误：服务安装后仍未检测到")
                return None
        else:
            return None

    if not running:
        print("服务未运行，尝试启动...")
        if not ensure_service_running(SERVICE_NAME):
            print("错误：服务启动失败，请手动检查")


if __name__ == "__main__":
    main()
