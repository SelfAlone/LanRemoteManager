# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLayout, QMainWindow, QSizePolicy, QStatusBar,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(905, 566)
        MainWindow.setMinimumSize(QSize(905, 566))
        MainWindow.setMaximumSize(QSize(905, 566))
        self.search_action = QAction(MainWindow)
        self.search_action.setObjectName(u"search_action")
        icon = QIcon(QIcon.fromTheme(u"system-search"))
        self.search_action.setIcon(icon)
        self.search_action.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.link_action = QAction(MainWindow)
        self.link_action.setObjectName(u"link_action")
        icon1 = QIcon(QIcon.fromTheme(u"list-add"))
        self.link_action.setIcon(icon1)
        self.link_action.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.conf_action = QAction(MainWindow)
        self.conf_action.setObjectName(u"conf_action")
        icon2 = QIcon(QIcon.fromTheme(u"document-properties"))
        self.conf_action.setIcon(icon2)
        self.conf_action.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(40, 20, 831, 481))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.verticalLayoutWidget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(900, 50))
        self.frame_5.setStyleSheet(u"")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 91, 31))
        self.time = QLabel(self.frame_5)
        self.time.setObjectName(u"time")
        self.time.setGeometry(QRect(660, 10, 161, 31))
        self.time.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.frame_5)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.frame = QFrame(self.verticalLayoutWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayoutWidget_2 = QWidget(self.frame)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 10, 391, 191))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.verticalLayout_4.addWidget(self.label_3)

        self.line = QFrame(self.verticalLayoutWidget_2)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 0))
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(2)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_4.addWidget(self.line)

        self.ip_info = QLabel(self.verticalLayoutWidget_2)
        self.ip_info.setObjectName(u"ip_info")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(3)
        sizePolicy1.setHeightForWidth(self.ip_info.sizePolicy().hasHeightForWidth())
        self.ip_info.setSizePolicy(sizePolicy1)
        self.ip_info.setLineWidth(1)
        self.ip_info.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_4.addWidget(self.ip_info)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_2 = QFrame(self.verticalLayoutWidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayoutWidget_3 = QWidget(self.frame_2)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 10, 391, 191))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.verticalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.label_4)

        self.line_2 = QFrame(self.verticalLayoutWidget_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setMinimumSize(QSize(0, 0))
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setLineWidth(2)
        self.line_2.setMidLineWidth(0)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_5.addWidget(self.line_2)

        self.mac_info = QLabel(self.verticalLayoutWidget_3)
        self.mac_info.setObjectName(u"mac_info")
        sizePolicy1.setHeightForWidth(self.mac_info.sizePolicy().hasHeightForWidth())
        self.mac_info.setSizePolicy(sizePolicy1)
        self.mac_info.setLineWidth(1)
        self.mac_info.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_5.addWidget(self.mac_info)


        self.gridLayout.addWidget(self.frame_2, 1, 1, 1, 1)

        self.frame_3 = QFrame(self.verticalLayoutWidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayoutWidget_4 = QWidget(self.frame_3)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 10, 391, 191))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.verticalLayoutWidget_4)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.verticalLayout_6.addWidget(self.label_5)

        self.line_3 = QFrame(self.verticalLayoutWidget_4)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(0, 0))
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_3.setLineWidth(2)
        self.line_3.setMidLineWidth(0)
        self.line_3.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_6.addWidget(self.line_3)

        self.login_user = QLabel(self.verticalLayoutWidget_4)
        self.login_user.setObjectName(u"login_user")
        sizePolicy1.setHeightForWidth(self.login_user.sizePolicy().hasHeightForWidth())
        self.login_user.setSizePolicy(sizePolicy1)
        self.login_user.setLineWidth(1)
        self.login_user.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_6.addWidget(self.login_user)


        self.gridLayout.addWidget(self.frame_3, 3, 0, 1, 1)

        self.frame_4 = QFrame(self.verticalLayoutWidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayoutWidget_5 = QWidget(self.frame_4)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 10, 391, 191))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.verticalLayoutWidget_5)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.verticalLayout_7.addWidget(self.label_6)

        self.line_4 = QFrame(self.verticalLayoutWidget_5)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setMinimumSize(QSize(0, 0))
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_4.setLineWidth(2)
        self.line_4.setMidLineWidth(0)
        self.line_4.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_7.addWidget(self.line_4)

        self.pc_name = QLabel(self.verticalLayoutWidget_5)
        self.pc_name.setObjectName(u"pc_name")
        sizePolicy1.setHeightForWidth(self.pc_name.sizePolicy().hasHeightForWidth())
        self.pc_name.setSizePolicy(sizePolicy1)
        self.pc_name.setLineWidth(1)
        self.pc_name.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_7.addWidget(self.pc_name)


        self.gridLayout.addWidget(self.frame_4, 3, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.search_action)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.link_action)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.conf_action)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.search_action.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22", None))
#if QT_CONFIG(tooltip)
        self.search_action.setToolTip(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u4e3b\u673a", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.search_action.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+S", None))
#endif // QT_CONFIG(shortcut)
        self.link_action.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
#if QT_CONFIG(tooltip)
        self.link_action.setToolTip(QCoreApplication.translate("MainWindow", u"\u4e34\u65f6\u8fde\u63a5", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.link_action.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+N", None))
#endif // QT_CONFIG(shortcut)
        self.conf_action.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.conf_action.setToolTip(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.conf_action.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+P", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Eludi", None))
        self.time.setText(QCoreApplication.translate("MainWindow", u"2025\u5e741\u67081\u65e512:12:22", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"IP\u5730\u5740", None))
        self.ip_info.setText(QCoreApplication.translate("MainWindow", u"123323232", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"MAC\u5730\u5740", None))
        self.mac_info.setText(QCoreApplication.translate("MainWindow", u"123323232", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u767b\u9646\u7528\u6237", None))
        self.login_user.setText(QCoreApplication.translate("MainWindow", u"123323232", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u8ba1\u7b97\u673a\u540d", None))
        self.pc_name.setText(QCoreApplication.translate("MainWindow", u"123323232", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

