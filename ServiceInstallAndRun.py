import ctypes
import sys
import win32con
import win32service
import time
import os
import logging
from datetime import datetime
from win32com.shell import shell
from PySide6.QtCore import QProcess

ultraVnc_exe_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + "x64" + os.sep + "winvnc.exe"

# 创建日志目录（如果不存在）
log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)

# 设置日志文件名（按日期）
log_file = os.path.join(log_dir, f"ServiceInstall_{datetime.now().strftime('%Y-%m-%d')}.log")

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        # logging.StreamHandler()  # 可选：同时输出到控制台
    ]
)


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
    """安装 VNC 服务"""
    process = QProcess()
    args = ["-install"]

    process.start(ultraVnc_exe_path, args)
    if not process.waitForStarted():
        logging.error("无法启动进程")
        return False

    if not process.waitForFinished(-1):
        logging.error("进程执行超时")
        return False

    exit_code = process.exitCode()
    stdout = process.readAllStandardOutput().data().decode('utf-8')
    stderr = process.readAllStandardError().data().decode('utf-8')

    if exit_code != 0:
        logging.error(f"安装失败: {stderr}")
        return False

    logging.info("服务安装成功")
    return True


def ensure_service_running(service_name):
    """确保服务运行"""
    process = QProcess()
    args = ["-Startservice"]

    process.start(ultraVnc_exe_path, args)
    if not process.waitForStarted():
        logging.error("无法启动服务进程")
        return False

    if not process.waitForFinished(-1):
        logging.error("服务启动超时")
        return False

    logging.info("服务启动命令已发送")

    for _ in range(5):
        exists, running = check_service_status(service_name)
        if running:
            logging.info("服务已成功启动")
            return True
        time.sleep(1)
    logging.warning("警告：服务启动状态未确认")
    return False


def allow_pass_firewall(exe_path):
    APP_PATH = exe_path
    RULE_NAME_IN = "Allow Inbound for UltraVNC_Server"
    RULE_NAME_OUT = "Allow Outbound for UltraVNC_Server"

    in_status = False
    out_status = False

    # 检查并创建入站规则
    if not is_firewall_rule_exists(RULE_NAME_IN):
        cmd_in = f'netsh advfirewall firewall add rule name="{RULE_NAME_IN}" dir=in action=allow program="{APP_PATH}" enable=yes'
        in_status = run_cmd_with_qprocess(cmd_in, "入站规则")
    else:
        logging.info("入站规则已存在，跳过创建")
        in_status = True

    # 检查并创建出站规则
    if not is_firewall_rule_exists(RULE_NAME_OUT):
        cmd_out = f'netsh advfirewall firewall add rule name="{RULE_NAME_OUT}" dir=out action=allow program="{APP_PATH}" enable=yes'
        out_status = run_cmd_with_qprocess(cmd_out, "出站规则")
    else:
        logging.info("出站规则已存在，跳过创建")
        out_status = True

    return in_status, out_status


def is_firewall_rule_exists(rule_name):
    """
    检查指定名称的防火墙规则是否存在
    :param rule_name: 规则名称
    :return: bool
    """
    process = QProcess()
    process.start("cmd.exe", ["/c", f'netsh advfirewall firewall show rule name="{rule_name}"'])

    if not process.waitForStarted():
        logging.error(f"无法启动规则检查进程：{rule_name}")
        return False

    if not process.waitForFinished(-1):
        logging.error(f"规则检查超时：{rule_name}")
        return False

    exit_code = process.exitCode()

    # 退出码为0表示规则存在
    return exit_code == 0


def run_cmd_with_qprocess(command, rule_type):
    """使用 QProcess 执行命令并返回执行结果"""
    process = QProcess()
    process.start("cmd.exe", ["/c", command])

    if not process.waitForStarted():
        logging.error(f"{rule_type}启动失败")
        return False

    if not process.waitForFinished(-1):
        logging.error(f"{rule_type}执行超时")
        return False

    exit_code = process.exitCode()
    stderr = process.readAllStandardError().data().decode('utf-8')

    if exit_code != 0:
        logging.error(f"{rule_type}失败：{stderr}")
        return False

    logging.info(f"{rule_type}已创建")
    return True


def main():
    SERVICE_NAME = "uvnc_service"

    if not is_admin():
        run_as_admin()
        sys.exit()
    else:
        logging.info("is admin")

    exists, running = check_service_status(SERVICE_NAME)

    if not exists:
        logging.info("未检测到服务，开始安装...")
        if install_service():
            exists, running = check_service_status(SERVICE_NAME)
            if not exists:
                logging.error("错误：服务安装后仍未检测到")
                return None
        else:
            return None

    if not running:
        logging.info("服务未运行，尝试启动...")
        if not ensure_service_running(SERVICE_NAME):
            logging.error("错误：服务启动失败，请手动检查")

    firewall_results = allow_pass_firewall(ultraVnc_exe_path)
    if all(firewall_results):
        logging.info("防火墙规则创建成功")
    else:
        logging.error("防火墙规则创建失败，请手动创建")
