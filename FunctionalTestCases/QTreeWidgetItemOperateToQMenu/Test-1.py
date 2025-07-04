import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QMenu
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QAction

class CustomTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, *args, item_type="folder", **kwargs):
        super().__init__(*args, **kwargs)
        self._item_type = item_type

    def get_item_type(self):
        return self._item_type

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeWidget 右键菜单示例")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setColumnCount(1)

        # 设置右键菜单策略
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.show_context_menu)

        # 添加示例数据
        root = CustomTreeWidgetItem(self.treeWidget, item_type="folder")
        root.setText(0, "根文件夹")

        child = CustomTreeWidgetItem(root, item_type="session")
        child.setText(0, "会话 1")

        layout.addWidget(self.treeWidget)
        self.setLayout(layout)

    def show_context_menu(self, item_point):
        item = self.treeWidget.itemAt(item_point)
        menu = ListWidgetContextMenu(item, self.treeWidget)
        menu.exec(self.treeWidget.viewport().mapToGlobal(item_point))

class ListWidgetContextMenu(QMenu):
    def __init__(self, item, father_tree):
        super().__init__(father_tree)
        font = QFont()
        font.setPointSize(10)

        if item is None:
            new_folder = QAction(QIcon.fromTheme("folder-new"), "新建文件夹", self)
            new_folder.setFont(font)
            new_session = QAction(QIcon.fromTheme("list-add"), "新建会话", self)
            self.addAction(new_folder)
            self.addAction(new_session)
            return

        if hasattr(item, 'get_item_type'):
            item_type = item.get_item_type()

            if item_type == "folder":
                new_folder = QAction(QIcon.fromTheme("folder-new"), "新建文件夹", self)
                new_session = QAction(QIcon.fromTheme("list-add"), "新建会话", self)
                edit_folder = QAction(QIcon.fromTheme("document-edit"), "编辑会话夹", self)
                delete_folder = QAction(QIcon.fromTheme("edit-delete"), "删除会话夹", self)
                self.addAction(new_folder)
                self.addAction(new_session)
                self.addAction(edit_folder)
                self.addAction(delete_folder)
                return

            if item_type == "session":
                rename_session = QAction(QIcon.fromTheme("document-edit"), "重命名会话", self)
                edit_session = QAction(QIcon.fromTheme("document-edit"), "编辑会话", self)
                delete_session = QAction(QIcon.fromTheme("edit-delete"), "删除会话", self)
                self.addAction(rename_session)
                self.addAction(edit_session)
                self.addAction(delete_session)
                return

        # 默认情况（如未知类型）
        default_action = QAction("默认操作", self)
        self.addAction(default_action)

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
