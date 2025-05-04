import time
import psutil
import win32api
import ctypes
import sys
import win32con
import pywintypes
from win32com.shell import shell


class DisplayManager:
    def __init__(self):
        self.original_settings = {}
        self.disabled_displays = set()

    def get_displays(self):
        displays = []
        i = 0
        while True:
            try:
                display = win32api.EnumDisplayDevices(None, i)
                # 仅处理已连接的显示器
                if display.StateFlags & win32con.DISPLAY_DEVICE_ATTACHED_TO_DESKTOP:
                    displays.append(display)
                i += 1
            except pywintypes.error:
                break
        return displays

    def disable_non_primary(self):
        displays = self.get_displays()
        if len(displays) <= 1:
            return False

        primary_name = None
        for d in displays:
            if d.StateFlags & win32con.DISPLAY_DEVICE_PRIMARY_DEVICE:
                primary_name = d.DeviceName
                break

        success_flag = False
        for display in displays:
            if display.DeviceName == primary_name:
                continue

            # 获取 PyDEVMODEW 对象
            print(display.DeviceName)
            try:
                devmode = win32api.EnumDisplaySettings(
                    display.DeviceName,
                    win32con.ENUM_CURRENT_SETTINGS
                )
            except pywintypes.error as e:
                print(f"获取 {display.DeviceName} 配置失败: {e}")
                continue

            # 保存原始设置（直接存储 PyDEVMODEW 对象）
            self.original_settings[display.DeviceName] = devmode

            # 修改分辨率设置
            devmode.PelsWidth = 0  # 注意属性名不同！
            devmode.PelsHeight = 0
            devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

            # 应用修改
            try:
                result = win32api.ChangeDisplaySettingsEx(
                    display.DeviceName,
                    devmode,  # 传递 PyDEVMODEW 对象
                    win32con.CDS_UPDATEREGISTRY
                )
                if result == win32con.DISP_CHANGE_SUCCESSFUL:
                    success_flag = True
                    self.disabled_displays.add(display.DeviceName)
            except pywintypes.error as e:
                print(f"修改 {display.DeviceName} 失败: {e}")
        return success_flag

    def restore_displays(self):
        for device_name in list(self.disabled_displays):
            devmode = self.original_settings.get(device_name)
            if devmode:
                try:
                    win32api.ChangeDisplaySettingsEx(
                        device_name,
                        devmode,
                        win32con.CDS_UPDATEREGISTRY
                    )
                except pywintypes.error as e:
                    print(f"恢复 {device_name} 失败: {e}")
        self.disabled_displays.clear()


def is_vnc_connected(vnc_port=5900):
    for conn in psutil.net_connections():
        if conn.status == 'ESTABLISHED' and conn.laddr.port == vnc_port:
            return True
    return False


def is_admin():
    """检查管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_elevated():
    lpApplicationName = sys.executable
    lpParameters = __file__

    shell.ShellExecuteEx(lpFile=lpApplicationName,
                         lpParameters=lpParameters,
                         lpVerb='runas',
                         nShow=win32con.SW_SHOW)


def main():
    if not is_admin():
        run_elevated()
        sys.exit()
    else:
        print("is admin")

    dm = DisplayManager()
    last_state = False
    try:
        while True:
            current_state = is_vnc_connected()

            if current_state and not last_state:
                print("检测到VNC连接，尝试禁用非主显示器...")
                dm.disable_non_primary()

            if not current_state and last_state:
                print("连接断开，恢复显示器...")
                dm.restore_displays()

            last_state = current_state
            time.sleep(1)

    except KeyboardInterrupt:
        dm.restore_displays()
        print("程序退出，已恢复显示器设置")


if __name__ == "__main__":
    main()
