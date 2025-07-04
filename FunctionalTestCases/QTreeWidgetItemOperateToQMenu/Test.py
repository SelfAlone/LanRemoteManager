import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt


class CustomTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)  # 单列
        self.setHeaderHidden(True)  # 隐藏表头

        # 设置右键菜单策略
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # 示例数据（可选）
        root = QTreeWidgetItem(self)
        root.setText(0, "根节点")
        child = QTreeWidgetItem(root)
        child.setText(0, "子节点")

    def show_context_menu(self, position):
        """右键菜单"""
        menu = QMenu(self)

        # 获取点击位置的项目
        item = self.itemAt(position)

        # 新建项目
        new_action = QAction("新建项目", self)
        new_action.triggered.connect(lambda: self.add_item(item))

        # 删除项目
        delete_action = QAction("删除项目", self)
        delete_action.triggered.connect(lambda: self.delete_item(item))

        # 新建子项目
        new_child_action = QAction("新建子项目", self)
        new_child_action.triggered.connect(lambda: self.add_child_item(item))

        # 重命名项目
        rename_action = QAction("重命名", self)
        rename_action.triggered.connect(lambda: self.rename_item(item))

        # 根据点击位置动态决定菜单项
        if item:
            menu.addAction(rename_action)
            menu.addAction(new_child_action)
            menu.addAction(delete_action)
        else:
            menu.addAction(new_action)

        menu.exec(self.viewport().mapToGlobal(position))

    def add_item(self, parent=None):
        """新建项目"""
        item = QTreeWidgetItem()
        item.setText(0, "新项目")
        if parent:
            parent.addChild(item)
        else:
            self.addTopLevelItem(item)

    def add_child_item(self, parent):
        """在项目下新建子项目"""
        if parent:
            child = QTreeWidgetItem(parent)
            child.setText(0, "子项目")

    def delete_item(self, item):
        """删除项目及其所有子项"""
        if not item:
            return

        # 如果是顶层项目，从顶层删除
        if item.parent() is None:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
        else:
            parent = item.parent()
            parent.removeChild(item)

    def rename_item(self, item):
        """触发重命名"""
        if item:
            self.editItem(item)  # 触发编辑模式


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeWidget 示例")
        self.resize(300, 400)

        layout = QVBoxLayout(self)

        # 创建自定义 TreeWidget
        self.tree = CustomTreeWidget()
        layout.addWidget(self.tree)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
