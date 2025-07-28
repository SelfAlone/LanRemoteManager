# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EditDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_EditDialog(object):
    def setupUi(self, EditDialog):
        if not EditDialog.objectName():
            EditDialog.setObjectName(u"EditDialog")
        EditDialog.resize(400, 300)
        EditDialog.setMinimumSize(QSize(400, 300))
        EditDialog.setMaximumSize(QSize(400, 300))
        EditDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(EditDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(EditDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.NameEdit = QLineEdit(self.groupBox)
        self.NameEdit.setObjectName(u"NameEdit")
        self.NameEdit.setMaximumSize(QSize(200, 16777215))
        self.NameEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.NameEdit, 0, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.ComputerEdit = QLineEdit(self.groupBox)
        self.ComputerEdit.setObjectName(u"ComputerEdit")
        self.ComputerEdit.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.ComputerEdit, 1, 1, 1, 1)

        self.noteEdit = QTextEdit(self.groupBox)
        self.noteEdit.setObjectName(u"noteEdit")

        self.gridLayout.addWidget(self.noteEdit, 3, 1, 1, 1)

        self.IPEdit = QLineEdit(self.groupBox)
        self.IPEdit.setObjectName(u"IPEdit")
        self.IPEdit.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.IPEdit, 2, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(EditDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.label_2.setBuddy(self.ComputerEdit)
        self.label_4.setBuddy(self.noteEdit)
        self.label_3.setBuddy(self.IPEdit)
        self.label.setBuddy(self.NameEdit)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.NameEdit, self.ComputerEdit)
        QWidget.setTabOrder(self.ComputerEdit, self.IPEdit)
        QWidget.setTabOrder(self.IPEdit, self.noteEdit)

        self.retranslateUi(EditDialog)

        QMetaObject.connectSlotsByName(EditDialog)
    # setupUi

    def retranslateUi(self, EditDialog):
        EditDialog.setWindowTitle(QCoreApplication.translate("EditDialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("EditDialog", u"\u7ec8\u7aef\u4fe1\u606f\u7f16\u8f91", None))
        self.label_2.setText(QCoreApplication.translate("EditDialog", u"\u8ba1\u7b97\u673a\u540d", None))
        self.label_4.setText(QCoreApplication.translate("EditDialog", u"<html><head/><body><p align=\"center\">\u5907\u6ce8</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("EditDialog", u"<html><head/><body><p align=\"center\">IP\u5730\u5740</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("EditDialog", u"<html><head/><body><p align=\"center\">\u59d3\u540d</p></body></html>", None))
    # retranslateUi

