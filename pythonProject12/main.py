import sys
from idlelib.replace import replace

import requests
import json
import random
import string
import re
import hashlib
import os
import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QVBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMainWindow
from log_in import *
from new_test import *
from registration import *
from start import *
from student_menu import *
from tester import *
from res import *
from PyQt5.QtGui import QPixmap, QKeyEvent

host = 'http://127.0.0.1:5000'
host = 'https://KOJlGylHl.pythonanywhere.com'


def hash_password(password: str, salt: bytes = None, iterations=100000) -> tuple:
    """Генерирует хеш пароля с солью (PBKDF2-HMAC-SHA256)."""
    if salt is None:
        salt = os.urandom(16)  # 128-битная соль
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations
    )
    return salt.hex(), key.hex()


def verify_password(password: str, salt: str, hashed: str) -> bool:
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        bytes.fromhex(salt),
        100000
    ).hex()
    return new_hash == hashed


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


def get_from_db(data):
    data = json.dumps(data)
    ans = requests.get(host, data=data).json()
    print(ans)
    return ans


def get_img(data):
    data = json.dumps(data)
    return requests.get(host, data=data)


def post_in_db(data):
    data = json.dumps(data)
    requests.post(host, data=data)
    return None


def post_images(files):
    requests.post(host, files=files)
    return None


class FirstMenu(QMainWindow, Ui_start):
    def __init__(self):
        super().__init__()
        self.next_form = None
        self.setupUi(self)
        self.log_in.clicked.connect(self.log)
        self.registration.clicked.connect(self.reg)
        # self.pixmap = QPixmap('my.png').scaled(300, 300)
        # self.label.resize(300, 300)
        # self.label.move(100, 300)
        # self.label.setPixmap(self.pixmap)

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

    def back(self):
        self.new_form = FirstMenu()
        self.new_form.show()
        self.close()

    def click(self):
        login = self.login.text()
        password = self.password.text()
        logins = get_from_db(['login', 'user', 'id > 0'])
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            self.statusbar.showMessage('Неправильный логин или пароль')
            self.login.setText('')
            self.password.setText('')
            return
        salt = get_from_db(['salt', 'salts', f'login="{login}"'])
        salt = list(map(lambda x: x[0], salt))[0]
        passwords = get_from_db(['password', 'user', f'login="{login}"'])
        hashed = list(map(lambda x: x[0], passwords))[0]
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            self.statusbar.showMessage('Неправильный логин или пароль')
            self.login.setText('')
            self.password.setText('')
            return
        status = get_from_db(['status', 'user', f'login="{login}"'])[0][0]
        if status == 0:
            self.new_form = StudentMenu(login)
            self.new_form.show()
            self.close()
        if status == 1:
            self.new_form = NewTest(login)
            self.new_form.show()
            self.close()


class Registration(QMainWindow, Ui_Registration):
    def __init__(self):
        super().__init__()
        self.new_form = None
        self.setupUi(self)
        self.registration_button.clicked.connect(self.click)
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.new_form = FirstMenu()
        self.new_form.show()
        self.close()

    def click(self):
        if self.loginEdit.text() == '' or self.password1Edit.text() == '' \
                or self.password1Edit.text() != self.password2Edit.text() or self.usernameEdit.text() == '':
            self.statusbar.showMessage('Неправильные данные')
            self.loginEdit.setText('')
            self.password1Edit.setText('')
            self.password2Edit.setText('')
            return

        if password_level(self.password1Edit.text()) != 'ok':
            self.statusbar.showMessage(password_level(self.password1Edit.text()))
            return

        logins = get_from_db(['login', 'user', 'id > 0'])
        logins = list(map(lambda x: x[0], logins))
        if self.loginEdit.text() in logins:
            self.statusbar.showMessage('Такой логин уже существует')
            return
        n = 0
        if self.comboBox.currentText() == 'Учитель':
            n = 1
        salt, hashed = hash_password(self.password1Edit.text())
        post_in_db(
            ['insert', 'user(login, username, password, status)',
             f'{self.loginEdit.text()} {self.usernameEdit.text()} {hashed} {n}'])
        post_in_db(['insert', 'salts(login, salt)', f'{self.loginEdit.text()} {salt}'])
        self.new_form = LogIn()
        self.new_form.show()
        self.close()


class StudentMenu(QMainWindow, Ui_StudentMenu):
    def __init__(self, login):
        super().__init__()
        self.next_form = None
        self.new_form = None
        self.setupUi(self)
        self.login = login
        self.startTestButton.clicked.connect(self.click)
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.new_form = LogIn()
        self.new_form.show()
        self.close()

    def click(self):
        keys = get_from_db(['key', 'test', 'id > 0'])
        keys = list(map(lambda x: x[0], keys))
        if self.codeEdit.text() not in keys:
            self.statusbar.showMessage('Ключ не действителен')
            return
        s = get_from_db(['t', 'test', f'key="{self.codeEdit.text()}"'])[0][0]
        self.next_form = Tester(s, self.login, self.codeEdit.text())
        self.next_form.show()
        self.close()


class NewTest(QMainWindow, Ui_NewTest):
    def __init__(self, login):
        super().__init__()
        self.copied = False
        self.answers = []
        self.login = login
        self.setupUi(self)
        self.addAnsButton.clicked.connect(self.add)
        self.cleaButton.clicked.connect(self.clear)
        self.loadButton.clicked.connect(self.load)
        self.pushButton.clicked.connect(self.back)
        # self.pushButton_2.clicked.connect(self.result)
        self.btn.clicked.connect(self.load_image)
        self.image = []
        self.counter = 0
        self.aditive = 0
        self.codeEdit.setText(generate_code())
        self.pushButton_3.clicked.connect(self.copy_code)
        self.comboBox.clear()
        items = ["1", "2", '3', '4', '5']
        self.comboBox.addItems(items)
        self.addAnsButton_2.clicked.connect(self.all_works)
        self.comboBox.setCurrentIndex(0)

    def copy_code(self):
        text = self.codeEdit.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.copied = True
        self.statusbar.showMessage('Код скопирован.')

    def load_image(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                    "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        print(image_path)
        self.image.append(['file', open(image_path, 'rb')])
        self.aditive = 1

    def all_works(self):
        self.next_form = Results(self.login)
        self.next_form.show()
        self.close()

    def back(self):
        self.next_form = LogIn()
        self.next_form.show()
        self.close()

    def add(self):
        if self.answerEdit.text() == '' or self.qwestionEdit.toPlainText() == '':
            self.statusbar.showMessage('Некорректные данные')
            self.qwestionEdit.setText('')
            self.answerEdit.setText('')
            return
        if self.aditive == 0:
            s = self.qwestionEdit.toPlainText() + f'&{self.comboBox.currentText()}&' + ',,,,' + self.answerEdit.text()
        else:

            s = self.qwestionEdit.toPlainText() + f'&{self.comboBox.currentText()}&' + f'i{self.counter}' + ',,,,' + self.answerEdit.text()  # i - изображение
            self.counter += self.aditive
        self.answers.append(s)
        self.qwestionEdit.setText('')
        self.answerEdit.setText('')
        self.statusbar.showMessage('Вопрос добавлен')

    def clear(self):
        self.answerEdit.setText('')
        self.qwestionEdit.setText('')

    def load(self):
        if not self.copied:
            self.statusbar.showMessage('Скопируйте код.')
            return
        if self.name_of_work.text() == '':
            self.statusbar.showMessage('Напишите название работы.')
            return
        if len(self.answers) == 0:
            self.statusbar.showMessage('Нет вопросов')
            return
        if self.codeEdit.text() == '':
            self.statusbar.showMessage('Пустое поле кода теста')
            return

        keys = get_from_db(['key', 'test', 'id > 0'])
        keys = list(map(lambda x: x[0], keys))
        if self.codeEdit.text() in keys:
            self.statusbar.showMessage('Ваш ключ не уникален')
            return
        self.answers = '***'.join(self.answers)
        for i in range(len(self.image)):
            if i == 0:
                self.image[i][0] = self.codeEdit.text()
            else:
                self.image[i][0] = f'file{i}'
            self.image[i] = tuple(self.image[i])
        post_in_db(['insert', 'test(key, t, author)', f'{self.codeEdit.text()} {self.answers} {self.login}'])
        post_images(files=self.image)
        post_in_db(['insert', 'works(key, name)', f'{self.codeEdit.text()} {self.name_of_work.text()}'])
        self.statusbar.showMessage('Проверочная создана успешно')


class Results(QMainWindow, Ui_Res):
    def __init__(self, login):
        super().__init__()
        self.new_form = None
        self.answers = []
        self.login = login
        self.setupUi(self)
        self.pushButton.clicked.connect(self.back)
        keys = get_from_db(['key', 'test', f'author="{self.login}"'])
        print(keys)
        s = ''
        for key in keys:
            key = key[0]
            try:
                work = get_from_db(['name', 'works', f'key="{key}"'])[0][0]
            except:
                work = 'Нет названия'
            s += f'Название работы: {work}, ключ работы: {key}' + '\n'

        self.textBrowser.setText(s)

    def back(self):
        self.new_form = NewTest(self.login)
        self.new_form.show()
        self.close()


class Tester(QMainWindow, Ui_Tester):
    def __init__(self, test, login, key):
        super().__init__()
        self.setupUi(self)
        self.login = login
        self.key = key
        print(self.key)
        self.results = []
        # Внутри test пары вопрос ответ через *** а внутри через ,,,,
        self.test = test.split('***')
        self.test = list(map(lambda x: x.split(',,,,'), self.test))
        print('self.test:', self.test)
        self.user_answers = ['' for _ in range(len(self.test))]
        self.saveButton.clicked.connect(self.save)
        self.previewButton.clicked.connect(self.preview)
        self.nextButton.clicked.connect(self.next)
        self.endButton.clicked.connect(self.end)
        self.current_qwe = 0
        self.index = -1
        if 'i' in self.test[self.current_qwe][0]:
            self.index = self.test[self.current_qwe][0][self.test[self.current_qwe][0].index('i') + 1:]
        self.qwestionText.setText(self.test[self.current_qwe][0][:self.test[self.current_qwe][0].index('&')])
        self.max_qwe = len(self.test) - 1
        self.pushButton.clicked.connect(self.back)
        if self.index != -1:
            s = '\\'
            filename = f'images{s}{self.key}{self.index}'
            response = get_img({'filename': filename})
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.label_3.mousePressEvent = lambda event: self.view_image("temp_image.jpg")

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
        self.next_form = StudentMenu(self.login)
        self.next_form.show()
        self.close()

    def save(self):
        self.statusbar.showMessage('')
        self.user_answers[self.current_qwe] = self.answerEdit.text()

    def preview(self):
        if self.current_qwe == 0:
            self.statusbar.showMessage('Некорректный запрос')
            return
        self.statusbar.showMessage('')
        self.current_qwe = self.current_qwe - 1
        if 'i' in self.test[self.current_qwe][0]:
            self.index = self.test[self.current_qwe][0][self.test[self.current_qwe][0].index('i') + 1:]
        self.qwestionText.setText(self.test[self.current_qwe][0][:self.test[self.current_qwe][0].index('&')])
        if self.index != -1:
            s = '\\'
            filename = f'images{s}{self.key}{self.index}'
            response = get_img({'filename': filename})
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def next(self):
        if self.current_qwe + 1 > self.max_qwe:
            self.statusbar.showMessage('Некорректный запрос')
            return
        self.statusbar.showMessage('')
        self.current_qwe = self.current_qwe + 1
        if 'i' in self.test[self.current_qwe][0]:
            self.index = self.test[self.current_qwe][0][self.test[self.current_qwe][0].index('i') + 1:]
        self.qwestionText.setText(self.test[self.current_qwe][0][:self.test[self.current_qwe][0].index('&')])
        if self.index != -1:
            s = '\\'
            filename = f'images{s}{self.key}{self.index}'
            response = get_img({'filename': filename})
            file = open("temp_image.jpg", "wb")
            file.write(response.content)
            pixmap = QPixmap("temp_image.jpg")
            self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.answerEdit.setText('')

    def end(self):
        logins = get_from_db(['logins', 'test', f'key="{self.key}"'])[0][0]
        if logins is not None:
            if self.login in logins.split('***'):
                self.statusbar.showMessage('Вы уже выполнили тестирование')
                return
        sp = []
        for i in range(self.max_qwe + 1):
            if self.user_answers[i] == self.test[i][1]:
                test_i = self.test[i][0]
                sp.append([int(test_i[test_i.index('&') + 1:test_i.index('&') + 2]), True])
            else:
                test_i = self.test[i][0]
                sp.append([int(test_i[test_i.index('&') + 1:test_i.index('&') + 2]), False])
        res = self.login + repr(sp)
        res = res.replace(',', '%')
        pre = get_from_db(['results', 'test', f'key="{self.key}"'])[0][0]
        if pre is None:
            pre = res + '***'
        else:
            pre += res + '***'
        # print(pre)
        post_in_db(['update', 'test', f'results="{pre}"', f'key="{self.key}"'])
        # print(['update', 'test', f'results="{pre}"', f'key="{self.key}"'])
        pre = get_from_db(['logins', 'test', f'key="{self.key}"'])[0][0]
        if pre is None:
            pre = self.login + '***'
        else:
            pre += self.login + '***'
        post_in_db(['update', 'test', f'logins="{pre}"', f'key="{self.key}"'])
        self.statusbar.showMessage('Работа завершена')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstMenu()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
