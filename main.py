import sys
import pymssql
import json
from pathlib import Path

import ServiceInstallAndRun as Service
import GetClientInfo
from main_ui import Ui_MainWindow
from EditDialog_ui import Ui_EditDialog
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem, QDialog, QMessageBox
from PySide6.QtCore import QTimer, QDateTime, Qt, QThread, Signal, Slot, QProcess


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
        self.connection = None  # 数据库连接

    def run(self):
        """线程主循环，持续监听任务请求"""
        while self.is_running:
            try:
                # 建立数据库连接
                self.connection = pymssql.connect(
                    server="192.168.23.236",
                    port=1433,
                    database="LanRemoteMaster",
                    user="sa",
                    password="yuan@5419"
                )
                break
            except pymssql.DatabaseError as e:
                self.query_error.emit(f"数据库连接失败: {str(e)}")
                self.sleep(5)

        while self.is_running:
            if self.task_queue:
                task = self.task_queue.pop(0)  # 取出任务
                sql = task.get("sql", "")
                task_type = task.get("type", "query")  # 默认为查询
                params = task.get("params", [])  # 可选参数

                try:
                    with self.connection.cursor() as cursor:
                        # 构建模糊查询参数（%param%）
                        formatted_params = [f"{param}" for param in params]

                        # 执行 SQL 查询或更新
                        cursor.execute(sql, formatted_params)

                        if task_type == "query":
                            results = cursor.fetchall()
                            self.query_result.emit(results)
                        elif task_type == "update":
                            self.connection.commit()
                            rows_affected = cursor.rowcount
                            if rows_affected == 0:
                                self.update_error.emit("更新失败: 受影响的记录数为0")
                            else:
                                self.update_result.emit(rows_affected)
                except pymssql.DatabaseError as e:
                    if task_type == "query":
                        self.query_error.emit(f"查询失败: {str(e)}")
                    elif task_type == "update":
                        self.update_error.emit(f"更新失败: {str(e)}")
                except Exception as e:
                    if task_type == "query":
                        self.query_error.emit(f"查询异常: {str(e)}")
                    elif task_type == "update":
                        self.update_error.emit(f"更新异常: {str(e)}")
            else:
                self.msleep(100)  # 避免 CPU 空转

        # 关闭数据库连接
        if self.connection:
            self.connection.close()

    def stop(self):
        """安全停止线程"""
        self.is_running = False
        self.terminate()
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


class Worker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, target_func=None):
        super().__init__()
        self.target_func = target_func
        self.is_running = True

    def run(self):
        try:
            if self.target_func:
                self.target_func()
            self.finished.emit("信息：服务已成功安装并运行")
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.is_running = False

    def stop(self):
        """安全停止线程"""
        self.is_running = False
        self.terminate()
        self.wait()


class EditDialog(QDialog, Ui_EditDialog):
    """编辑/更新记录窗口"""

    def __init__(self, table, db):
        super(EditDialog, self).__init__()
        self.setupUi(self)
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
                "111111"
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
        self.db_worker = None
        self.service_worker = None

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

        # 创建持久数据库查询线程
        self.db_worker = DatabaseWorker()
        self.db_worker.query_result.connect(self.update_table)
        self.db_worker.query_error.connect(self.show_message)
        self.db_worker.update_result.connect(
            lambda x: QMessageBox.information(self, "信息", f"已成功更新{x}条记录", QMessageBox.Ok))
        self.db_worker.update_error.connect(self.show_message)
        self.db_worker.start()

        # 立即运行定时器任务
        self.update_time()
        self.display_client_info()
        self.send_insert_to_worker()

        self.actionoff.triggered.connect(self.db_worker.stop)
        self.pushButton.clicked.connect(self.send_query_to_worker)
        self.lineEdit.returnPressed.connect(self.send_query_to_worker)
        self.ClientRecordTable.itemClicked.connect(lambda x: self.statusbar.showMessage(
            f"坐标({self.ClientRecordTable.row(x)},{self.ClientRecordTable.column(x)})", 2000))

        # 使用 QTimer.singleShot 延迟启动线程，确保 UI 已渲染
        QTimer.singleShot(0, self.service_install)

    def service_install(self):
        self.service_worker = Worker(Service.main)
        self.service_worker.finished.connect(self.show_message)
        self.service_worker.error.connect(self.show_message)
        self.service_worker.start()

    def update_time(self):
        # 获取当前时间并格式化
        current_time = QDateTime.currentDateTime()
        time_str = current_time.toString("yyyy-MM-dd HH:mm:ss")
        self.TimeLabel.setText(time_str)

    def display_client_info(self):
        client_info = GetClientInfo.get_system_info()
        self.FullNameLabel.setText(client_info["Name"])
        self.IpLabel.setText(client_info['ComputerIP'])
        self.MacLabel.setText(client_info['ComputerMAC'])
        self.LoginUserLabel.setText(client_info['LoginUserName'])
        self.ClientNameLabel.setText(client_info['ComputerName'])

    def send_insert_to_worker(self):
        new_data = GetClientInfo.get_system_info()
        if self.compare_and_save_state(new_data):
            insert_sentence = """
            MERGE INTO ComputerList AS target
            USING (
                SELECT 
                    %s AS ComputerName,
                    %s AS Name,
                    %s AS LoginUserName,
                    %s AS ComputerMAC,
                    %s AS ComputerIP,
                    %s AS StartTime
            ) AS source
            ON target.ComputerName = source.ComputerName AND target.Name = source.Name
            WHEN MATCHED THEN
                UPDATE SET
                    target.LoginUserName = source.LoginUserName,
                    target.ComputerMAC = source.ComputerMAC,
                    target.ComputerIP = source.ComputerIP,
                    target.StartTime = source.StartTime
            WHEN NOT MATCHED THEN
                INSERT (ComputerName, Name, LoginUserName, ComputerMAC, ComputerIP, StartTime)
                VALUES (
                    source.ComputerName,
                    source.Name,
                    source.LoginUserName,
                    source.ComputerMAC,
                    source.ComputerIP,
                    source.StartTime
                );
            """
            params = [
                new_data['ComputerName'],
                new_data['Name'],
                new_data['LoginUserName'],
                new_data['ComputerMAC'],
                new_data['ComputerIP'],
                new_data['StartTime']
            ]
            self.db_worker.send_insert(insert_sentence, params)

    def compare_and_save_state(self, new_data):
        path = Path(".\\client_info.json")

        if not path.exists():
            # 文件不存在，创建并写入
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            return True

        # 文件存在，读取旧数据
        with open(path, 'r', encoding='utf-8') as f:
            try:
                old_data = json.load(f)
            except json.JSONDecodeError:
                # 如果文件内容不是合法的 json（如空文件），可以选择覆盖
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=4)
                return True

        # 比较两个 json 数据是否相同
        temp_new = new_data.copy()
        old_data.pop("StartTime", None)
        temp_new.pop("StartTime", None)

        if old_data == temp_new:
            return False
        else:
            # 不相同，更新文件
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            return True

    def send_query_to_worker(self):
        query_str = [self.lineEdit.text()] * 7
        if query_str[0]:
            query_sentence = ("SELECT Name, LoginUserName, ComputerName, ComputerIP, "
                              "ComputerMAC, StartTime, Tab FROM ComputerList "
                              f"WHERE Name LIKE %s or LoginUserName LIKE %s "
                              f"or ComputerName LIKE %s or ComputerIP LIKE %s "
                              f"or ComputerMAC LIKE %s or StartTime LIKE %s or Tab LIKE %s")
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
        self.statusbar.showMessage(f"{msg}")


if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
