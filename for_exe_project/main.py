import os

import requests
import json
import random
import string
import re
import sys

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QVBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QPushButton, QHBoxLayout, QWidget, QFrame, QLabel, QGraphicsOpacityEffect
from PyQt5.QtWidgets import QMainWindow
from log_in import *
from new_test import *
from registration import *
from start import *
from student_menu import *
from tester import *
from res import *
from teacher_menu import *
from choose_work import *
from check_form import *
from PyQt5.QtGui import QPixmap, QKeyEvent, QIcon

host = 'http://127.0.0.1:5000'

host = 'https://KOJlGylHl.pythonanywhere.com'


def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    else:
        return 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    return score


# from bot import send_result
def generate_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def password_level(password):
    score = check_password_strength(password)
    if score == 4:
        return 'ok'
    else:
        return 'Пароль должен состоять хотя бы из 8 символов, включая оба регистра и спец. символы.'


def get_img(data, url):
    data = json.dumps(data)
    return requests.get(host + url, json=data)


def post_in_db(data, url):
    response = requests.post(host + url, json=data)
    return response


def post_images(files, url):
    response = requests.post(host + url, files=files)
    return response


class Notification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_animation()

    def setup_ui(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 200)

        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: #2E2E2E;
                border-radius: 8px;
                border: 1px solid #4A4A4A;
            }
        """)

        # Макет
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 10, 15, 10)
        self.title_label = QLabel("Уведомление")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-weight: bold;
                font-size: 14px;
            }
        """)

        self.message_label = QLabel("Сообщение")
        self.message_label.setStyleSheet("""
            QLabel {
                color: #CCCCCC;
                font-size: 12px;
            }
        """)
        self.message_label.setWordWrap(True)
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                color: #AAAAAA;
                font-size: 16px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                color: #FFFFFF;
            }
        """)
        self.close_btn.clicked.connect(self.hide_notification)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)

        layout.addLayout(header_layout)
        layout.addWidget(self.message_label)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.container)
        self.setLayout(main_layout)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

    def setup_animation(self):
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_notification)

    def show_notification(self, title, message, duration=3000, position=None, center_on_parent=True):
        """Показать уведомление"""
        self.title_label.setText(title)
        self.message_label.setText(message)

        if center_on_parent and self.parent():
            # Центр родительского окна
            parent_center = self.parent().geometry().center()
            self.move(parent_center - self.rect().center())
        else:
            screen_center = self.screen().availableGeometry().center()
            self.move(screen_center - self.rect().center())

        self.fade_animation.stop()
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()

        self.show()

        # Автоскрытие
        if duration > 0:
            self.timer.start(duration)

    def hide_notification(self):
        self.fade_animation.stop()
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.finished.connect(self.close)
        self.fade_animation.start()

    def mousePressEvent(self, event):
        self.hide_notification()

    def set_theme(self, theme="dark"):
        if theme == "light":
            self.container.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border-radius: 8px;
                    border: 1px solid #DDDDDD;
                }
            """)
            self.title_label.setStyleSheet("""
                QLabel {
                    color: #333333;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            self.message_label.setStyleSheet("""
                QLabel {
                    color: #666666;
                    font-size: 12px;
                }
            """)
            self.close_btn.setStyleSheet("""
                QPushButton {
                    color: #666666;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                    background: transparent;
                }
                QPushButton:hover {
                    color: #000000;
                }
            """)


class FirstMenu(QMainWindow, Ui_start):
    def __init__(self):
        super().__init__()
        self.next_form = None
        self.setupUi(self)
        self.log_in.clicked.connect(self.log)
        self.registration.clicked.connect(self.reg)
        self.setWindowTitle('Testify')

        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))

    def log(self):
        self.next_form = LogIn()
        self.next_form.show()
        self.close()

    def reg(self):
        self.next_form = Registration()
        self.next_form.show()
        self.close()


class LogIn(QMainWindow, Ui_log_in):
    def __init__(self):
        super().__init__()
        self.new_form = None
        self.setupUi(self)
        self.log_in_button.clicked.connect(self.click)
        self.pushButton.clicked.connect(self.back)
        self.notification = Notification(self)
        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))

    def back(self):
        self.new_form = FirstMenu()
        self.new_form.show()
        self.close()

    def click(self):
        login = self.login.text()
        password = self.password.text()
        data = {'login': login,
                'password': password}
        response = post_in_db(data, '/log_in')
        if response.status_code != 200:
            self.login.setText('')
            self.password.setText('')
            self.notification.show_notification(
                "Неуспешно",
                response.json()['message'],
                duration=4000,
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        data = response.json()
        status = data['status']
        if status == 0:
            self.new_form = StudentMenu(login, password)
            self.new_form.show()
            self.close()
        if status == 1:
            self.new_form = TeacherMenu(login, password)
            self.new_form.show()
            self.close()
            # self.new_form = NewTest(login, password)
            # self.new_form.show()
            # self.close()


class TeacherMenu(QMainWindow, Ui_TeacherMenu):
    def __init__(self, login, password):
        super().__init__()
        self.next_form = None
        self.new_form = None
        self.setupUi(self)
        self.login = login
        self.password = password
        self.create_work_button.clicked.connect(self.create_work)
        self.see_works_button.clicked.connect(self.see_works)
        self.pushButton_4.clicked.connect(self.check_work)
        self.back_button.clicked.connect(self.back)
        self.notification = Notification(self)
        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))

    def create_work(self):
        data = {'login': self.login,
                'password': self.password}

        response = post_in_db(data, '/log_in')
        if response.status_code != 200:
            self.notification.show_notification(
                "Неуспешно",
                response.json()['message'],
                duration=3500,
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.new_form = NewTest(self.login, self.password)
        self.new_form.show()
        self.close()

    def see_works(self):
        data = {'login': self.login,
                'password': self.password}

        response = post_in_db(data, '/log_in')
        if response.status_code != 200:
            self.notification.show_notification(
                "Неуспешно",
                response.json()['message'],
                duration=3500,
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.new_form = Results(self.login, self.password)
        self.new_form.show()
        self.close()

    def check_work(self):
        data = {'login': self.login,
                'password': self.password,
                'key': self.codeEdit_2.text()}

        response = post_in_db(data, '/to_check_work')
        if response.status_code != 200:
            self.notification.show_notification(
                "Неуспешно",
                response.json()['message'],
                duration=3500,
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.new_form = ChooseWork(self.login, self.password, self.codeEdit_2.text())
        self.new_form.show()
        self.close()

    def back(self):
        self.new_form = LogIn()
        self.new_form.show()
        self.close()


class ChooseWork(QMainWindow, Ui_ChooseWork):
    def __init__(self, login, password, key):
        super().__init__()
        self.next_form = None
        self.new_form = None
        self.setupUi(self)
        self.login = login
        self.password = password
        self.key = key
        data = {'login': login, 'password': password, 'key': key}
        response = post_in_db(data, '/logins_by_key')  # '''logins, usernames'''
        self.logins = response.json()['logins']
        self.usernames = response.json()['usernames']
        self.comboBox.addItems(self.usernames)
        self.satrt_check_button.clicked.connect(self.start_check)
        self.back_button.clicked.connect(self.back)
        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))

    def start_check(self):
        username = self.comboBox.currentText()
        login = self.logins[self.usernames.index(username)]
        self.new_form = CheckForm(self.login, self.password, self.key, login)
        self.new_form.show()
        self.close()

    def back(self):
        self.new_form = TeacherMenu(self.login, self.password)
        self.new_form.show()
        self.close()


class CheckForm(QMainWindow, Ui_CheckForm):
    def __init__(self, login, password, key, userlogin):
        super().__init__()
        self.next_form = None
        self.new_form = None
        self.setupUi(self)
        self.login = login
        self.password = password
        self.key = key
        self.userlogin = userlogin
        data = {'login': self.login, 'password': self.password, 'key': self.key}
        response = post_in_db(data, '/tester')
        resp_j = response.json()
        self.questions = resp_j['questions']
        self.answers = resp_j['answers']
        self.points = resp_j['points']
        self.pre = resp_j['pre']
        self.index = -1
        self.notification = Notification(self)
        for i in range(len(self.pre)):
            if self.pre[i][0] == self.userlogin:
                self.index = i
        if self.index == -1:
            self.notification.show_notification(
                "Неуспешно",
                'Логин ученика не найден',
                duration=3500,
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.current_qwe = 0

        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))

        self.qwestionEdit.setText(self.questions[self.current_qwe])
        self.answerEdit.setText(self.answers[self.current_qwe])
        self.useranswerEdit.setText(self.pre[self.index][1][self.current_qwe][1])
        self.comboBox.clear()
        self.comboBox.addItems(list(map(str, (range(0, int(self.points[self.current_qwe]) + 1)))))
        self.comboBox.setCurrentText(str(self.pre[self.index][1][self.current_qwe][0]))

        s = '\\'
        s = '/'
        filename = f'../images{s}{self.key}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image1.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image1.jpg")
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.imageLabel.mousePressEvent = lambda event: self.view_image("temp_image1.jpg")

        s = '\\'
        s = '/'
        filename = f'../images{s}{self.key}_{self.userlogin}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.userimageLabel.setPixmap(pixmap.scaled(self.userimageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.userimageLabel.mousePressEvent = lambda event: self.view_image("temp_image.jpg")

        self.back_button.clicked.connect(self.back)
        self.endButton.clicked.connect(self.end)
        self.previewButton.clicked.connect(self.preview)
        self.nextButton.clicked.connect(self.next)

    def view_image(self, image_path):
        image_dialog = QDialog(self)
        image_dialog.setWindowTitle("View Image")
        image_dialog.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()
        image_view = QGraphicsView()
        image_scene = QGraphicsScene()
        pixmap = QPixmap(image_path)
        image_item = QGraphicsPixmapItem(pixmap)
        image_scene.addItem(image_item)
        image_view.setScene(image_scene)
        main_layout.addWidget(image_view)

        image_view.setFocusPolicy(Qt.StrongFocus)
        image_view.setFocus()

        rotate_button = QPushButton("Rotate")
        rotate_button.setFixedSize(100, 40)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(rotate_button)
        main_layout.addLayout(button_layout)

        image_dialog.setLayout(main_layout)

        def rotate_image(angle):
            image_item.setRotation(image_item.rotation() + angle)

        rotate_button.clicked.connect(lambda: rotate_image(90))

        def keyPressEvent(event: QKeyEvent):
            if event.modifiers() & Qt.ControlModifier:
                if event.key() == Qt.Key_Left:
                    rotate_image(-90)
                    event.accept()
                    return
                elif event.key() == Qt.Key_Right:
                    rotate_image(90)
                    event.accept()
                    return
            QGraphicsView.keyPressEvent(image_view, event)
        image_view.keyPressEvent = keyPressEvent

        def wheelEvent(event):
            if event.modifiers() == Qt.ControlModifier:
                delta = event.angleDelta().y()
                if delta > 0:
                    image_view.scale(1.2, 1.2)
                else:
                    image_view.scale(0.8, 0.8)
                event.accept()
            else:
                QGraphicsView.wheelEvent(image_view, event)

        image_view.wheelEvent = wheelEvent

        image_dialog.exec()

    def back(self):
        self.new_form = ChooseWork(self.login, self.password, self.key)
        self.new_form.show()
        self.close()

    def end(self):
        self.pre[self.index][1][self.current_qwe][0] = int(self.comboBox.currentText())
        data = {'login': self.login, 'res': self.pre, 'key': self.key, 'password': self.password}
        response = post_in_db(data, '/big_update')
        if response.status_code == 200:
            self.notification.show_notification(
                "Успех",
                'Работа проверена',
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
        else:
            self.notification.show_notification(
                "Неуспешно",
                response.json()['message'],
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return

    def preview(self):
        if self.current_qwe == 0:
            self.notification.show_notification(
                "Неуспешно",
                "Это уже первый вопрос.",
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.pre[self.index][1][self.current_qwe][0] = int(self.comboBox.currentText())
        self.current_qwe -= 1
        self.qwestionEdit.setText(self.questions[self.current_qwe])
        self.answerEdit.setText(self.answers[self.current_qwe])
        self.useranswerEdit.setText(self.pre[self.index][1][self.current_qwe][1])
        self.comboBox.clear()
        self.comboBox.addItems(list(map(str, (range(0, int(self.points[self.current_qwe]) + 1)))))
        self.comboBox.setCurrentText(str(self.pre[self.index][1][self.current_qwe][0]))

        s = '\\'
        s = '/'
        filename = f'../images{s}{self.key}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image1.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image1.jpg")
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.imageLabel.mousePressEvent = lambda event: self.view_image("temp_image1.jpg")

        s = '\\'
        s = '/'
        filename = f'../images{s}{self.key}_{self.userlogin}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.userimageLabel.setPixmap(pixmap.scaled(self.userimageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.userimageLabel.mousePressEvent = lambda event: self.view_image("temp_image.jpg")

    def next(self):
        if self.current_qwe == len(self.questions) - 1:
            self.notification.show_notification(
                "Неуспешно",
                "Это уже последний вопрос.",
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.pre[self.index][1][self.current_qwe][0] = int(self.comboBox.currentText())
        self.current_qwe += 1
        self.qwestionEdit.setText(self.questions[self.current_qwe])
        self.answerEdit.setText(self.answers[self.current_qwe])
        self.useranswerEdit.setText(self.pre[self.index][1][self.current_qwe][1])
        self.comboBox.clear()
        self.comboBox.addItems(list(map(str, (range(0, int(self.points[self.current_qwe]) + 1)))))
        self.comboBox.setCurrentText(str(self.pre[self.index][1][self.current_qwe][0]))

        s = '\\'
        s = '/'
        filename = f'../images{s}{self.key}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image1.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image1.jpg")
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.imageLabel.mousePressEvent = lambda event: self.view_image("temp_image1.jpg")

        s = '\\'
        s = '/'
        filename = f'../images{s}{self.key}_{self.userlogin}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.userimageLabel.setPixmap(pixmap.scaled(self.userimageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.userimageLabel.mousePressEvent = lambda event: self.view_image("temp_image.jpg")


class Registration(QMainWindow, Ui_Registration):
    def __init__(self):
        super().__init__()
        self.new_form = None
        self.setupUi(self)
        self.registration_button.clicked.connect(self.click)
        self.pushButton.clicked.connect(self.back)
        self.notification = Notification(self)
        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))

    def back(self):
        self.new_form = FirstMenu()
        self.new_form.show()
        self.close()

    def click(self):
        if self.loginEdit.text() == '' or self.password1Edit.text() == '' \
                or self.password1Edit.text() != self.password2Edit.text() or self.usernameEdit.text() == '':
            self.notification.show_notification(
                "Неуспешно.",
                "Введённые данные некорректны",
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            self.loginEdit.setText('')
            self.password1Edit.setText('')
            self.password2Edit.setText('')
            return

        if password_level(self.password1Edit.text()) != 'ok':
            self.notification.show_notification(
                "Неуспешно.",
                password_level(self.password1Edit.text()),
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        data = {'login': self.loginEdit.text(),
                'password': self.password1Edit.text(),
                'username': self.usernameEdit.text(),
                'status': self.comboBox.currentText()}
        response = post_in_db(data, '/registration')
        if response.status_code != 200:
            data = response.json()
            self.notification.show_notification(
                "Неуспешно",
                data['message'],
                duration=4000
            )
            self.notification = Notification(self)
            return
        self.new_form = LogIn()
        self.new_form.show()
        self.close()


class StudentMenu(QMainWindow, Ui_StudentMenu):
    def __init__(self, login, password):
        super().__init__()
        self.next_form = None
        self.new_form = None
        self.setupUi(self)
        self.login = login
        self.password = password
        self.notification = Notification(self)
        self.startTestButton.clicked.connect(self.click)
        self.pushButton.clicked.connect(self.back)
        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))

    def back(self):
        self.new_form = LogIn()
        self.new_form.show()
        self.close()

    def click(self):
        data = {'login': self.login,
                'password': self.password,
                'key': self.codeEdit.text()}
        response = post_in_db(data, '/student_menu')
        if response.status_code != 200:
            self.notification.show_notification(
                "Неуспешно.",
                response.json()['message'],
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.next_form = Tester(self.login, self.password, self.codeEdit.text())
        self.next_form.show()
        self.close()


class NewTest(QMainWindow, Ui_NewTest):
    def __init__(self, login, password):
        super().__init__()
        self.copied = False
        self.password = password
        self.login = login
        self.setupUi(self)
        self.addAnsButton.clicked.connect(self.add)
        self.loadButton.clicked.connect(self.load)
        self.pushButton.clicked.connect(self.back)
        # self.pushButton_2.clicked.connect(self.result)
        self.btn.clicked.connect(self.load_image)
        self.counter = 0
        self.aditive = 0
        self.codeEdit.setText(generate_code())
        self.pushButton_3.clicked.connect(self.copy_code)
        self.comboBox.clear()
        items = ["1", "2", '3', '4', '5']
        self.comboBox.addItems(items)
        self.all_works_button.clicked.connect(self.all_works)
        self.comboBox.setCurrentIndex(0)
        self.one_back_button.clicked.connect(self.one_back)
        self.notification = Notification(self)
        self.current_index = 0
        self.points = []
        self.questions = []
        self.answers = []
        self.image = {}
        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))

    def one_back(self):
        if self.current_index == 0:
            self.notification.show_notification(
                "Неуспешно",
                "Это уже первый вопрос",
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.current_index -= 1
        self.qwestionEdit.setText(self.questions[self.current_index])
        self.answerEdit.setText(self.answers[self.current_index])
        self.comboBox.setCurrentText(self.points[self.current_index])

    def copy_code(self):
        text = self.codeEdit.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.copied = True
        self.notification.show_notification(
            "Успех",
            'Код скопирован.',
            position=self.mapToGlobal(self.rect().topRight())
        )
        self.notification = Notification(self)

    def load_image(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                    "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        try:
            self.image[str(self.current_index)] = open(image_path, 'rb')
        except FileNotFoundError:
            print('Отмена при выборе изображения')

    def all_works(self):
        self.next_form = Results(self.login, self.password)
        self.next_form.show()
        self.close()

    def back(self):
        self.next_form = TeacherMenu(self.login, self.password)
        self.next_form.show()
        self.close()

    def add(self):
        if self.answerEdit.text() == '' or self.qwestionEdit.toPlainText() == '':
            self.notification.show_notification(
                "Неуспешно.",
                "Пустое поле вопрос или ответ.",
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return

        if len(self.questions) == self.current_index:
            self.questions.append('')
            self.answers.append('')
            self.points.append('')
        self.questions[self.current_index] = self.qwestionEdit.toPlainText()
        self.answers[self.current_index] = (self.answerEdit.text())
        self.points[self.current_index] = self.comboBox.currentText()

        if len(self.questions) <= self.current_index + 1:
            self.qwestionEdit.setText('')
            self.answerEdit.setText('')
            self.comboBox.setCurrentIndex(0)
        else:
            self.qwestionEdit.setText(self.questions[self.current_index + 1])
            self.answerEdit.setText(self.answers[self.current_index + 1])
            self.comboBox.setCurrentText(self.points[self.current_index + 1])
        self.current_index += 1
        self.notification.show_notification(
            "Успех",
            'Вопрос добавлен',
            position=self.mapToGlobal(self.rect().topRight())
        )
        self.notification = Notification(self)

    def load(self):
        if not self.copied:
            self.notification.show_notification(
                "Неуспешно.",
                'Код не скопирован',
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        if self.name_of_work.text() == '':
            self.notification.show_notification(
                "Неуспешно.",
                'Напишите название работы.',
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        if len(self.answers) == 0:
            self.notification.show_notification(
                "Неуспешно.",
                'Добавьте вопросы.',
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        data = {'login': self.login,
                'password': self.password,
                'key': self.codeEdit.text(),
                'name_of_work': self.name_of_work.text(),
                'answers': self.answers,
                'questions': self.questions,
                'points': self.points}  # add pictures
        response = post_in_db(data, '/new_test')
        if response.status_code != 200:
            self.notification.show_notification(
                "Неуспешно.",
                response.json()['message'],
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        else:
            response = post_images(self.image,
                                   f'/load_images/{self.codeEdit.text()}/{self.login}/{self.password}' + '/teacher')
            if response.status_code == 200:
                self.notification.show_notification(
                    "Успех",
                    response.json()['message'],
                    position=self.mapToGlobal(self.rect().topRight())
                )
                self.notification = Notification(self)
                return
            else:
                self.notification.show_notification(
                    "Неуспешно.",
                    response.json()['message'],
                    position=self.mapToGlobal(self.rect().topRight())
                )
                self.notification = Notification(self)
                return


class Results(QMainWindow, Ui_Res):
    def __init__(self, login, password):
        super().__init__()

        self.new_form = None
        self.answers = []
        self.login = login
        self.password = password
        self.setupUi(self)
        self.pushButton.clicked.connect(self.back)
        self.notification = Notification(self)
        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))
        data = {'login': self.login,
                'password': self.password,
                }
        response = post_in_db(data, '/results')

        if response.status_code == 200:
            self.textBrowser.setText(response.json()['message'])
        else:
            self.notification.show_notification(
                "Неуспешно.",
                response.json()['message'],
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return

    def back(self):
        self.new_form = TeacherMenu(self.login, self.password)
        self.new_form.show()
        self.close()


class Tester(QMainWindow, Ui_Tester):

    def __init__(self, login, password, key):
        super().__init__()
        self.setupUi(self)
        self.login = login
        self.key = key
        self.password = password
        self.results = []
        self.notification = Notification(self)
        # Внутри test пары вопрос ответ через *** а внутри через ,,,,
        self.setWindowTitle('Testify')
        s = '/'
        filename = f'../images{s}icon'
        response = get_img({'filename': filename, 'login': "teacher3", 'password': "Qwerty2008@"}, '/send_image')
        if response != '0':
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(pixmap))
        data = {'login': self.login,
                'password': self.password,
                'key': self.key}

        response = post_in_db(data, '/tester')
        json_resp = response.json()
        self.questions = json_resp['questions']
        self.answers = json_resp['answers']
        self.points = json_resp['points']
        self.pre = json_resp['pre']

        self.user_answers = ['' for _ in range(len(self.questions))]
        self.saveButton.clicked.connect(self.save)
        self.previewButton.clicked.connect(self.preview)
        self.nextButton.clicked.connect(self.next)
        self.endButton.clicked.connect(self.end)
        self.current_qwe = 0
        self.qwestionText.setText(self.questions[self.current_qwe])
        self.max_qwe = len(self.questions) - 1
        self.pushButton.clicked.connect(self.back)
        self.btn.clicked.connect(self.load_image)
        self.image = {}

        # s = '\\'
        s = '/'
        filename = f'../images{s}{self.key}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.label_3.mousePressEvent = lambda event: self.view_image("temp_image.jpg")

    def load_image(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                    "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        try:
            self.image[str(self.current_qwe)] = open(image_path, 'rb')
            self.notification.show_notification(
                "Успешно.",
                "Изображение выбрано.",
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
        except FileNotFoundError:
            print('Отмена при выборе изображения')

    def view_image(self, image_path):
        image_dialog = QDialog(self)
        image_dialog.setWindowTitle("View Image")
        image_dialog.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()
        image_view = QGraphicsView()
        image_scene = QGraphicsScene()
        pixmap = QPixmap(image_path)
        image_item = QGraphicsPixmapItem(pixmap)
        image_scene.addItem(image_item)
        image_view.setScene(image_scene)
        main_layout.addWidget(image_view)

        # Устанавливаем фокус на QGraphicsView для получения событий клавиатуры
        image_view.setFocusPolicy(Qt.StrongFocus)
        image_view.setFocus()

        rotate_button = QPushButton("Rotate")
        rotate_button.setFixedSize(100, 40)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(rotate_button)
        main_layout.addLayout(button_layout)

        image_dialog.setLayout(main_layout)

        def rotate_image(angle):
            image_item.setRotation(image_item.rotation() + angle)

        rotate_button.clicked.connect(lambda: rotate_image(90))

        def keyPressEvent(event: QKeyEvent):
            if event.modifiers() & Qt.ControlModifier:
                if event.key() == Qt.Key_Left:
                    rotate_image(-90)
                    event.accept()  # Помечаем событие как обработанное
                    return
                elif event.key() == Qt.Key_Right:
                    rotate_image(90)
                    event.accept()
                    return
            # Для остальных случаев вызываем базовую обработку
            QGraphicsView.keyPressEvent(image_view, event)

        # Переопределяем keyPressEvent для QGraphicsView
        image_view.keyPressEvent = keyPressEvent

        def wheelEvent(event):
            if event.modifiers() == Qt.ControlModifier:
                delta = event.angleDelta().y()
                if delta > 0:
                    image_view.scale(1.2, 1.2)
                else:
                    image_view.scale(0.8, 0.8)
                event.accept()  # Помечаем событие как обработанное
            else:
                QGraphicsView.wheelEvent(image_view, event)

        image_view.wheelEvent = wheelEvent

        image_dialog.exec()

    def back(self):
        self.next_form = StudentMenu(self.login, self.password)
        self.next_form.show()
        self.close()

    def save(self):
        self.user_answers[self.current_qwe] = self.answerEdit.text()
        self.notification.show_notification(
            "Успешно.",
            "Сохранено",
            position=self.mapToGlobal(self.rect().topRight())
        )
        self.notification = Notification(self)

    def preview(self):
        if self.current_qwe == 0:
            self.notification.show_notification(
                "Неуспешно.",
                'Это уже первый вопрос.',
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.current_qwe = self.current_qwe - 1
        self.qwestionText.setText(self.questions[self.current_qwe])
        self.answerEdit.setText(self.user_answers[self.current_qwe])

        # s = '\\'
        s = '/'
        filename = f'../images{s}{self.key}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def next(self):
        if self.current_qwe + 1 > self.max_qwe:
            self.notification.show_notification(
                "Неуспешно.",
                'Это уже последний вопрос.',
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        self.current_qwe = self.current_qwe + 1
        self.qwestionText.setText(self.questions[self.current_qwe])
        self.answerEdit.setText(self.user_answers[self.current_qwe])
        s = '\\'
        s = '/'

        filename = f'../images{s}{self.key}{self.current_qwe}'
        response = get_img({'filename': filename, 'login': self.login, 'password': self.password}, '/send_image')
        if response != '0':
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def end(self):
        sp = []
        for i in range(self.max_qwe + 1):
            if self.user_answers[i] == self.answers[i]:
                sp.append([int(self.points[i]), self.user_answers[i]])
            else:
                sp.append([0, self.user_answers[i]])
        res = [self.login, sp]

        data = {'login': self.login,
                'password': self.password,
                'res': res,
                'key': self.key}
        response = post_in_db(data, '/update_results')
        if response.status_code != 200:
            self.notification.show_notification(
                "Неуспешно.",
                response.json()['message'],
                position=self.mapToGlobal(self.rect().topRight())
            )
            self.notification = Notification(self)
            return
        else:
            response = post_images(self.image,
                                   f'/load_images/{self.key}/{self.login}/{self.password}' + '/user')
            if response.status_code == 200:
                self.notification.show_notification(
                    "Успех",
                    response.json()['message'],
                    position=self.mapToGlobal(self.rect().topRight())
                )
                self.notification = Notification(self)
            else:
                self.notification.show_notification(
                    "Неуспешно.",
                    response.json()['message'],
                    position=self.mapToGlobal(self.rect().topRight())
                )
                self.notification = Notification(self)
            return


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myapp.1.0")
        myappid = 'mycompany.myapp.1.0'  # Произвольный идентификатор
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    ex = FirstMenu()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
