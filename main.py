import sys

import ServiceInstallAndRun
import GetClientInfo
from main_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem
from PySide6.QtCore import QTimer, QDateTime, Qt, QThread, Signal, Slot
from PySide6.QtSql import QSqlDatabase, QSqlQuery


class DatabaseWorker(QThread):
    query_result = Signal(list)  # 查询结果信号
    error_occurred = Signal(str)  # 错误信号

    def __init__(self):
        super().__init__()
        self.query_queue = []  # 查询任务队列
        self.is_running = True  # 线程运行标志

    def run(self):
        """线程主循环，持续监听查询请求"""
        db = QSqlDatabase.addDatabase('QMYSQL', 'worker_connection')  # 独立连接
        db.setDatabaseName("LanRemoteManager")
        db.setHostName("192.168.241.38")
        db.setPort(3306)
        db.setUserName("root")
        db.setPassword("yuan@5419")
        if not db.open():
            self.error_occurred.emit("数据库连接失败")
            return

        while self.is_running:
            if self.query_queue:
                query_str = self.query_queue.pop(0)  # 取出查询语句
                try:
                    query = QSqlQuery(db)
                    if query.exec(query_str):
                        results = []
                        while query.next():
                            row = [str(query.value(col)) for col in range(query.record().count())]
                            results.append(row)
                        self.query_result.emit(results)  # 发送结果
                    else:
                        self.error_occurred.emit(f"查询失败: {query.lastError().text()}")
                except Exception as e:
                    self.error_occurred.emit(f"执行异常: {str(e)}")
            else:
                self.msleep(100)  # 避免CPU空转

        db.close()  # 退出时关闭连接

    def stop(self):
        """安全停止线程"""
        self.is_running = False
        self.wait()

    @Slot(str)
    def receive_query(self, query_str):
        """接收主线程的查询请求"""
        self.query_queue.append(query_str)


class FuncQLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("<a href='连接'><font color=blue>连接</font></a> | <a href='编辑'><font color=blue>编辑</font></a>")
        self.setAlignment(Qt.AlignCenter)
        self.linkActivated.connect(lambda x: self.click_link(x))

    def click_link(self, string):
        print(f"{string}")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 创建时间更新定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每1000毫秒（1秒）触发一次

        # 创建客户端信息更新定时器
        self.client_info_timer = QTimer(self)
        self.client_info_timer.timeout.connect(self.update_client_info)
        self.client_info_timer.start(10000)

        # 立即显示初始时间
        self.update_time()
        self.update_client_info()

        # 创建持久数据库查询线程
        self.worker = DatabaseWorker()
        self.worker.query_result.connect(self.update_table)
        self.worker.error_occurred.connect(self.show_error)
        self.worker.start()

        self.actionoff.triggered.connect(lambda: self.worker.stop())
        self.pushButton.clicked.connect(lambda: self.send_query_to_worker())
        self.ClientRecordTable.itemClicked.connect(lambda x: self.statusbar.showMessage(
            f"坐标({self.ClientRecordTable.row(x)},{self.ClientRecordTable.column(x)})", 2000))

    def update_time(self):
        # 获取当前时间并格式化
        current_time = QDateTime.currentDateTime()
        time_str = current_time.toString("yyyy-MM-dd HH:mm:ss")
        self.TimeLabel.setText(time_str)

    def update_client_info(self):
        client_info = GetClientInfo.get_system_info()
        self.FullNameLabel.setText(client_info["full_name"])
        self.IpLabel.setText(client_info['ip_address'])
        self.MacLabel.setText(client_info['mac_address'])
        self.LoginUserLabel.setText(client_info['login_user'])
        self.ClientNameLabel.setText(client_info['computer_name'])

    def send_query_to_worker(self):
        query_str = self.lineEdit.text()
        if query_str:
            query_str = ("SELECT full_name, login_user, computer_name, ip_address, mac_address, last_login, "
                         "client_note FROM ClientInfo LIMIT 10")
            self.lineEdit.clear()
            self.worker.receive_query(query_str)  # 发送查询请求
        else:
            query_str = ("SELECT full_name, login_user, computer_name, ip_address, mac_address, last_login, "
                         "client_note FROM ClientInfo")
            self.worker.receive_query(query_str)

    def update_table(self, results):
        """更新表格数据"""
        self.ClientRecordTable.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                self.ClientRecordTable.setItem(row, col, QTableWidgetItem(value))
            self.ClientRecordTable.setCellWidget(row, 7, FuncQLabel())

    def show_error(self, error_msg):
        self.statusbar.showMessage(f"错误: {error_msg}", 5000)


if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
