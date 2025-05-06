import ctypes
import sys
import subprocess
import win32con
import win32service
import time
import os
from win32com.shell import shell

ultraVnc_exe_path = f"{os.path.dirname(os.path.abspath(__file__))}{os.sep}x64{os.sep}winvnc.exe"


def is_admin():
    """检查管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    lpApplicationName = sys.executable
    lpParameters = __file__

    shell.ShellExecuteEx(lpFile=lpApplicationName,
                         lpParameters=lpParameters,
                         lpVerb='runas',
                         nShow=win32con.SW_SHOW)


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


def allow_pass_firewall():
    # 设置程序路径
    APP_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep + "x64" + os.sep + "winvnc.exe"
    RULE_NAME_IN = f"Allow Inbound for UltraVNC_Server"
    RULE_NAME_OUT = f"Allow Outbound for UltraVNC_Server"

    in_status = False
    out_status = False

    # 添加入站规则
    try:
        subprocess.run(
            f'netsh advfirewall firewall add rule name="{RULE_NAME_IN}" dir=in action=allow program="{APP_PATH}" enable=yes',
            check=True,
            shell=True
        )
        print(f"入站规则已创建：{RULE_NAME_IN}")
        in_status = True
    except subprocess.CalledProcessError as e:
        print(f"入站规则创建失败：{e}")

    # 添加出站规则
    try:
        subprocess.run(
            f'netsh advfirewall firewall add rule name="{RULE_NAME_OUT}" dir=out action=allow program="{APP_PATH}" enable=yes',
            check=True,
            shell=True
        )
        print(f"出站规则已创建：{RULE_NAME_OUT}")
        out_status = True
    except subprocess.CalledProcessError as e:
        print(f"出站规则创建失败：{e}")
    return in_status, out_status


def main():
    SERVICE_NAME = "uvnc_service"

    # 提权检测
    if not is_admin():
        run_as_admin()
        sys.exit()
    else:
        print("is admin")
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

    if all(allow_pass_firewall()):
        print("防火墙规则创建成功")
    else:
        print("防火墙规则创建失败，请手动创建")


if __name__ == "__main__":
    main()
