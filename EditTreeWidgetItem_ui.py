# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CreatNewFolder.ui'
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
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit, QGridLayout, QComboBox,
                               QSizePolicy, QVBoxLayout, QWidget, QToolButton, QFrame, QStackedWidget,
                               QLayout, QSpinBox)


class Ui_Dialog(object):
    def setupEditFolderUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 240)
        Dialog.setMinimumSize(QSize(320, 240))
        Dialog.setMaximumSize(QSize(320, 240))
        Dialog.setModal(True)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateEditFolderUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    def setupEditSessionUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(550, 450)
        Dialog.setMinimumSize(QSize(550, 450))
        Dialog.setMaximumSize(QSize(550, 450))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButton = QToolButton(Dialog)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setMinimumSize(QSize(0, 50))
        self.toolButton.setMaximumSize(QSize(50, 50))
        self.toolButton.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.toolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolButton.setAutoRaise(False)
        self.toolButton.setArrowType(Qt.ArrowType.NoArrow)

        self.horizontalLayout.addWidget(self.toolButton)

        self.toolButton_2 = QToolButton(Dialog)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setMinimumSize(QSize(0, 50))
        self.toolButton_2.setMaximumSize(QSize(50, 50))
        self.toolButton_2.setAutoRepeat(False)

        self.horizontalLayout.addWidget(self.toolButton_2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.Shape.Box)
        self.stackedWidget.setFrameShadow(QFrame.Shadow.Sunken)
        self.pagevnc = QWidget()
        self.pagevnc.setObjectName(u"session_vnc")
        self.verticalLayout_2 = QVBoxLayout(self.pagevnc)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.pagevnc)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(149, 0))
        self.lineEdit.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(149, 0))
        self.lineEdit_2.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 0, 2, 2, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(80, 0))
        self.spinBox.setMaximumSize(QSize(100, 16777215))
        self.spinBox.setMaximum(65535)
        self.spinBox.setValue(5900)

        self.gridLayout.addWidget(self.spinBox, 0, 4, 1, 1)

        self.gridLayout.setRowStretch(0, 5)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 6)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)

        self.verticalLayout_2.addWidget(self.groupBox, 0, Qt.AlignmentFlag.AlignLeft)

        self.groupBox_2 = QGroupBox(self.pagevnc)
        self.groupBox_2.setObjectName(u"groupBox_2")

        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(1, 6)
        self.stackedWidget.addWidget(self.pagevnc)
        self.pagerdp = QWidget()
        self.pagerdp.setObjectName(u"session_rdp")
        self.verticalLayout_3 = QVBoxLayout(self.pagerdp)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_3 = QGroupBox(self.pagerdp)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_4, 0, 3, 1, 1)

        self.lineEdit_3 = QLineEdit(self.groupBox_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(149, 0))
        self.lineEdit_3.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.lineEdit_3, 0, 1, 1, 1)

        self.lineEdit_4 = QLineEdit(self.groupBox_3)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(149, 0))
        self.lineEdit_4.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.lineEdit_4, 1, 1, 1, 1)

        self.line_3 = QFrame(self.groupBox_3)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 0, 2, 2, 1)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.spinBox_2 = QSpinBox(self.groupBox_3)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMinimumSize(QSize(80, 0))
        self.spinBox_2.setMaximumSize(QSize(100, 16777215))
        self.spinBox_2.setMaximum(65535)
        self.spinBox_2.setValue(3389)
        self.spinBox_2.setDisplayIntegerBase(10)

        self.gridLayout_2.addWidget(self.spinBox_2, 0, 4, 1, 1)

        self.gridLayout_2.setRowStretch(0, 5)
        self.gridLayout_2.setRowStretch(1, 5)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 6)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setColumnStretch(4, 1)

        self.verticalLayout_3.addWidget(self.groupBox_3, 0, Qt.AlignmentFlag.AlignLeft)

        self.groupBox_4 = QGroupBox(self.pagerdp)
        self.groupBox_4.setObjectName(u"groupBox_4")

        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.verticalLayout_3.setStretch(0, 4)
        self.verticalLayout_3.setStretch(1, 6)
        self.stackedWidget.addWidget(self.pagerdp)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateEditSessionUi(Dialog)

        self.stackedWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateEditFolderUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u65b0\u5efa\u6587\u4ef6\u5939", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"*\u6587\u4ef6\u5939\u540d", None))

    def retranslateEditSessionUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"VNC", None))
        self.toolButton_2.setText(QCoreApplication.translate("Dialog", u"RDP", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"VNC\u57fa\u7840\u8bbe\u7f6e", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"*\u7aef\u53e3\u53f7", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"*\u5bc6\u7801", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"*\u4e3b\u673a\u540d/IP", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"\u9ad8\u7ea7\u8bbe\u7f6e", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"RDP\u57fa\u7840\u8bbe\u7f6e", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"*\u7aef\u53e3\u53f7", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u7528\u6237\u540d", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"*\u4e3b\u673a\u540d/IP", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"\u9ad8\u7ea7\u8bbe\u7f6e", None))
