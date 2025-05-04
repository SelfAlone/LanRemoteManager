import psutil
import socket
import time
import win32api
import win32con

# 配置UltraVNC服务端口
VNC_PORT = 5900


def is_vnc_connected():
    """检测UltraVNC客户端连接状态"""
    for conn in psutil.net_connections():
        if (conn.type == socket.SOCK_STREAM and  # 使用 socket 模块
                conn.status == 'ESTABLISHED' and
                conn.laddr.port == VNC_PORT):
            return True
    return False


def is_multi_monitor():
    """检测是否为多显示器环境"""
    return win32api.GetSystemMetrics(win32con.SM_CMONITORS) > 1


def disable_secondary_displays():
    """关闭除主显示器外的所有显示器"""
    monitors = win32api.EnumDisplayMonitors()
    if len(monitors) <= 1:
        return

    for i, monitor in enumerate(monitors):
        if i == 0:  # 跳过主显示器
            continue

        devmode = win32api.EnumDisplaySettings(
            monitor[1].DeviceName,
            win32con.ENUM_CURRENT_SETTINGS
        )

        # 设置分辨率为0x0以禁用显示器
        devmode.PelsWidth = 0
        devmode.PelsHeight = 0
        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

        win32api.ChangeDisplaySettingsEx(
            monitor[1].DeviceName,
            devmode,
            win32con.CDS_UPDATEREGISTRY
        )


def restore_displays():
    """恢复所有显示器到原始状态"""
    monitors = win32api.EnumDisplayMonitors()
    if len(monitors) <= 1:
        return

    for i, monitor in enumerate(monitors):
        if i == 0:
            continue

        devmode = win32api.EnumDisplaySettings(
            monitor[1].DeviceName,
            win32con.ENUM_REGISTRY_SETTINGS
        )

        win32api.ChangeDisplaySettingsEx(
            monitor[1].DeviceName,
            devmode,
            win32con.CDS_UPDATEREGISTRY
        )


def main():
    """主监控循环"""
    vnc_connected = False
    while True:
        current_status = is_vnc_connected() and is_multi_monitor()

        if current_status and not vnc_connected:
            disable_secondary_displays()
            print("已关闭非主显示器")

        elif not current_status and vnc_connected:
            restore_displays()
            print("已恢复所有显示器")

        vnc_connected = current_status
        time.sleep(1)  # 每秒检查一次连接状态


if __name__ == "__main__":
    main()
