import time
import json
import os
import socket
from datetime import datetime
import psutil
import ctypes
from ctypes import wintypes
from typing import Dict, Any

# 配置项
CONFIG = {
    "db_type": "mysql",  # mysql 或 mssql
    "check_interval": 1 * 10 * 60,  # 10分钟（秒）
    "state_file": f"{os.path.dirname(os.path.abspath(__file__))}{os.sep}system_monitor_state.json",
    "mysql": {
        "host": "192.168.241.38",
        "user": "root",
        "password": "yuan@5419",
        "database": "LanRemoteManager",
        "port": 3306
    },
    "mssql": {
        "server": "your_server",
        "database": "your_database",
        "user": "your_username",
        "password": "your_password",
        "driver": "ODBC Driver 17 for SQL Server"
    }
}


def is_physical_interface(iface_name: str) -> bool:
    """基于名称特征的物理接口判断"""
    virtual_keywords = [
        'Virtual', 'VPN', 'Hyper-V',
        'VMware', 'VBox', 'vEthernet',
        'WSL', "wsl", "VMnet", "Loopback"
    ]
    return not any(kw in iface_name for kw in virtual_keywords)


def get_windows_user_full_name():
    # 定义函数参数和返回值类型
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    GetUserNameEx.argtypes = [
        wintypes.DWORD,  # NameFormat 参数
        wintypes.LPWSTR,  # lpNameBuffer 缓冲区
        ctypes.POINTER(wintypes.DWORD)  # 修正：使用 ctypes.POINTER
    ]
    GetUserNameEx.restype = wintypes.BOOL

    # 定义名称格式：NameDisplay（对应值为 3）
    NameDisplay = 3
    size = wintypes.DWORD(0)

    # 第一次调用获取所需缓冲区大小
    GetUserNameEx(NameDisplay, None, ctypes.byref(size))

    # 创建足够大的缓冲区
    buffer = ctypes.create_unicode_buffer(size.value)

    # 第二次调用获取实际数据
    if GetUserNameEx(NameDisplay, buffer, ctypes.byref(size)):
        return buffer.value
    else:
        return None  # 失败时返回空


def get_system_info() -> Dict[str, Any]:
    # 基础信息（不变化的部分只需获取一次）
    static_info = {
        "computer_name": socket.gethostname(),
        "full_name": get_windows_user_full_name(),
        "login_user": psutil.users()[0].name,
    }

    # 网络信息
    net_info = {}
    try:
        # 获取活动网络接口
        interface = psutil.net_if_stats()
        active_iface = [k for k, v in interface.items() if v.isup and is_physical_interface(k)]

        if active_iface:
            ifaddresses = psutil.net_if_addrs().get(active_iface[0], [])
            for addr in ifaddresses:
                if addr.family == psutil.AF_LINK:
                    net_info["mac_address"] = addr.address.replace('-', ':')
                elif addr.family == socket.AF_INET:
                    net_info["ip_address"] = addr.address

    except Exception as e:
        print(f"网络信息获取失败: {str(e)}")

    return {
        **static_info,
        **net_info,
        "last_login": datetime.now().isoformat()
    }


class StateManager:
    """状态持久化管理器"""

    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"状态加载失败: {str(e)}")
        return {}

    def save_state(self, data: Dict) -> None:
        try:
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"状态保存失败: {str(e)}")

    def compare_state(self, new_data: Dict) -> bool:
        """比较状态变化，排除last_login字段"""
        old_data = self.state.copy()
        old_data.pop('last_login', None)
        current_data = new_data.copy()
        current_data.pop('last_login', None)
        return old_data == current_data


class DatabaseClient:
    """高效数据库客户端"""

    def __init__(self, config: Dict):
        self.config = config
        self._conn = None

    @property
    def connection(self):
        """按需创建连接"""
        if not self._conn or not self._ping():
            self._connect()
        return self._conn

    def _ping(self) -> bool:
        """检查连接有效性"""
        try:
            if self.config['db_type'] == 'mysql':
                self._conn.ping(reconnect=True)
            return True
        except:
            return False

    def _connect(self):
        """建立新连接"""
        try:
            if self.config['db_type'] == 'mysql':
                import pymysql
                self._conn = pymysql.connect(
                    host=self.config['mysql']['host'],
                    user=self.config['mysql']['user'],
                    password=self.config['mysql']['password'],
                    database=self.config['mysql']['database'],
                    port=self.config['mysql']['port'],
                    cursorclass=pymysql.cursors.DictCursor
                )
            elif self.config['db_type'] == 'mssql':
                import pyodbc
                self._conn = pyodbc.connect(
                    f"DRIVER={self.config['mssql']['driver']};"
                    f"SERVER={self.config['mssql']['server']};"
                    f"DATABASE={self.config['mssql']['database']};"
                    f"UID={self.config['mssql']['user']};"
                    f"PWD={self.config['mssql']['password']}"
                )
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")
            raise

    def upsert_record(self, data: Dict):
        """高效更新插入操作"""
        try:
            with self.connection.cursor() as cursor:
                # 使用参数化查询防止SQL注入
                if self.config['db_type'] == 'mysql':
                    sql = """
                    INSERT INTO ClientInfo 
                    (computer_name, full_name, login_user, ip_address, mac_address, last_login)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        ip_address = VALUES(ip_address),
                        mac_address = VALUES(mac_address),
                        last_login = VALUES(last_login)
                    """
                else:  # MSSQL
                    sql = """
                    MERGE INTO device_info AS target
                    USING (VALUES (?, ?, ?, ?, ?)) AS source 
                        (computer_name, login_user, ip_address, mac_address, last_login)
                    ON target.computer_name = source.computer_name 
                        AND target.login_user = source.login_user
                    WHEN MATCHED THEN
                        UPDATE SET 
                            ip_address = source.ip_address,
                            mac_address = source.mac_address,
                            last_login = source.last_login
                    WHEN NOT MATCHED THEN
                        INSERT VALUES (source.computer_name, source.login_user, 
                                      source.ip_address, source.mac_address, source.last_login);
                    """
                cursor.execute(sql, (
                    data['computer_name'],
                    data['full_name'],
                    data['login_user'],
                    data.get('ip_address', ''),
                    data.get('mac_address', ''),
                    data['last_login']
                ))
                self._conn.commit()
                return True
        except Exception as e:
            print(f"数据库操作失败: {str(e)}")
            self._conn.rollback()
            return False


def main():
    # 初始化组件
    state_mgr = StateManager(CONFIG['state_file'])
    db_client = DatabaseClient(CONFIG)

    # 初始状态
    last_update_time = 0
    start_update_times = False

    while True:
        try:
            current_data = get_system_info()

            # 判断是否需要更新（1小时周期或数据变化）
            if (time.time() - last_update_time > CONFIG['check_interval'] or
                not state_mgr.compare_state(current_data)) or not start_update_times:

                for _ in range(60):
                    if db_client.upsert_record(current_data):
                        start_update_times = True
                        state_mgr.save_state(current_data)
                        last_update_time = time.time()
                        print(f"数据更新成功: {current_data}")
                        break
                    else:
                        time.sleep(10)
                        print("数据更新失败")
                else:
                    raise ConnectionError("数据更新失败，请检查网络连接与数据库配置")

            # 使用高效休眠（分多次短休眠以便响应信号）
            for __ in range(10):  # 10分钟 = 10 * 60秒
                time.sleep(60)

        except KeyboardInterrupt:
            print("程序已终止")
            break
        except Exception as e:
            print(f"运行时错误: {str(e)}")
            time.sleep(60)  # 错误后等待1分钟再重试


if __name__ == "__main__":
    main()
