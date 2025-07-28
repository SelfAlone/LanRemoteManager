import sys
import pymssql
import json
from pathlib import Path

from Func import GetClientInfo, ServiceInstallAndRun as Service
from qt_material import QtStyleTools, apply_stylesheet
from Ui.main_ui import Ui_MainWindow
from Ui.EditDialog_ui import Ui_EditDialog
from Ui.EditTreeWidgetItem_ui import Ui_Dialog
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem, QDialog, QMessageBox, \
    QListWidgetItem, QTreeWidgetItem, QMenu, QTreeWidget
from PySide6.QtCore import QTimer, QDateTime, Qt, QThread, Signal, Slot, QProcess
from PySide6.QtGui import QIcon, QFont, QAction, QFontDatabase


class DatabaseWorker(QThread):
    # 查询相关信号
    query_result = Signal(list)  # 查询结果
    query_error = Signal(str)  # 查询错误

    # 更新相关信号
    update_result = Signal(int)  # 更新成功，返回受影响行数
    update_error = Signal(str)  # 更新失败

    # 插入相关信号
    insert_result = Signal(int)
    insert_error = Signal(str)

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
                    server="192.168.248.236",
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
                        elif task_type == "insert":
                            self.connection.commit()
                            rows_affected = cursor.rowcount
                            if rows_affected == 0:
                                self.insert_error.emit("插入失败: 受影响的记录数为0")
                            else:
                                self.insert_result.emit(rows_affected)
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

        # 绑定按钮事件
        self.buttonBox.accepted.connect(self.send_update_to_worker)
        self.buttonBox.rejected.connect(self.close)

    def send_update_to_worker(self):
        """发送更新任务到数据库线程"""
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
        """获取当前记录信息"""
        name = self.clientRecordTable.item(self.clientRecordTable.currentRow(), 0).text()
        computer_name = self.clientRecordTable.item(self.clientRecordTable.currentRow(), 2).text()
        ip = self.clientRecordTable.item(self.clientRecordTable.currentRow(), 3).text()
        note = self.clientRecordTable.item(self.clientRecordTable.currentRow(), 6).text()
        return [name, computer_name, ip, note]

    def get_primary(self):
        """获取当前记录的主键信息"""
        return [self.clientRecordTable.item(self.clientRecordTable.currentRow(), 1).text(),
                self.clientRecordTable.item(self.clientRecordTable.currentRow(), 2).text()]

    def update_local_record(self, new_record):
        """更新当前记录"""
        self.clientRecordTable.item(self.clientRecordTable.currentRow(), 0).setText(new_record[0])
        self.clientRecordTable.item(self.clientRecordTable.currentRow(), 2).setText(new_record[1])
        self.clientRecordTable.item(self.clientRecordTable.currentRow(), 3).setText(new_record[2])
        self.clientRecordTable.item(self.clientRecordTable.currentRow(), 6).setText(new_record[3])


class EditTreeWidgetItemDialog(QDialog, Ui_Dialog):
    """编辑/更新树结构窗口"""

    def __init__(self, window_type, edit_type, tree_widget, item=None):  # edit_type类型为新增/修改
        super(EditTreeWidgetItemDialog, self).__init__()
        self.window_type = window_type  # 窗口类型
        self.treeWidget = tree_widget  # 树结构控件
        self.current_item = item  # 当前树结构项
        if window_type == "folder":
            self.setupEditFolderUi(self)
            if edit_type == "creat":
                self.buttonBox.accepted.connect(self.creat_folder_item)
                self.buttonBox.rejected.connect(self.close)
            else:  # 修改
                self.lineEdit.setText(item.text(0))
                self.buttonBox.accepted.connect(self.edit_folder_item)
                self.buttonBox.rejected.connect(self.close)
            return

        if window_type == "session":
            self.setupEditSessionUi(self)
            self.pushButton.clicked.connect(lambda: self.switch_page(0, self.stackedWidget.currentIndex()))
            self.pushButton_2.clicked.connect(lambda: self.switch_page(1, self.stackedWidget.currentIndex()))
            if edit_type == "creat":
                self.buttonBox.accepted.connect(self.creat_session_item)
                self.buttonBox.rejected.connect(self.close)
            elif item.attribute["type"] == "session_vnc":
                self.stackedWidget.setCurrentIndex(0)  # 切换到VNC页面
                self.lineEdit.setText(item.attribute["host"])
                self.lineEdit_2.setText(item.attribute["password"])
                self.spinBox.setValue(item.attribute["port"])

                self.buttonBox.accepted.connect(self.edit_session_item)
                self.buttonBox.rejected.connect(self.close)
            elif item.attribute["type"] == "session_rdp":
                pass
            return

    def creat_folder_item(self):
        """创建文件夹"""
        parent = self.current_item
        text = self.lineEdit.text()

        if not text:
            QMessageBox.information(self, "信息", "文件夹名不能为空!", QMessageBox.Ok)
            return

        item = SessionTreeItem("folder", text)

        # 添加子项
        if parent:  # 有父级
            parent.addChild(item)
        else:  # 无父级
            self.treeWidget.addTopLevelItem(item)

        self.save_treeWidget("Data/treeStructure.json", self.treeWidget)
        self.lineEdit.clear()

    def creat_session_item(self):
        """创建会话"""
        parent = self.current_item
        current_index = self.stackedWidget.currentIndex()
        item_attributes = {}

        if current_index == 0:  # StackWidget 0 VNC
            item_attributes["host"] = self.lineEdit.text().strip()
            item_attributes["password"] = self.lineEdit_2.text().strip()
            item_attributes["port"] = self.spinBox.value()
            item_attributes["type"] = self.stackedWidget.widget(current_index).objectName()
        if current_index == 1:  # StackWidget 1 RDP
            pass

        if not item_attributes["host"] or not item_attributes["password"]:
            QMessageBox.information(self, "信息", "请填写完整信息!", QMessageBox.Ok)
            return

        item = SessionTreeItem("session", item_attributes["host"], item_attributes)
        if parent:
            parent.addChild(item)
        else:
            self.treeWidget.addTopLevelItem(item)

        self.save_treeWidget("Data/treeStructure.json", self.treeWidget)
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def edit_folder_item(self):
        """修改文件夹"""
        item = self.current_item
        text = self.lineEdit.text()

        if not text:
            QMessageBox.information(self, "信息", "文件夹名不能为空!", QMessageBox.Ok)
            return

        if item.text(0) == text:
            QMessageBox.information(self, "信息", "未进行修改!", QMessageBox.Ok)
            return

        # 修改item属性并持久化存储
        item.setText(0, text)
        self.save_treeWidget("Data/treeStructure.json", self.treeWidget)
        self.close()

    def edit_session_item(self):
        """修改会话"""
        item = self.current_item
        item_attributes = {}
        current_index = self.stackedWidget.currentIndex()
        connect_type = item.attribute["type"]

        if connect_type == self.stackedWidget.widget(current_index).objectName():  # stackWidget 0 VNC
            item_attributes["host"] = self.lineEdit.text().strip()
            item_attributes["password"] = self.lineEdit_2.text().strip()
            item_attributes["port"] = self.spinBox.value()
            item_attributes["type"] = connect_type
        else:  # stackWidget 1 RDP
            pass

        if not item_attributes["host"] or not item_attributes["password"]:
            QMessageBox.information(self, "信息", "请填写完整信息!", QMessageBox.Ok)
            return

        if item_attributes == item.attribute:
            QMessageBox.information(self, "信息", "未进行修改!", QMessageBox.Ok)
            return

        # 修改item属性并持久化存储
        item.setText(0, item_attributes["host"])
        item.attribute = item_attributes
        self.save_treeWidget("Data/treeStructure.json", self.treeWidget)
        self.close()

    def switch_page(self, target_index, page_index):
        """切换页面"""
        if target_index != page_index:
            self.stackedWidget.setCurrentIndex(target_index)

    @classmethod
    def save_treeWidget(cls, file_path, treeWidget):
        """递归保存treeWidget结构"""

        def serialize_item(item):
            if item.get_item_type() == "folder":
                item_data = {
                    "text": item.text(0),
                    "type": item.get_item_type(),
                    "children": []
                }
            else:
                item_data = {
                    "text": item.text(0),
                    "type": item.get_item_type(),
                    "data": item.get_item_attribute()
                }
            for index in range(item.childCount()):
                child = item.child(index)
                item_data["children"].append(serialize_item(child))
            return item_data

        root_data = []
        for i in range(treeWidget.topLevelItemCount()):
            root = treeWidget.topLevelItem(i)
            root_data.append(serialize_item(root))

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(root_data, f, ensure_ascii=False, indent=2)


class FuncQLabel(QLabel):
    """QLabel的链接功能"""

    def __init__(self, table, db, his_list):
        super().__init__()
        self.ClientRecordTable = table
        self.db_worker = db
        self.listWidget = his_list
        self.setText(
            "<a href='Link'><font color=blue>连接</font></a> | <a href='Edit'><font color=blue>编辑</font></a>")
        self.setAlignment(Qt.AlignCenter)
        self.linkActivated.connect(self.click_link)

    def click_link(self, key):
        """调用UltraVNC外部程序"""
        full_name = self.ClientRecordTable.item(self.ClientRecordTable.currentRow(), 0).text()
        login_user_name = self.ClientRecordTable.item(self.ClientRecordTable.currentRow(), 1).text()
        computer_name = self.ClientRecordTable.item(self.ClientRecordTable.currentRow(), 2).text()
        ip = self.ClientRecordTable.item(self.ClientRecordTable.currentRow(), 3).text()

        attributes = {
            "full_name": full_name,
            "login_user_name": login_user_name,
            "computer_name": computer_name,
            "ip": ip,
        }

        if key == "Link":
            vnc_process = QProcess()
            vnc_path = r".\x64\vncviewer.exe"
            args = [
                f"{ip}",
                "-password",
                "111111"
            ]
            vnc_process.setProgram(vnc_path)
            vnc_process.setArguments(args)
            vnc_process.startDetached()

            if self.insert_history_record(attributes):  # 向历史列表添加连接记录
                self.save_listWidget()
            return
        if key == "Edit":
            edit_dialog = EditDialog(self.ClientRecordTable, self.db_worker)  # 传入主窗口表格控件与数据库工作线程
            edit_dialog.exec()
            return

    def insert_history_record(self, item_attributes):
        """插入历史列表"""
        if self.item_exists(item_attributes):
            return False

        if self.listWidget.count() < 16:
            self.listWidget.insertItem(0, HisListWidgetItem(item_attributes))
            return True

        if self.listWidget.count() == 16:
            self.listWidget.insertItem(0, HisListWidgetItem(item_attributes))
            last_item = self.listWidget.takeItem(self.listWidget.count() - 1)  # 移除历史连接记录列表最后一行
            del last_item  # 显式删除
            return True

    def item_exists(self, attributes):
        """判断历史列表中是否存在该连接记录"""
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.attributes == attributes:
                return True
        return False

    def save_listWidget(self):
        """保存历史列表结构"""
        attributes_list = []
        with open("Data/listStructure.json", "w", encoding="utf-8") as f:
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                attributes_list.append(item.attributes)
            json.dump(attributes_list, f, ensure_ascii=False, indent=2)


class HisListWidgetItem(QListWidgetItem):
    """历史列表项"""

    def __init__(self, attributes):
        super().__init__()
        self.attributes = attributes
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.Computer))
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setIcon(icon)
        self.setText(self.attributes["ip"])
        self.setToolTip(
            f"Host: \t{self.attributes['ip']}\n"
            f"User: \t{self.attributes['login_user_name']}\n"
            f"Computer: {self.attributes['computer_name']}"
        )  # 提示信息


class SessionTreeItem(QTreeWidgetItem):
    """树结构项"""

    def __init__(self, item_type, text, item_attribute=None):
        super().__init__()
        self.item_type = item_type
        if item_type == "folder":
            icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
            self.setIcon(0, icon)
            self.setText(0, text)
            return
        if item_type == "session":
            icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.InsertLink))
            self.attribute = item_attribute
            self.setIcon(0, icon)
            self.setText(0, text)
            self.setToolTip(0,
                            f"Host: \t{item_attribute['host']}\n"
                            f"Port: \t{item_attribute['port']}\n"
                            f"Type: \t{item_attribute['type']}")  # 提示信息
            return

    def get_item_type(self):
        return self.item_type

    def get_item_attribute(self):
        return self.attribute


class TreeWidgetContextMenu(QMenu):
    def __init__(self, item, tree_widget):
        super().__init__()
        self.treeWidget = tree_widget

        # 根据传入的item类型，生成菜单
        if item is None:
            new_folder = QAction(QIcon.fromTheme("folder-new"), "新建文件夹", self)
            new_folder.triggered.connect(lambda: self.create_new_folder(item))

            new_session = QAction(QIcon.fromTheme("list-add"), "新建会话", self)
            new_session.triggered.connect(lambda: self.create_new_session(item))
            self.addAction(new_folder)
            self.addAction(new_session)
            return

        if hasattr(item, 'get_item_type'):
            item_type = item.get_item_type()

            if item_type == "folder":
                new_folder = QAction(QIcon.fromTheme("folder-new"), "新建文件夹", self)
                new_folder.triggered.connect(lambda: self.create_new_folder(item))

                new_session = QAction(QIcon.fromTheme("list-add"), "新建会话", self)
                new_session.triggered.connect(lambda: self.create_new_session(item))

                edit_folder = QAction(QIcon.fromTheme("edit-redo"), "编辑会话夹", self)
                edit_folder.triggered.connect(lambda: self.edit_folder(item))

                delete_folder = QAction(QIcon.fromTheme("edit-delete"), "删除会话夹", self)
                delete_folder.triggered.connect(lambda: self.delete_item(item))

                self.addAction(new_folder)
                self.addAction(new_session)
                self.addAction(edit_folder)
                self.addAction(delete_folder)
                return

            if item_type == "session":
                edit_session = QAction(QIcon.fromTheme("edit-redo"), "编辑会话", self)
                edit_session.triggered.connect(lambda: self.edit_session(item))

                delete_session = QAction(QIcon.fromTheme("edit-delete"), "删除会话", self)
                delete_session.triggered.connect(lambda: self.delete_item(item))

                self.addAction(edit_session)
                self.addAction(delete_session)
                return

        # 默认情况（如未知类型）
        default_action = QAction("默认操作", self)
        self.addAction(default_action)

    def create_new_folder(self, parent=None):
        edit_dialog = EditTreeWidgetItemDialog("folder", "creat", self.treeWidget, parent)
        edit_dialog.exec()
        return

    def create_new_session(self, parent=None):
        edit_dialog = EditTreeWidgetItemDialog("session", "creat", self.treeWidget, parent)
        edit_dialog.exec()
        return

    def edit_folder(self, item):
        edit_dialog = EditTreeWidgetItemDialog("folder", "edit", self.treeWidget, item)
        edit_dialog.exec()
        return

    def delete_item(self, item):
        """删除项目及其所有子项"""
        if not item:
            return

        # 如果是顶层项目，从顶层删除
        if item.parent() is None:
            index = self.treeWidget.indexOfTopLevelItem(item)
            self.treeWidget.takeTopLevelItem(index)
        else:
            parent = item.parent()
            parent.removeChild(item)

        EditTreeWidgetItemDialog.save_treeWidget("Data/treeStructure.json", self.treeWidget)

    def edit_session(self, item):
        edit_dialog = EditTreeWidgetItemDialog("session", "edit", self.treeWidget, item)
        edit_dialog.exec()
        return


class MainWindow(QMainWindow, Ui_MainWindow, QtStyleTools):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.load_treeWidget("Data/treeStructure.json")
        self.load_listWidget("Data/listStructure.json")
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

        # 信号绑定
        self.treeWidget.customContextMenuRequested.connect(self.show_context_menu)  # 绑定treeWidget控件右键菜单
        # self.treeWidget_2.customContextMenuRequested.connect(self.show_context_menu)
        self.actionNew.triggered.connect(
            lambda: EditTreeWidgetItemDialog("session", "creat", self.treeWidget).exec()
        )
        self.actionoff.triggered.connect(self.db_worker.stop)
        self.actionThemeSwitch.triggered.connect(self.switch_theme)
        self.LeftSearchEdit.textEdited.connect(self.switch_page)
        self.pushButton.clicked.connect(self.send_query_to_worker)
        self.lineEdit.returnPressed.connect(self.send_query_to_worker)
        self.listWidget.itemDoubleClicked.connect(self.item_double_clicked)
        self.treeWidget.itemDoubleClicked.connect(self.item_double_clicked)
        self.treeWidget_2.itemDoubleClicked.connect(self.item_double_clicked)

        # 使用 QTimer.singleShot 延迟启动线程，确保 UI 已渲染
        QTimer.singleShot(0, self.service_install)

    def switch_theme(self, checked):
        """切换主题"""
        if checked:
            icon = QIcon.fromTheme("weather-overcast")
            self.apply_stylesheet(self, theme="dark_blue.xml")
            self.actionThemeSwitch.setIcon(icon)
        else:
            icon = QIcon.fromTheme("weather-clear")
            self.apply_stylesheet(self, theme="light_blue.xml", invert_secondary=True)
            self.actionThemeSwitch.setIcon(icon)

    def closeEvent(self, event):
        """安全停止数据库服务线程"""
        self.db_worker.stop()

    def service_install(self):
        """安装UltraVNC服务 并确保通过防火墙"""
        self.service_worker = Worker(Service.main)
        self.service_worker.finished.connect(self.show_message)
        self.service_worker.error.connect(self.show_message)
        self.service_worker.start()

    def update_time(self):
        """获取当前时间并格式化"""
        current_time = QDateTime.currentDateTime()
        time_str = current_time.toString("yyyy-MM-dd HH:mm:ss")
        self.TimeLabel.setText(time_str)

    def display_client_info(self):
        """获取客户端信息"""
        client_info = GetClientInfo.get_system_info()
        self.FullNameLabel.setText(client_info["Name"])
        self.IpLabel.setText(client_info['ComputerIP'])
        self.MacLabel.setText(client_info['ComputerMAC'])
        self.LoginUserLabel.setText(client_info['LoginUserName'])
        self.ClientNameLabel.setText(client_info['ComputerName'])

    def switch_page(self, text):
        if not text:
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.stackedWidget.setCurrentIndex(1)
            result = self.find_items_in_treeWidget(self.treeWidget, text)
            self.left_search_result(result)

    @staticmethod
    def find_items_in_treeWidget(tree_widget, text, column=0, case_sensitive=False):
        """
            在 QTreeWidget 中查找显示文本包含指定文本的所有项。

            :param tree_widget: QTreeWidget 控件
            :param text: 要搜索的文本
            :param column: 检查的列号（默认为 0）
            :param case_sensitive: 是否区分大小写
        """
        matched_items = []

        def traverse_item(item):
            if item.item_type != "folder":
                # 获取当前项指定列的文本
                item_text = item.text(column)
                # 根据是否区分大小写进行匹配
                if case_sensitive:
                    contains = text in item_text
                else:
                    contains = text.lower() in item_text.lower()

                if contains:
                    matched_items.append(item)

            # 递归遍历所有子项
            for i in range(item.childCount()):
                child = item.child(i)
                traverse_item(child)

        # 从每个顶层项开始遍历
        for i in range(tree_widget.topLevelItemCount()):
            top_item = tree_widget.topLevelItem(i)
            traverse_item(top_item)

        return matched_items

    def left_search_result(self, result):
        """左侧搜索结果"""
        self.treeWidget_2.clear()
        for item in result:
            item_clone = SessionTreeItem(item.item_type, item.text(0), item.attribute)
            self.treeWidget_2.addTopLevelItem(item_clone)

    def send_insert_to_worker(self):
        """构造插入语句"""
        path = Path("Data/client_info.json")
        new_data = GetClientInfo.get_system_info()
        old_data = self.load_client_info(path)
        if self.compare_client_info(new_data, old_data):
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
            self.db_worker.insert_result.connect(lambda: self.save_client_info(path, new_data))
            # self.db_worker.insert_result.connect(lambda x: QMessageBox.information(self, '提示', f"成功插入{x}条数据"))

    def send_query_to_worker(self):
        """构造查询语句"""
        query_str = [self.lineEdit.text()] * 7
        if query_str[0]:
            query_sentence = ("SELECT Name, LoginUserName, ComputerName, ComputerIP, "
                              "ComputerMAC, StartTime, Tab FROM ComputerList "
                              f"WHERE Name LIKE %s OR LoginUserName LIKE %s "
                              f"OR ComputerName LIKE %s OR ComputerIP LIKE %s "
                              f"OR ComputerMAC LIKE %s OR StartTime LIKE %s OR Tab LIKE %s")
            self.lineEdit.clear()
            self.db_worker.send_query(query_sentence, [f"%{s}%" for s in query_str])  # 添加通配符 % 实现模糊查询
        else:
            query_sentence = ("SELECT Name, LoginUserName, ComputerName, ComputerIP, "
                              "ComputerMAC, StartTime, Tab FROM ComputerList")
            self.db_worker.send_query(query_sentence)

    @staticmethod
    def compare_client_info(new_data, old_data):
        """比较当前计算机信息与历史记录是否相同"""
        if old_data:
            return True

        # 比较两个 json 数据是否相同
        if old_data == new_data:
            return False
        else:
            return True

    @staticmethod
    def load_client_info(path):
        """读取客户端信息文件"""
        if not path.exists():
            # 文件不存在，创建文件返回空字典
            with open(path, 'w', encoding='utf-8'):
                return {}

        # 文件存在，读取旧数据
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                # 如果文件内容不是合法的 json（如空文件），可以选择覆盖
                with open(path, 'w', encoding='utf-8'):
                    return {}

    @staticmethod
    def save_client_info(path, client_info):
        """保存客户端信息"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(client_info, f, ensure_ascii=False, indent=4)

    def load_treeWidget(self, file_path):
        """从文件递归加载树结构"""

        def deserialize_item(parent, item_data):
            if item_data["type"] == "folder":
                item_text = item_data["text"]
                item_type = item_data["type"]
                item = SessionTreeItem(item_type, item_text)

                if isinstance(parent, QTreeWidget):
                    parent.addTopLevelItem(item)
                else:
                    parent.addChild(item)

                for child_data in item_data.get("children", []):
                    deserialize_item(item, child_data)

            if item_data["type"] == "session":
                item_text = item_data["text"]
                item_type = item_data["type"]
                item_data = item_data["data"]
                item = SessionTreeItem(item_type, item_text, item_data)

                if isinstance(parent, QTreeWidget):
                    parent.addTopLevelItem(item)
                else:
                    parent.addChild(item)

        self.treeWidget.clear()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for root_data in data:
                deserialize_item(self.treeWidget, root_data)
        except FileNotFoundError:
            pass

    def load_listWidget(self, file_path):
        """从文件加载列表结构"""
        self.listWidget.clear()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for index, item_attribute in enumerate(data):
                self.listWidget.insertItem(index, HisListWidgetItem(item_attribute))
        except FileNotFoundError:
            pass

    def update_table(self, results):
        """更新表格数据"""
        self.ClientRecordTable.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                self.ClientRecordTable.setItem(row, col, QTableWidgetItem(value))
            self.ClientRecordTable.setCellWidget(row, 7,
                                                 FuncQLabel(self.ClientRecordTable, self.db_worker,
                                                            self.listWidget))  # 添加自定义控件
        self.ClientRecordTable.resizeColumnsToContents()  # 根据内容自适应列宽

    @staticmethod
    def item_double_clicked(item):
        """双击列表项或树项时，启动 VNC 终端"""
        vnc_process = QProcess()
        vnc_path = r".\x64\vncviewer.exe"
        args = []

        if isinstance(item, HisListWidgetItem):
            ip = item.attributes["ip"]
            args = [
                f"{ip}",
                "-password",
                "111111"
            ]
        if isinstance(item, SessionTreeItem):
            if item.item_type == "folder":
                return

            host = item.attribute["host"] + ":" + str(item.attribute["port"])
            password = item.attribute["password"]
            args = [
                f"{host}",
                "-password",
                f"{password}"
            ]

        vnc_process.setProgram(vnc_path)
        vnc_process.setArguments(args)
        vnc_process.startDetached()

    def show_context_menu(self, item_point):
        """treeWidget右键菜单"""
        item = self.treeWidget.itemAt(item_point)
        menu = TreeWidgetContextMenu(item, self.treeWidget)
        menu.exec(self.treeWidget.viewport().mapToGlobal(item_point))
        # self.tree_context_menu.exec(QCursor.pos())  # 显示菜单

    def show_message(self, msg):
        self.statusbar.showMessage(f"{msg}")


def load_font(path):
    font_id = QFontDatabase.addApplicationFont(path)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    return font_family


if __name__ == '__main__':
    app = QApplication.instance()  # 获取当前正在运行的 QApplication 对象
    if app is None:
        app = QApplication(sys.argv)
        # global_font = load_font("Data/JetBrainsMono-Bold.ttf")
        # app.setFont(QFont(global_font))
    window = MainWindow()
    apply_stylesheet(app, theme="light_blue.xml", invert_secondary=True)  # 设置样式
    window.show()
    sys.exit(app.exec())
