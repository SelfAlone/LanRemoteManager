import sys

import ServiceInstallAndRun
import GetClientInfo
from main_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, QDateTime


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每1000毫秒（1秒）触发一次

        # 立即显示初始时间
        self.update_time()

        self.client_info = GetClientInfo.get_system_info()
        self.label.setText(self.client_info["full_name"])
        self.ip_info.setText(self.client_info['ip_address'])
        self.mac_info.setText(self.client_info['mac_address'])
        self.login_user.setText(self.client_info['login_user'])
        self.pc_name.setText(self.client_info['computer_name'])

    def update_time(self):
        # 获取当前时间并格式化
        current_time = QDateTime.currentDateTime()
        time_str = current_time.toString("yyyy-MM-dd HH:mm:ss")
        self.time.setText(time_str)


if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
