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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSplitter,
    QStackedWidget, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QToolBar, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1018, 685)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        icon = QIcon(QIcon.fromTheme(u"document-open"))
        self.actionNew.setIcon(icon)
        self.actionNew.setMenuRole(QAction.MenuRole.NoRole)
        self.actionsetting = QAction(MainWindow)
        self.actionsetting.setObjectName(u"actionsetting")
        icon1 = QIcon(QIcon.fromTheme(u"document-properties"))
        self.actionsetting.setIcon(icon1)
        self.actionsetting.setMenuRole(QAction.MenuRole.NoRole)
        self.actionhelp = QAction(MainWindow)
        self.actionhelp.setObjectName(u"actionhelp")
        icon2 = QIcon(QIcon.fromTheme(u"help-browser"))
        self.actionhelp.setIcon(icon2)
        self.actionhelp.setMenuRole(QAction.MenuRole.NoRole)
        self.actionoff = QAction(MainWindow)
        self.actionoff.setObjectName(u"actionoff")
        icon3 = QIcon(QIcon.fromTheme(u"system-shutdown"))
        self.actionoff.setIcon(icon3)
        self.actionoff.setMenuRole(QAction.MenuRole.NoRole)
        self.actionping = QAction(MainWindow)
        self.actionping.setObjectName(u"actionping")
        icon4 = QIcon(QIcon.fromTheme(u"network-wired"))
        self.actionping.setIcon(icon4)
        self.actionping.setMenuRole(QAction.MenuRole.NoRole)
        self.actionThemeSwitch = QAction(MainWindow)
        self.actionThemeSwitch.setObjectName(u"actionThemeSwitch")
        self.actionThemeSwitch.setCheckable(True)
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WeatherClear))
        self.actionThemeSwitch.setIcon(icon5)
        self.actionThemeSwitch.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.LeftSearchEdit = QLineEdit(self.layoutWidget)
        self.LeftSearchEdit.setObjectName(u"LeftSearchEdit")

        self.verticalLayout.addWidget(self.LeftSearchEdit)

        self.line_8 = QFrame(self.layoutWidget)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_8)

        self.stackedWidget = QStackedWidget(self.layoutWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.stackedWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_9 = QVBoxLayout(self.page)
        self.verticalLayout_9.setSpacing(1)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(1, 1, 1, 1)
        self.tabWidget_2 = QTabWidget(self.page)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setTabPosition(QTabWidget.TabPosition.West)
        self.tabWidget_2.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget_2.setTabBarAutoHide(False)
        self.HistoryTab = QWidget()
        self.HistoryTab.setObjectName(u"HistoryTab")
        self.verticalLayout_2 = QVBoxLayout(self.HistoryTab)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.listWidget = QListWidget(self.HistoryTab)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMovement(QListView.Movement.Static)
        self.listWidget.setFlow(QListView.Flow.TopToBottom)
        self.listWidget.setLayoutMode(QListView.LayoutMode.SinglePass)
        self.listWidget.setSpacing(2)
        self.listWidget.setViewMode(QListView.ViewMode.ListMode)

        self.verticalLayout_2.addWidget(self.listWidget)

        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FormatJustifyLeft))
        self.tabWidget_2.addTab(self.HistoryTab, icon6, "")
        self.SessionTab = QWidget()
        self.SessionTab.setObjectName(u"SessionTab")
        self.verticalLayout_3 = QVBoxLayout(self.SessionTab)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.treeWidget = QTreeWidget(self.SessionTab)
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setFont(0, font);
        __qtreewidgetitem.setIcon(0, icon7);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.treeWidget.setAutoExpandDelay(-1)

        self.verticalLayout_3.addWidget(self.treeWidget)

        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailSend))
        self.tabWidget_2.addTab(self.SessionTab, icon8, "")

        self.verticalLayout_9.addWidget(self.tabWidget_2)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_10 = QVBoxLayout(self.page_2)
        self.verticalLayout_10.setSpacing(1)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(1, 1, 1, 1)
        self.treeWidget_2 = QTreeWidget(self.page_2)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setFont(0, font);
        self.treeWidget_2.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_2.setObjectName(u"treeWidget_2")
        self.treeWidget_2.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeWidget_2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.treeWidget_2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.verticalLayout_10.addWidget(self.treeWidget_2)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.splitter.addWidget(self.layoutWidget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.HomeTab = QWidget()
        self.HomeTab.setObjectName(u"HomeTab")
        self.HomeTab.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.HomeTab)
        self.gridLayout.setSpacing(30)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.frame_4 = QFrame(self.HomeTab)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(300, 180))
        self.frame_4.setMaximumSize(QSize(400, 250))
        self.frame_4.setStyleSheet(u"background-color: rgb(117, 167, 255);\n"
"border-radius:10px;")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_11 = QLabel(self.frame_4)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_8.addWidget(self.label_11)

        self.line_6 = QFrame(self.frame_4)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_8.addWidget(self.line_6)

        self.ClientNameLabel = QLabel(self.frame_4)
        self.ClientNameLabel.setObjectName(u"ClientNameLabel")
        self.ClientNameLabel.setStyleSheet(u"font-size: 20px;\n"
"font-weight: bold;")
        self.ClientNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.ClientNameLabel)

        self.verticalLayout_8.setStretch(0, 3)
        self.verticalLayout_8.setStretch(2, 7)

        self.gridLayout.addWidget(self.frame_4, 3, 2, 1, 1)

        self.label_3 = QLabel(self.HomeTab)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 3, 1)

        self.frame = QFrame(self.HomeTab)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(300, 180))
        self.frame.setMaximumSize(QSize(400, 250))
        self.frame.setStyleSheet(u"background-color: rgb(117, 167, 255);\n"
"border-radius:10px;\n"
"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setTextFormat(Qt.TextFormat.AutoText)

        self.verticalLayout_5.addWidget(self.label_7)

        self.line_3 = QFrame(self.frame)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setStyleSheet(u"")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_3)

        self.IpLabel = QLabel(self.frame)
        self.IpLabel.setObjectName(u"IpLabel")
        self.IpLabel.setStyleSheet(u"font-size: 20px;\n"
"font-weight: bold;")
        self.IpLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.IpLabel)

        self.verticalLayout_5.setStretch(0, 3)
        self.verticalLayout_5.setStretch(2, 7)

        self.gridLayout.addWidget(self.frame, 2, 1, 1, 1)

        self.frame_2 = QFrame(self.HomeTab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(300, 180))
        self.frame_2.setMaximumSize(QSize(400, 250))
        self.frame_2.setStyleSheet(u"background-color: rgb(117, 167, 255);\n"
"border-radius: 10px;\n"
"")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_6.addWidget(self.label_9)

        self.line_4 = QFrame(self.frame_2)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_4)

        self.MacLabel = QLabel(self.frame_2)
        self.MacLabel.setObjectName(u"MacLabel")
        self.MacLabel.setStyleSheet(u"font-size: 20px;\n"
"font-weight: bold;")
        self.MacLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.MacLabel)

        self.verticalLayout_6.setStretch(0, 3)
        self.verticalLayout_6.setStretch(2, 7)

        self.gridLayout.addWidget(self.frame_2, 2, 2, 1, 1)

        self.frame_5 = QFrame(self.HomeTab)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 30))
        self.frame_5.setMaximumSize(QSize(16777215, 40))
        self.frame_5.setStyleSheet(u"background-color: rgb(117, 167, 255);\n"
"border-radius:6px;")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.FullNameLabel = QLabel(self.frame_5)
        self.FullNameLabel.setObjectName(u"FullNameLabel")
        self.FullNameLabel.setStyleSheet(u"font-size: 16px;\n"
"font-weight: bold;")
        self.FullNameLabel.setTextFormat(Qt.TextFormat.AutoText)

        self.horizontalLayout_3.addWidget(self.FullNameLabel)

        self.line = QFrame(self.frame_5)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.line_2 = QFrame(self.frame_5)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line_2)

        self.TimeLabel = QLabel(self.frame_5)
        self.TimeLabel.setObjectName(u"TimeLabel")
        self.TimeLabel.setStyleSheet(u"font-size: 16px;\n"
"font-weight: bold;")

        self.horizontalLayout_3.addWidget(self.TimeLabel)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(2, 8)
        self.horizontalLayout_3.setStretch(4, 1)

        self.gridLayout.addWidget(self.frame_5, 1, 1, 1, 2)

        self.frame_3 = QFrame(self.HomeTab)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(300, 180))
        self.frame_3.setMaximumSize(QSize(400, 250))
        self.frame_3.setStyleSheet(u"background-color: rgb(117, 167, 255);\n"
"border-radius:10px;")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_10 = QLabel(self.frame_3)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_7.addWidget(self.label_10)

        self.line_5 = QFrame(self.frame_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_5)

        self.LoginUserLabel = QLabel(self.frame_3)
        self.LoginUserLabel.setObjectName(u"LoginUserLabel")
        self.LoginUserLabel.setStyleSheet(u"font-size: 20px;\n"
"font-weight: bold;")
        self.LoginUserLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.LoginUserLabel)

        self.verticalLayout_7.setStretch(0, 3)
        self.verticalLayout_7.setStretch(2, 7)

        self.gridLayout.addWidget(self.frame_3, 3, 1, 1, 1)

        self.label_4 = QLabel(self.HomeTab)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 4)

        self.label_5 = QLabel(self.HomeTab)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 3, 3, 1)

        self.label_6 = QLabel(self.HomeTab)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 4)

        icon9 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome))
        self.tabWidget.addTab(self.HomeTab, icon9, "")
        self.SearchTab = QWidget()
        self.SearchTab.setObjectName(u"SearchTab")
        self.SearchTab.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.SearchTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.SearchTab)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(self.SearchTab)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 25))
        self.lineEdit.setMaximumSize(QSize(500, 16777215))
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.SearchTab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        self.pushButton.setMinimumSize(QSize(25, 25))
        self.pushButton.setMaximumSize(QSize(25, 25))
        icon10 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemSearch))
        self.pushButton.setIcon(icon10)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.label_2 = QLabel(self.SearchTab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.ClientRecordTable = QTableWidget(self.SearchTab)
        if (self.ClientRecordTable.columnCount() < 8):
            self.ClientRecordTable.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.ClientRecordTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.ClientRecordTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.ClientRecordTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.ClientRecordTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.ClientRecordTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.ClientRecordTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.ClientRecordTable.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.ClientRecordTable.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.ClientRecordTable.setObjectName(u"ClientRecordTable")
        self.ClientRecordTable.setAlternatingRowColors(True)
        self.ClientRecordTable.setRowCount(0)
        self.ClientRecordTable.horizontalHeader().setStretchLastSection(False)
        self.ClientRecordTable.verticalHeader().setVisible(False)
        self.ClientRecordTable.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_4.addWidget(self.ClientRecordTable)

        self.tabWidget.addTab(self.SearchTab, icon10, "")
        self.splitter.addWidget(self.tabWidget)

        self.horizontalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMovable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QToolBar(MainWindow)
        self.toolBar_2.setObjectName(u"toolBar_2")
        sizePolicy.setHeightForWidth(self.toolBar_2.sizePolicy().hasHeightForWidth())
        self.toolBar_2.setSizePolicy(sizePolicy)
        self.toolBar_2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.toolBar_2.setMovable(False)
        self.toolBar_2.setAllowedAreas(Qt.ToolBarArea.AllToolBarAreas)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_2)

        self.toolBar.addAction(self.actionNew)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionping)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionsetting)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionhelp)
        self.toolBar_2.addAction(self.actionoff)
        self.toolBar_2.addSeparator()
        self.toolBar_2.addAction(self.actionThemeSwitch)

        self.retranslateUi(MainWindow)
        self.actionoff.triggered.connect(MainWindow.close)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)
        self.listWidget.setCurrentRow(-1)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(tooltip)
        self.actionNew.setToolTip(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u4e34\u65f6\u4f1a\u8bdd", None))
#endif // QT_CONFIG(tooltip)
        self.actionsetting.setText(QCoreApplication.translate("MainWindow", u"setting", None))
#if QT_CONFIG(tooltip)
        self.actionsetting.setToolTip(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.actionhelp.setText(QCoreApplication.translate("MainWindow", u"help", None))
#if QT_CONFIG(tooltip)
        self.actionhelp.setToolTip(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
#endif // QT_CONFIG(tooltip)
        self.actionoff.setText(QCoreApplication.translate("MainWindow", u"off", None))
#if QT_CONFIG(tooltip)
        self.actionoff.setToolTip(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
#endif // QT_CONFIG(tooltip)
        self.actionping.setText(QCoreApplication.translate("MainWindow", u"ping", None))
#if QT_CONFIG(tooltip)
        self.actionping.setToolTip(QCoreApplication.translate("MainWindow", u"\u5728\u7ebf\u68c0\u6d4b", None))
#endif // QT_CONFIG(tooltip)
        self.actionThemeSwitch.setText(QCoreApplication.translate("MainWindow", u"ThemeSwitch", None))
#if QT_CONFIG(tooltip)
        self.actionThemeSwitch.setToolTip(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u5207\u6362", None))
#endif // QT_CONFIG(tooltip)
        self.LeftSearchEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22...", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.HistoryTab), QCoreApplication.translate("MainWindow", u"\u5386\u53f2", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u7528\u6237\u4f1a\u8bdd", None));
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.SessionTab), QCoreApplication.translate("MainWindow", u"\u4f1a\u8bdd", None))
        ___qtreewidgetitem1 = self.treeWidget_2.headerItem()
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u7ed3\u679c", None));
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">\u8ba1\u7b97\u673a\u540d</span></p></body></html>", None))
        self.ClientNameLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\"></span></p></body></html>", None))
        self.label_3.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">IP\u5730\u5740</span></p></body></html>", None))
        self.IpLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\"></span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">MAC\u5730\u5740</span></p></body></html>", None))
        self.MacLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\"></span></p></body></html>", None))
        self.FullNameLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\"></span></p></body></html>", None))
        self.label_8.setText("")
        self.TimeLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\"></span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">\u767b\u9646\u8d26\u53f7</span></p></body></html>", None))
        self.LoginUserLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\"></span></p></body></html>", None))
        self.label_4.setText("")
        self.label_5.setText("")
        self.label_6.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.HomeTab), QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.label.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8ba1\u7b97\u673a\u540d/IP\u5730\u5740/MAC\u5730\u5740/\u767b\u9646\u7528\u6237...", None))
        self.pushButton.setText("")
        self.label_2.setText("")
        ___qtablewidgetitem = self.ClientRecordTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u59d3\u540d", None));
        ___qtablewidgetitem1 = self.ClientRecordTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55\u540d", None));
        ___qtablewidgetitem2 = self.ClientRecordTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u8ba1\u7b97\u673a\u540d", None));
        ___qtablewidgetitem3 = self.ClientRecordTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"IP\u5730\u5740", None));
        ___qtablewidgetitem4 = self.ClientRecordTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"MAC\u5730\u5740", None));
        ___qtablewidgetitem5 = self.ClientRecordTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u6700\u8fd1\u767b\u9646\u65f6\u95f4", None));
        ___qtablewidgetitem6 = self.ClientRecordTable.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u5907\u6ce8", None));
        ___qtablewidgetitem7 = self.ClientRecordTable.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u529f\u80fd", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SearchTab), QCoreApplication.translate("MainWindow", u"\u641c\u7d22", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.toolBar_2.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar_2", None))
    # retranslateUi

