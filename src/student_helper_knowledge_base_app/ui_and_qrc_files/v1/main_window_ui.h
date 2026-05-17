/********************************************************************************
** Form generated from reading UI file 'main_window_ui.ui'
**
** Created by: Qt User Interface Compiler version 6.11.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef MAIN_WINDOW_UI_H
#define MAIN_WINDOW_UI_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCalendarWidget>
#include <QtWidgets/QDockWidget>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout_3;
    QHBoxLayout *horizontalLayout;
    QLineEdit *lineEdit;
    QPushButton *pushButton;
    QTabWidget *tabWidget;
    QWidget *tab;
    QHBoxLayout *horizontalLayout_2;
    QVBoxLayout *verticalLayout_4;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidgetContents;
    QVBoxLayout *verticalLayout_6;
    QSpacerItem *verticalSpacer;
    QLabel *label;
    QSpacerItem *verticalSpacer_3;
    QHBoxLayout *horizontalLayout_3;
    QPushButton *pushButton_3;
    QPushButton *pushButton_4;
    QSpacerItem *verticalSpacer_4;
    QPushButton *pushButton_2;
    QSpacerItem *verticalSpacer_2;
    QGroupBox *groupBox;
    QVBoxLayout *verticalLayout_7;
    QVBoxLayout *verticalLayout_5;
    QListWidget *listWidget;
    QSpacerItem *verticalSpacer_5;
    QCalendarWidget *calendarWidget;
    QWidget *tab_2;
    QMenuBar *menuBar;
    QMenu *menu;
    QMenu *menu_2;
    QStatusBar *statusBar;
    QDockWidget *dockWidget_6;
    QWidget *dockWidgetContents_6;
    QVBoxLayout *verticalLayout_2;
    QTreeWidget *treeWidget;
    QDockWidget *dockWidget_7;
    QWidget *dockWidgetContents_7;
    QVBoxLayout *verticalLayout;
    QFrame *frame;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(771, 600);
        MainWindow->setToolButtonStyle(Qt::ToolButtonStyle::ToolButtonTextBesideIcon);
        MainWindow->setDocumentMode(false);
        MainWindow->setDockNestingEnabled(false);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        verticalLayout_3 = new QVBoxLayout(centralwidget);
        verticalLayout_3->setObjectName("verticalLayout_3");
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName("horizontalLayout");
        lineEdit = new QLineEdit(centralwidget);
        lineEdit->setObjectName("lineEdit");

        horizontalLayout->addWidget(lineEdit);

        pushButton = new QPushButton(centralwidget);
        pushButton->setObjectName("pushButton");

        horizontalLayout->addWidget(pushButton);


        verticalLayout_3->addLayout(horizontalLayout);

        tabWidget = new QTabWidget(centralwidget);
        tabWidget->setObjectName("tabWidget");
        tabWidget->setEnabled(true);
        tabWidget->setAutoFillBackground(false);
        tabWidget->setTabPosition(QTabWidget::TabPosition::North);
        tabWidget->setTabShape(QTabWidget::TabShape::Rounded);
        tabWidget->setDocumentMode(false);
        tabWidget->setTabsClosable(true);
        tabWidget->setMovable(true);
        tabWidget->setTabBarAutoHide(true);
        tab = new QWidget();
        tab->setObjectName("tab");
        horizontalLayout_2 = new QHBoxLayout(tab);
        horizontalLayout_2->setObjectName("horizontalLayout_2");
        verticalLayout_4 = new QVBoxLayout();
        verticalLayout_4->setObjectName("verticalLayout_4");
        scrollArea = new QScrollArea(tab);
        scrollArea->setObjectName("scrollArea");
        scrollArea->setWidgetResizable(true);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName("scrollAreaWidgetContents");
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 351, 591));
        verticalLayout_6 = new QVBoxLayout(scrollAreaWidgetContents);
        verticalLayout_6->setObjectName("verticalLayout_6");
        verticalSpacer = new QSpacerItem(20, 5, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Minimum);

        verticalLayout_6->addItem(verticalSpacer);

        label = new QLabel(scrollAreaWidgetContents);
        label->setObjectName("label");
        QSizePolicy sizePolicy(QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Maximum);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(label->sizePolicy().hasHeightForWidth());
        label->setSizePolicy(sizePolicy);
        label->setTabletTracking(false);
        label->setTextFormat(Qt::TextFormat::AutoText);
        label->setScaledContents(false);
        label->setAlignment(Qt::AlignmentFlag::AlignCenter);
        label->setWordWrap(false);
        label->setOpenExternalLinks(false);

        verticalLayout_6->addWidget(label);

        verticalSpacer_3 = new QSpacerItem(20, 5, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Minimum);

        verticalLayout_6->addItem(verticalSpacer_3);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setObjectName("horizontalLayout_3");
        pushButton_3 = new QPushButton(scrollAreaWidgetContents);
        pushButton_3->setObjectName("pushButton_3");

        horizontalLayout_3->addWidget(pushButton_3);

        pushButton_4 = new QPushButton(scrollAreaWidgetContents);
        pushButton_4->setObjectName("pushButton_4");

        horizontalLayout_3->addWidget(pushButton_4);


        verticalLayout_6->addLayout(horizontalLayout_3);

        verticalSpacer_4 = new QSpacerItem(20, 5, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Minimum);

        verticalLayout_6->addItem(verticalSpacer_4);

        pushButton_2 = new QPushButton(scrollAreaWidgetContents);
        pushButton_2->setObjectName("pushButton_2");

        verticalLayout_6->addWidget(pushButton_2);

        verticalSpacer_2 = new QSpacerItem(20, 5, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Minimum);

        verticalLayout_6->addItem(verticalSpacer_2);

        groupBox = new QGroupBox(scrollAreaWidgetContents);
        groupBox->setObjectName("groupBox");
        QSizePolicy sizePolicy1(QSizePolicy::Policy::Preferred, QSizePolicy::Policy::Minimum);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(150);
        sizePolicy1.setHeightForWidth(groupBox->sizePolicy().hasHeightForWidth());
        groupBox->setSizePolicy(sizePolicy1);
        verticalLayout_7 = new QVBoxLayout(groupBox);
        verticalLayout_7->setObjectName("verticalLayout_7");
        verticalLayout_5 = new QVBoxLayout();
        verticalLayout_5->setObjectName("verticalLayout_5");
        listWidget = new QListWidget(groupBox);
        listWidget->setObjectName("listWidget");
        listWidget->setFrameShadow(QFrame::Shadow::Sunken);
        listWidget->setSortingEnabled(true);

        verticalLayout_5->addWidget(listWidget);


        verticalLayout_7->addLayout(verticalLayout_5);


        verticalLayout_6->addWidget(groupBox);

        verticalSpacer_5 = new QSpacerItem(20, 5, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Minimum);

        verticalLayout_6->addItem(verticalSpacer_5);

        calendarWidget = new QCalendarWidget(scrollAreaWidgetContents);
        calendarWidget->setObjectName("calendarWidget");

        verticalLayout_6->addWidget(calendarWidget);

        scrollArea->setWidget(scrollAreaWidgetContents);

        verticalLayout_4->addWidget(scrollArea);


        horizontalLayout_2->addLayout(verticalLayout_4);

        tabWidget->addTab(tab, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName("tab_2");
        tabWidget->addTab(tab_2, QString());

        verticalLayout_3->addWidget(tabWidget);

        MainWindow->setCentralWidget(centralwidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName("menuBar");
        menuBar->setGeometry(QRect(0, 0, 771, 33));
        menu = new QMenu(menuBar);
        menu->setObjectName("menu");
        menu_2 = new QMenu(menuBar);
        menu_2->setObjectName("menu_2");
        MainWindow->setMenuBar(menuBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName("statusBar");
        MainWindow->setStatusBar(statusBar);
        dockWidget_6 = new QDockWidget(MainWindow);
        dockWidget_6->setObjectName("dockWidget_6");
        dockWidget_6->setFloating(false);
        dockWidgetContents_6 = new QWidget();
        dockWidgetContents_6->setObjectName("dockWidgetContents_6");
        verticalLayout_2 = new QVBoxLayout(dockWidgetContents_6);
        verticalLayout_2->setObjectName("verticalLayout_2");
        treeWidget = new QTreeWidget(dockWidgetContents_6);
        QTreeWidgetItem *__qtreewidgetitem = new QTreeWidgetItem();
        __qtreewidgetitem->setText(0, QString::fromUtf8("\320\240\320\260\320\267\320\264\320\265\320\273\321\213"));
        treeWidget->setHeaderItem(__qtreewidgetitem);
        treeWidget->setObjectName("treeWidget");

        verticalLayout_2->addWidget(treeWidget);

        dockWidget_6->setWidget(dockWidgetContents_6);
        MainWindow->addDockWidget(Qt::DockWidgetArea::LeftDockWidgetArea, dockWidget_6);
        dockWidget_7 = new QDockWidget(MainWindow);
        dockWidget_7->setObjectName("dockWidget_7");
        dockWidgetContents_7 = new QWidget();
        dockWidgetContents_7->setObjectName("dockWidgetContents_7");
        verticalLayout = new QVBoxLayout(dockWidgetContents_7);
        verticalLayout->setObjectName("verticalLayout");
        frame = new QFrame(dockWidgetContents_7);
        frame->setObjectName("frame");
        frame->setFrameShape(QFrame::Shape::StyledPanel);
        frame->setFrameShadow(QFrame::Shadow::Raised);

        verticalLayout->addWidget(frame);

        dockWidget_7->setWidget(dockWidgetContents_7);
        MainWindow->addDockWidget(Qt::DockWidgetArea::RightDockWidgetArea, dockWidget_7);

        menuBar->addAction(menu->menuAction());
        menuBar->addAction(menu_2->menuAction());

        retranslateUi(MainWindow);

        tabWidget->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        pushButton->setText(QCoreApplication::translate("MainWindow", "\320\235\320\260\320\271\321\202\320\270", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:700;\">\320\235\320\260\321\207\320\260\320\273\320\276 \321\200\320\260\320\261\320\276\321\202\321\213</span></p></body></html>", nullptr));
        pushButton_3->setText(QCoreApplication::translate("MainWindow", "\320\241\320\276\320\267\320\264\320\260\321\202\321\214 \320\267\320\260\320\277\320\270\321\201\321\214", nullptr));
        pushButton_4->setText(QCoreApplication::translate("MainWindow", "\320\241\320\276\320\267\320\264\320\260\321\202\321\214 \321\200\320\260\320\267\320\264\320\265\320\273", nullptr));
        pushButton_2->setText(QCoreApplication::translate("MainWindow", "\320\227\320\260\320\263\321\200\321\203\320\267\320\270\321\202\321\214 \321\204\320\276\321\202\320\276 \320\277\320\276 EXIF", nullptr));
        groupBox->setTitle(QCoreApplication::translate("MainWindow", "\320\237\320\276\321\201\320\273\320\265\320\264\320\275\320\270\320\265 \320\276\321\202\320\272\321\200\321\213\321\202\321\213\320\265 \320\267\320\260\320\277\320\270\321\201\320\270", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(tab), QCoreApplication::translate("MainWindow", "Tab 1", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(tab_2), QCoreApplication::translate("MainWindow", "Tab 2", nullptr));
        menu->setTitle(QCoreApplication::translate("MainWindow", "\320\237\321\200\320\276\321\204\320\270\320\273\321\214", nullptr));
        menu_2->setTitle(QCoreApplication::translate("MainWindow", "\320\235\320\260\321\201\321\202\321\200\320\276\320\271\320\272\320\270", nullptr));
        dockWidget_6->setWindowTitle(QCoreApplication::translate("MainWindow", "\320\230\320\265\321\200\320\260\321\200\321\205\320\270\321\217 \320\261\320\260\320\267\321\213 \320\267\320\275\320\260\320\275\320\270\320\271", nullptr));
        dockWidget_7->setWindowTitle(QCoreApplication::translate("MainWindow", "\320\241\320\262\320\271\321\201\321\202\320\262\320\260", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // MAIN_WINDOW_UI_H
