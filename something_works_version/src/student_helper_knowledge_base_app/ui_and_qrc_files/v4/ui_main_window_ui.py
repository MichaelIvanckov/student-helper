# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_uibXXBrH.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QFrame, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSplitter, QStatusBar, QTabWidget,
    QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1011, 653)
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.action_3 = QAction(MainWindow)
        self.action_3.setObjectName(u"action_3")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_9 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(40, 40))
        self.pushButton.setMaximumSize(QSize(30, 16777215))
        font = QFont()
        font.setPointSize(17)
        self.pushButton.setFont(font)

        self.horizontalLayout.addWidget(self.pushButton)

        self.search_line_edit = QLineEdit(self.centralwidget)
        self.search_line_edit.setObjectName(u"search_line_edit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_line_edit.sizePolicy().hasHeightForWidth())
        self.search_line_edit.setSizePolicy(sizePolicy)
        self.search_line_edit.setMinimumSize(QSize(0, 40))
        self.search_line_edit.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(12)
        self.search_line_edit.setFont(font1)
        self.search_line_edit.setFrame(True)

        self.horizontalLayout.addWidget(self.search_line_edit)

        self.search_button = QPushButton(self.centralwidget)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setMinimumSize(QSize(0, 40))
        self.search_button.setFont(font1)

        self.horizontalLayout.addWidget(self.search_button)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setMinimumSize(QSize(590, 0))
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.treeWidget = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1")
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(50)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy2)
        self.treeWidget.setMinimumSize(QSize(60, 0))
        self.splitter.addWidget(self.treeWidget)
        self.main_tabs = QTabWidget(self.splitter)
        self.main_tabs.setObjectName(u"main_tabs")
        self.main_tabs.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(200)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.main_tabs.sizePolicy().hasHeightForWidth())
        self.main_tabs.setSizePolicy(sizePolicy3)
        self.main_tabs.setBaseSize(QSize(500, 0))
        self.main_tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.main_tabs.setAutoFillBackground(False)
        self.main_tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.main_tabs.setTabShape(QTabWidget.TabShape.Rounded)
        self.main_tabs.setDocumentMode(False)
        self.main_tabs.setTabsClosable(True)
        self.main_tabs.setMovable(True)
        self.main_tabs.setTabBarAutoHide(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_10 = QVBoxLayout(self.tab)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 701, 631))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setPointSize(21)
        font2.setWeight(QFont.Thin)
        font2.setItalic(False)
        font2.setKerning(True)
        self.label.setFont(font2)
        self.label.setTabletTracking(False)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)

        self.verticalLayout_6.addWidget(self.label)

        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(0, 10, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.create_entry_button = QPushButton(self.frame)
        self.create_entry_button.setObjectName(u"create_entry_button")
        self.create_entry_button.setMinimumSize(QSize(0, 40))
        font3 = QFont()
        font3.setPointSize(15)
        font3.setBold(False)
        self.create_entry_button.setFont(font3)
        self.create_entry_button.setCheckable(False)

        self.horizontalLayout_3.addWidget(self.create_entry_button)

        self.horizontalSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.create_section_button = QPushButton(self.frame)
        self.create_section_button.setObjectName(u"create_section_button")
        self.create_section_button.setMinimumSize(QSize(0, 40))
        font4 = QFont()
        font4.setPointSize(15)
        self.create_section_button.setFont(font4)

        self.horizontalLayout_3.addWidget(self.create_section_button)

        self.horizontalSpacer_3 = QSpacerItem(0, 10, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addWidget(self.frame)

        self.frame1 = QFrame(self.scrollAreaWidgetContents)
        self.frame1.setObjectName(u"frame1")
        self.horizontalLayout_2 = QHBoxLayout(self.frame1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.load_photo_by_exif_button = QPushButton(self.frame1)
        self.load_photo_by_exif_button.setObjectName(u"load_photo_by_exif_button")
        self.load_photo_by_exif_button.setMinimumSize(QSize(0, 40))
        self.load_photo_by_exif_button.setFont(font4)

        self.horizontalLayout_2.addWidget(self.load_photo_by_exif_button)


        self.verticalLayout_6.addWidget(self.frame1)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(150)
        sizePolicy5.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy5)
        self.verticalLayout_7 = QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.last_opened_list = QListWidget(self.groupBox)
        self.last_opened_list.setObjectName(u"last_opened_list")
        self.last_opened_list.setFrameShadow(QFrame.Shadow.Sunken)
        self.last_opened_list.setSortingEnabled(True)

        self.verticalLayout_5.addWidget(self.last_opened_list)


        self.verticalLayout_7.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.verticalSpacer_5 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)

        self.calendar = QCalendarWidget(self.scrollAreaWidgetContents)
        self.calendar.setObjectName(u"calendar")

        self.verticalLayout_6.addWidget(self.calendar)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)


        self.verticalLayout_10.addLayout(self.verticalLayout_4)

        self.main_tabs.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.main_tabs.addTab(self.tab_2, "")
        self.splitter.addWidget(self.main_tabs)
        self.frame_2 = QFrame(self.splitter)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(50)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy6)
        self.frame_2.setMinimumSize(QSize(60, 0))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.textBrowser_2 = QTextBrowser(self.frame_2)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.verticalLayout_3.addWidget(self.textBrowser_2)

        self.splitter.addWidget(self.frame_2)

        self.verticalLayout_9.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1011, 33))
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menuBar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu_2.addAction(self.action)

        self.retranslateUi(MainWindow)

        self.main_tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043c\u043e\u0449\u043d\u0438\u043a \u0441\u0442\u0443\u0434\u0435\u043d\u0442\u0430", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0431\u0430\u0437\u0443", None))
        self.action_3.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0432\u0430\u043b\u0438\u0442\u044c \u0431\u0430\u0437\u044b", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u2630", None))
        self.search_line_edit.setInputMask("")
        self.search_line_edit.setText("")
        self.search_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u0442\u0435\u043a\u0441\u0442\u0443 \u0437\u0430\u043c\u0435\u0442\u043a\u0438 \u0432 \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.search_button.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0439\u0442\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u041d\u0430\u0447\u0430\u043b\u043e \u0440\u0430\u0431\u043e\u0442\u044b</span></p></body></html>", None))
        self.create_entry_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.create_section_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0440\u0430\u0437\u0434\u0435\u043b", None))
        self.load_photo_by_exif_button.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0444\u043e\u0442\u043e \u043f\u043e EXIF", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0435 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041e \u0437\u0430\u043f\u0438\u0441\u0438:", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
    # retranslateUi

