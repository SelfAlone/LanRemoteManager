import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem,
    QPushButton, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt

def save_tree_widget(tree, file_path):
    def serialize_item(item):
        item_data = {
            "text": item.text(0),
            "data": item.data(0, Qt.UserRole) or {},
            "children": []
        }
        for i in range(item.childCount()):
            child = item.child(i)
            item_data["children"].append(serialize_item(child))
        return item_data

    root_data = []
    for i in range(tree.topLevelItemCount()):
        root = tree.topLevelItem(i)
        root_data.append(serialize_item(root))

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(root_data, f, ensure_ascii=False, indent=2)

def load_tree_widget(tree, file_path):
    def deserialize_item(parent, item_data):
        item = QTreeWidgetItem(parent)
        item.setText(0, item_data["text"])
        item.setData(0, Qt.UserRole, item_data["data"])

        if isinstance(item_data["data"], dict) and item_data["data"].get("expanded", False):
            tree.expandItem(item)

        for child_data in item_data.get("children", []):
            deserialize_item(item, child_data)

    tree.clear()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for root_data in data:
            deserialize_item(tree, root_data)
    except FileNotFoundError:
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeWidget 持久化示例")
        self.resize(400, 300)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setColumnCount(1)

        root = QTreeWidgetItem(self.tree)
        root.setText(0, "根目录")
        root.setData(0, Qt.UserRole, {"type": "folder", "expanded": True})

        child = QTreeWidgetItem(root)
        child.setText(0, "子节点")
        child.setData(0, Qt.UserRole, {"type": "file", "id": 1, "checked": True})
        child.setCheckState(0, Qt.Checked)

        self.tree.expandAll()

        save_btn = QPushButton("保存结构")
        save_btn.clicked.connect(lambda: save_tree_widget(self.tree, "tree.json"))

        load_btn = QPushButton("加载结构")
        load_btn.clicked.connect(lambda: load_tree_widget(self.tree, "tree.json"))

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(save_btn)
        layout.addWidget(load_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())