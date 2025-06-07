import sys

import ServiceInstallAndRun
import GetClientInfo
from main_ui import Ui_MainWindow
from EditDialog_ui import Ui_EditDialog
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem, QDialog, QMessageBox
from PySide6.QtCore import QTimer, QDateTime, Qt, QThread, Signal, Slot, QProcess
from PySide6.QtSql import QSqlDatabase, QSqlQuery

from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtSql import QSqlQuery, QSqlDatabase


class DatabaseWorker(QThread):
    # 查询相关信号
    query_result = Signal(list)  # 查询结果
    query_error = Signal(str)  # 查询错误

    # 更新相关信号
    update_result = Signal(int)  # 更新成功，返回受影响行数
    update_error = Signal(str)  # 更新失败

    def __init__(self):
        super().__init__()
        self.task_queue = []  # 任务队列，统一处理查询和更新
        self.is_running = True  # 线程运行标志

    def run(self):
        """线程主循环，持续监听任务请求"""
        db = QSqlDatabase.addDatabase('QODBC', 'worker_connection')  # 独立连接
        db.setDatabaseName("RemoteConnection")
        db.setHostName("192.168.2.31")
        db.setPort(1433)
        db.setUserName("temp")
        db.setPassword("Egnc201*")

        if not db.open():
            self.query_error.emit(f"错误：{db.lastError()}")
            return

        while self.is_running:
            if self.task_queue:
                task = self.task_queue.pop(0)  # 取出任务
                sql = task.get("sql", "")
                task_type = task.get("type", "query")  # 默认为查询
                params = task.get("params", [])  # 可选参数

                try:
                    query = QSqlQuery(db)
                    if params:
                        query.prepare(sql)
                        for param in params:  # 循环替换占位符
                            query.addBindValue(f'%{param}%')
                        success = query.exec()
                    else:
                        success = query.exec(sql)

                    if not success:
                        error_msg = query.lastError().text()
                        if task_type == "query":
                            self.query_error.emit(f"查询失败: {error_msg}")
                        else:
                            self.update_error.emit(f"更新失败: {error_msg}")
                        continue

                    if task_type == "query":
                        results = []
                        while query.next():
                            row = [str(query.value(col)) for col in range(query.record().count())]
                            results.append(row)
                        self.query_result.emit(results)
                    else:
                        if query.numRowsAffected() == 0:  # 已更新的行数
                            self.update_error.emit(f"更新失败: 受影响的记录数为0，语句错误")
                        else:
                            self.update_result.emit(query.numRowsAffected())  # 返回受影响行数

                except Exception as e:
                    if task_type == "query":
                        self.query_error.emit(f"查询异常: {str(e)}")
                    else:
                        self.update_error.emit(f"更新异常: {str(e)}")

            else:
                self.msleep(100)  # 避免 CPU 空转

        db.close()  # 退出时关闭连接

    def stop(self):
        """安全停止线程"""
        self.is_running = False
        self.wait()

    @Slot(dict)
    def receive_task(self, task):
        """接收主线程的任务请求，格式：{'type': 'query'/'update', 'sql': '...', 'params': [...]}"""
        self.task_queue.append(task)

    # 便捷方法：发送查询任务
    def send_query(self, sql, params=None):
        task = {"type": "query", "sql": sql}
        if params:
            task["params"] = params
        self.receive_task(task)

    # 便捷方法：发送更新任务
    def send_update(self, sql, params=None):
        task = {"type": "update", "sql": sql}
        if params:
            task["params"] = params
        self.receive_task(task)

    # 便捷方法：发送插入任务
    def send_insert(self, sql, params=None):
        task = {"type": "insert", "sql": sql}
        if params:
            task["params"] = params
        self.receive_task(task)


class EditDialog(QDialog, Ui_EditDialog):
    """编辑/更新记录窗口"""

    def __init__(self, table, db):
        super(EditDialog, self).__init__()
        self.setupUi(self)
        self.windowTitle("编辑")
        self.clientRecordTable = table
        self.db_worker = db

        # 填充QLineEdit控件
        edit_info = self.get_edit_info()  # 从当前记录获取填充信息
        self.NameEdit.setText(edit_info[0])
        self.ComputerEdit.setText(edit_info[1])
        self.IPEdit.setText(edit_info[2])
        self.noteEdit.setText(edit_info[3])

        self.buttonBox.accepted.connect(self.send_update_to_worker)
        self.buttonBox.rejected.connect(self.close)

    def send_update_to_worker(self):
        new_record = [self.NameEdit.text().strip(), self.ComputerEdit.text().strip(), self.IPEdit.text().strip(),
                      self.noteEdit.toPlainText().strip()]
        if new_record == self.get_edit_info():  # 新记录是否与原记录相同
            QMessageBox.information(self, "信息", "未对记录做出修改，无需更新", QMessageBox.Ok)
        else:
            new_record.extend(self.get_primary())  # 增加主键信息
            update_sentence = (f"UPDATE ComputerList SET Name = '{new_record[0]}', ComputerName = '{new_record[1]}', "
                               f"ComputerIP = '{new_record[2]}', Tab = '{new_record[3]}' WHERE LoginUserName = "
                               f"'{new_record[4]}' AND ComputerName = '{new_record[5]}'")  # SQL更新语句
            self.db_worker.update_result.connect(lambda: self.update_local_record(new_record))  # 数据库更新成功后再更新本地记录
            self.db_worker.send_update(update_sentence)

    def get_edit_info(self):
        name = self.clientRecordTable.item(self.clientRecordTable.currentRow(), 0).text()
        computer_name = self.clientRecordTable.item(self.clientRecordTable.currentRow(), 2).text()
        ip = self.clientRecordTable.item(self.clientRecordTable.currentRow(), 3).text()
        note = self.clientRecordTable.item(self.clientRecordTable.currentRow(), 6).text()
        return [name, computer_name, ip, note]

    def get_primary(self):
        return [self.clientRecordTable.item(self.clientRecordTable.currentRow(), 1).text(),
                self.clientRecordTable.item(self.clientRecordTable.currentRow(), 2).text()]

    def update_local_record(self, new_record):
        self.clientRecordTable.item(self.clientRecordTable.currentRow(), 0).setText(new_record[0])
        self.clientRecordTable.item(self.clientRecordTable.currentRow(), 2).setText(new_record[1])
        self.clientRecordTable.item(self.clientRecordTable.currentRow(), 3).setText(new_record[2])
        self.clientRecordTable.item(self.clientRecordTable.currentRow(), 6).setText(new_record[3])


class FuncQLabel(QLabel):
    def __init__(self, table, db):
        super().__init__()
        self.ClientRecordTable = table
        self.db_worker = db
        self.setText(
            "<a href='Link'><font color=blue>连接</font></a> | <a href='Edit'><font color=blue>编辑</font></a>")
        self.setAlignment(Qt.AlignCenter)
        self.linkActivated.connect(self.click_link)

    def click_link(self, key):
        """调用UltraVNC外部程序"""
        if key == "Link":
            vnc_process = QProcess()
            vnc_path = r".\x64\vncviewer.exe"
            ip = self.ClientRecordTable.item(self.ClientRecordTable.currentRow(), 3).text()
            args = [
                f"{ip}",
                "-password",
                "805635"
            ]
            vnc_process.setProgram(vnc_path)
            vnc_process.setArguments(args)
            vnc_process.startDetached()
        if key == "Edit":
            edit_dialog = EditDialog(self.ClientRecordTable, self.db_worker)  # 传入主窗口表格控件与数据库工作线程
            edit_dialog.show()
            edit_dialog.exec()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 创建时间更新定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每1000毫秒（1秒）触发一次

        # 创建客户端信息显示刷新定时器
        self.dis_client_info_timer = QTimer(self)
        self.dis_client_info_timer.timeout.connect(self.display_client_info)
        self.dis_client_info_timer.start(10000)

        # 创建客户端信息更新定时器
        self.update_client_info_timer = QTimer(self)
        self.update_client_info_timer.timeout.connect(self.send_insert_to_worker)
        self.update_client_info_timer.start(9000000)

        # 立即显示初始时间
        self.update_time()
        self.display_client_info()

        # 创建持久数据库查询线程
        self.db_worker = DatabaseWorker()
        self.db_worker.query_result.connect(self.update_table)
        self.db_worker.query_error.connect(self.show_message)
        self.db_worker.update_result.connect(
            lambda x: QMessageBox.information(self, "信息", f"已成功更新{x}条记录", QMessageBox.Ok))
        self.db_worker.update_error.connect(self.show_message)
        self.db_worker.start()

        self.actionoff.triggered.connect(self.db_worker.stop)
        self.pushButton.clicked.connect(self.send_query_to_worker)
        self.lineEdit.returnPressed.connect(self.send_query_to_worker)
        self.ClientRecordTable.itemClicked.connect(lambda x: self.statusbar.showMessage(
            f"坐标({self.ClientRecordTable.row(x)},{self.ClientRecordTable.column(x)})", 2000))

    def update_time(self):
        # 获取当前时间并格式化
        current_time = QDateTime.currentDateTime()
        time_str = current_time.toString("yyyy-MM-dd HH:mm:ss")
        self.TimeLabel.setText(time_str)

    def display_client_info(self):
        client_info = GetClientInfo.get_system_info()
        self.FullNameLabel.setText(client_info["full_name"])
        self.IpLabel.setText(client_info['ip_address'])
        self.MacLabel.setText(client_info['mac_address'])
        self.LoginUserLabel.setText(client_info['login_user'])
        self.ClientNameLabel.setText(client_info['computer_name'])

    def send_insert_to_worker(self):
        pass

    def send_query_to_worker(self):
        query_str = [self.lineEdit.text()] * 7
        if query_str[0]:
            query_sentence = ("SELECT Name, LoginUserName, ComputerName, ComputerIP, "
                              "ComputerMAC, StartTime, Tab FROM ComputerList "
                              f"WHERE Name LIKE ? or LoginUserName LIKE ? "
                              f"or ComputerName LIKE ? or ComputerIP LIKE ? "
                              f"or ComputerMAC LIKE ? or StartTime LIKE ? or Tab LIKE ?")
            self.lineEdit.clear()
            self.db_worker.send_query(query_sentence, query_str)  # 发送查询请求
        else:
            query_sentence = ("SELECT Name, LoginUserName, ComputerName, ComputerIP, "
                              "ComputerMAC, StartTime, Tab FROM ComputerList")
            self.db_worker.send_query(query_sentence)

    def update_table(self, results):
        """更新表格数据"""
        self.ClientRecordTable.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                self.ClientRecordTable.setItem(row, col, QTableWidgetItem(value))
            self.ClientRecordTable.setCellWidget(row, 7, FuncQLabel(self.ClientRecordTable, self.db_worker))  # 添加自定义控件
        self.ClientRecordTable.resizeColumnsToContents()  # 根据内容自适应列宽

    def show_message(self, msg):
        self.statusbar.showMessage(f"{msg}", 5000)


if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
