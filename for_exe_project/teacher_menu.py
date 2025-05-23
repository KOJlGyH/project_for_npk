# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'teacher_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TeacherMenu(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("/* General Settings */\n"
"QWidget {\n"
"    font-family: \"Comic Sans MS\"; /* Fun and playful font */\n"
"    font-size: 14px;\n"
"    color: #2c3e50; /* Dark blue for text */\n"
"    background-color: #f9f9f9; /* Light gray background */\n"
"}\n"
"\n"
"/* Background Images for Different Pages */\n"
"QWidget#mathPage {\n"
"    background-image: url(:/backgrounds/math_background.png); /* Math-themed background */\n"
"    background-position: center;\n"
"    background-repeat: no-repeat;\n"
"    background-size: cover;\n"
"}\n"
"\n"
"QWidget#sciencePage {\n"
"    background-image: url(:/backgrounds/science_background.png); /* Science-themed background */\n"
"    background-position: center;\n"
"    background-repeat: no-repeat;\n"
"    background-size: cover;\n"
"}\n"
"\n"
"QWidget#literaturePage {\n"
"    background-image: url(:/backgrounds/literature_background.png); /* Literature-themed background */\n"
"    background-position: center;\n"
"    background-repeat: no-repeat;\n"
"    background-size: cover;\n"
"}\n"
"\n"
"QWidget#historyPage {\n"
"    background-image: url(:/backgrounds/history_background.png); /* History-themed background */\n"
"    background-position: center;\n"
"    background-repeat: no-repeat;\n"
"    background-size: cover;\n"
"}\n"
"\n"
"/* Buttons */\n"
"QPushButton {\n"
"    background-color: #ff6f61; /* Coral */\n"
"    color: white;\n"
"    border: 2px solid #ff3b2f; /* Darker coral */\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    font-weight: bold;\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #ff3b2f; /* Darker coral on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #ff1a1a; /* Even darker coral when pressed */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #bdc3c7; /* Gray */\n"
"    color: #7f8c8d; /* Light gray text */\n"
"    border: 2px solid #95a5a6;\n"
"}\n"
"\n"
"/* Line Edits */\n"
"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white */\n"
"    border: 2px solid #3498db; /* Blue border */\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #ff6f61; /* Coral border when focused */\n"
"}\n"
"\n"
"/* Labels */\n"
"QLabel {\n"
"    color: #2c3e50; /* Dark blue */\n"
"    font-size: 14px;\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white */\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel#titleLabel {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #3498db; /* Blue for titles */\n"
"    background-color: transparent; /* No background for titles */\n"
"}\n"
"\n"
"/* Combo Boxes */\n"
"QComboBox {\n"
"    background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white */\n"
"    border: 2px solid #3498db; /* Blue border */\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 30px;\n"
"    border-left: 2px solid #3498db;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/down_arrow.png); /* Replace with your icon */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: white;\n"
"    border: 2px solid #3498db;\n"
"    selection-background-color: #ff6f61; /* Coral for selected item */\n"
"    selection-color: white;\n"
"}\n"
"\n"
"/* Check Boxes */\n"
"QCheckBox {\n"
"    color: #2c3e50;\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white */\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(:/icons/checked.png); /* Replace with your icon */\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(:/icons/unchecked.png); /* Replace with your icon */\n"
"}\n"
"\n"
"/* Radio Buttons */\n"
"QRadioButton {\n"
"    color: #2c3e50;\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white */\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    image: url(:/icons/radio_checked.png); /* Replace with your icon */\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"    image: url(:/icons/radio_unchecked.png); /* Replace with your icon */\n"
"}\n"
"\n"
"/* Progress Bars */\n"
"QProgressBar {\n"
"    background-color: #bdc3c7;\n"
"    border: 2px solid #95a5a6;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"    color: #2c3e50;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #ff6f61; /* Coral */\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* Spin Boxes */\n"
"QSpinBox {\n"
"    background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white */\n"
"    border: 2px solid #3498db; /* Blue border */\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QSpinBox::up-button, QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 30px;\n"
"    border-left: 2px solid #3498db;\n"
"}\n"
"\n"
"QSpinBox::up-arrow {\n"
"    image: url(:/icons/up_arrow.png); /* Replace with your icon */\n"
"}\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/down_arrow.png); /* Replace with your icon */\n"
"}\n"
"\n"
"/* Group Boxes */\n"
"QGroupBox {\n"
"    border: 2px solid #3498db; /* Blue border */\n"
"    border-radius: 10px;\n"
"    margin-top: 10px;\n"
"    padding-top: 15px;\n"
"    font-weight: bold;\n"
"    color: #3498db; /* Blue for group box titles */\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0 10px;\n"
"}\n"
"\n"
"/* Tabs */\n"
"QTabWidget::pane {\n"
"    border: 2px solid #3498db; /* Blue border */\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #ecf0f1;\n"
"    border: 2px solid #3498db;\n"
"    border-bottom: none;\n"
"    padding: 10px 20px;\n"
"    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: white;\n"
"    border-bottom: 2px solid white;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background-color: #ff6f61; /* Coral on hover */\n"
"    color: white;\n"
"}\n"
"\n"
"/* Scroll Bars */\n"
"QScrollBar:horizontal, QScrollBar:vertical {\n"
"    background-color: #ecf0f1;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal, QScrollBar::handle:vertical {\n"
"    background-color: #ff6f61; /* Coral */\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QScrollBar::add-line, QScrollBar::sub-line {\n"
"    background: none;\n"
"}\n"
"\n"
"/* Tool Tips */\n"
"QToolTip {\n"
"    background-color: #ff6f61; /* Coral */\n"
"    color: white;\n"
"    border: 2px solid #ff3b2f;\n"
"    padding: 10px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* Menus */\n"
"QMenuBar {\n"
"    background-color: #ecf0f1;\n"
"    color: #2c3e50;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    padding: 10px 20px;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background-color: #ff6f61; /* Coral */\n"
"    color: white;\n"
"}\n"
"\n"
"QMenu {\n"
"    background-color: white;\n"
"    border: 2px solid #3498db;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    padding: 10px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    background-color: #ff6f61; /* Coral */\n"
"    color: white;\n"
"}\n"
"\n"
"/* Tables */\n"
"QTableView {\n"
"    background-color: white;\n"
"    border: 2px solid #3498db;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: #ff6f61; /* Coral */\n"
"    color: white;\n"
"}\n"
"\n"
"/* Text Edit */\n"
"QTextEdit {\n"
"    background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white */\n"
"    border: 2px solid #3498db;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QTextEdit:focus {\n"
"    border: 2px solid #ff6f61; /* Coral */\n"
"}\n"
"\n"
"/* Status Bar */\n"
"QStatusBar {\n"
"    background-color: #ecf0f1;\n"
"    border-top: 2px solid #3498db;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"/* Tool Bars */\n"
"QToolBar {\n"
"    background-color: #ecf0f1;\n"
"    border-bottom: 2px solid #3498db;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QToolBar::separator {\n"
"    background-color: #3498db;\n"
"    width: 2px;\n"
"    margin: 10px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(30, 30, 171, 41))
        self.back_button.setStyleSheet("")
        self.back_button.setObjectName("back_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 10, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(-1)
        self.label.setFont(font)
        self.label.setStyleSheet("font-size: 20px;\n"
"")
        self.label.setObjectName("label")
        self.create_work_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_work_button.setGeometry(QtCore.QRect(270, 110, 271, 41))
        self.create_work_button.setStyleSheet("")
        self.create_work_button.setObjectName("create_work_button")
        self.see_works_button = QtWidgets.QPushButton(self.centralwidget)
        self.see_works_button.setGeometry(QtCore.QRect(270, 180, 271, 41))
        self.see_works_button.setStyleSheet("")
        self.see_works_button.setObjectName("see_works_button")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(120, 240, 421, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(-1)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.codeEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.codeEdit_2.setMaximumSize(QtCore.QSize(16777215, 45))
        self.codeEdit_2.setStyleSheet("")
        self.codeEdit_2.setObjectName("codeEdit_2")
        self.horizontalLayout.addWidget(self.codeEdit_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(270, 340, 271, 41))
        self.pushButton_4.setStyleSheet("")
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 40))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.back_button.setText(_translate("MainWindow", "<--- Вернуться"))
        self.label.setText(_translate("MainWindow", "Окно учителя"))
        self.create_work_button.setText(_translate("MainWindow", "Создать проверочную"))
        self.see_works_button.setText(_translate("MainWindow", "Посмотреть работы"))
        self.label_3.setText(_translate("MainWindow", "Код проверочной"))
        self.pushButton_4.setText(_translate("MainWindow", "Ручная проверка"))
