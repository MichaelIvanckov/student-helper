# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_uiWYycWA.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QDockWidget, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(903, 609)
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_line_edit = QLineEdit(self.centralwidget)
        self.search_line_edit.setObjectName(u"search_line_edit")

        self.horizontalLayout.addWidget(self.search_line_edit)

        self.search_button = QPushButton(self.centralwidget)
        self.search_button.setObjectName(u"search_button")

        self.horizontalLayout.addWidget(self.search_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.main_tabs = QTabWidget(self.centralwidget)
        self.main_tabs.setObjectName(u"main_tabs")
        self.main_tabs.setEnabled(True)
        self.main_tabs.setAutoFillBackground(False)
        self.main_tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.main_tabs.setTabShape(QTabWidget.TabShape.Rounded)
        self.main_tabs.setDocumentMode(False)
        self.main_tabs.setTabsClosable(True)
        self.main_tabs.setMovable(True)
        self.main_tabs.setTabBarAutoHide(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_2 = QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 445, 591))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setTabletTracking(False)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)

        self.verticalLayout_6.addWidget(self.label)

        self.verticalSpacer_3 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.create_entry_button = QPushButton(self.scrollAreaWidgetContents)
        self.create_entry_button.setObjectName(u"create_entry_button")

        self.horizontalLayout_3.addWidget(self.create_entry_button)

        self.create_section_button = QPushButton(self.scrollAreaWidgetContents)
        self.create_section_button.setObjectName(u"create_section_button")

        self.horizontalLayout_3.addWidget(self.create_section_button)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_4 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)

        self.load_photo_by_exif_button = QPushButton(self.scrollAreaWidgetContents)
        self.load_photo_by_exif_button.setObjectName(u"load_photo_by_exif_button")

        self.verticalLayout_6.addWidget(self.load_photo_by_exif_button)

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(150)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
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


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.main_tabs.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.main_tabs.addTab(self.tab_2, "")

        self.verticalLayout_3.addWidget(self.main_tabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 903, 33))
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menuBar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.hierarchy_dock = QDockWidget(MainWindow)
        self.hierarchy_dock.setObjectName(u"hierarchy_dock")
        self.hierarchy_dock.setFloating(False)
        self.dockWidgetContents_6 = QWidget()
        self.dockWidgetContents_6.setObjectName(u"dockWidgetContents_6")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.sections_tree = QTreeWidget(self.dockWidgetContents_6)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"\u0420\u0430\u0437\u0434\u0435\u043b\u044b")
        self.sections_tree.setHeaderItem(__qtreewidgetitem)
        self.sections_tree.setObjectName(u"sections_tree")

        self.verticalLayout_2.addWidget(self.sections_tree)

        self.hierarchy_dock.setWidget(self.dockWidgetContents_6)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.hierarchy_dock)
        self.properties_dock = QDockWidget(MainWindow)
        self.properties_dock.setObjectName(u"properties_dock")
        self.dockWidgetContents_7 = QWidget()
        self.dockWidgetContents_7.setObjectName(u"dockWidgetContents_7")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_7)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.dockWidgetContents_7)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_8.addWidget(self.label_2)

        self.textBrowser = QTextBrowser(self.frame)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_8.addWidget(self.textBrowser)


        self.verticalLayout.addWidget(self.frame)

        self.properties_dock.setWidget(self.dockWidgetContents_7)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)

        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)

        self.main_tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
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
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.hierarchy_dock.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0418\u0435\u0440\u0430\u0440\u0445\u0438\u044f \u0431\u0430\u0437\u044b \u0437\u043d\u0430\u043d\u0438\u0439", None))
        self.properties_dock.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0421\u0432\u0439\u0441\u0442\u0432\u0430", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041e \u0437\u0430\u043f\u0438\u0441\u0438:", None))
    # retranslateUi

