import socket
from datetime import datetime
import psutil
import ctypes
from ctypes import wintypes
from typing import Dict, Any


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
    # 基础信息
    static_info = {
        "ComputerName": socket.gethostname(),
        "Name": get_windows_user_full_name(),
        "LoginUserName": psutil.users()[0].name,
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
                    net_info["ComputerMAC"] = addr.address.replace('-', ':')
                elif addr.family == socket.AF_INET:
                    net_info["ComputerIP"] = addr.address
        else:
            net_info["ComputerMAC"] = "00:00:00:00:00:00"
            net_info["ComputerIP"] = "169.254.169.254"

    except Exception as e:
        return {
            **static_info,
            "ComputerIP": "169.254.169.254",
            "ComputerMAC": "00:00:00:00:00:00",
            "StartTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    return {
        **static_info,
        **net_info,
        "StartTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
