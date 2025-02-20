import sys
import requests
import json

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from log_in import *
from new_test import *
from registration import *
from start import *
from student_menu import *
from tester import *
from res import *
from PyQt5.QtGui import QPixmap


# from bot import send_result


def password_level(password):
    return 'ok'


def get_from_db(data):
    data = json.dumps(data)
    return requests.get('http://127.0.0.1:5000', data=data).json()


def post_in_db(data):
    data = json.dumps(data)
    requests.post('http://127.0.0.1:5000/', data=data)
    return None


class FirstMenu(QMainWindow, Ui_start):
    def __init__(self):
        super().__init__()
        self.next_form = None
        self.setupUi(self)
        self.log_in.clicked.connect(self.log)
        self.registration.clicked.connect(self.reg)
        self.pixmap = QPixmap('my.png').scaled(300, 300)
        self.label.resize(300, 300)
        self.label.move(100, 300)
        self.label.setPixmap(self.pixmap)

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
        passwords = get_from_db(['password', 'user', f'login="{login}"'])
        passwords = list(map(lambda x: x[0], passwords))
        if login not in logins or password not in passwords:
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
        post_in_db(
            ['insert', 'user(login, username, password, status)', f'{self.loginEdit.text()} {self.usernameEdit.text()} {self.password1Edit.text()} {n}'])
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
        self.answers = []
        self.login = login
        self.setupUi(self)
        self.addAnsButton.clicked.connect(self.add)
        self.cleaButton.clicked.connect(self.clear)
        self.loadButton.clicked.connect(self.load)
        self.pushButton.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.result)

    def result(self):

        self.next_form = Results(self.login, self.codeEdit.text())
        self.next_form.show()
        self.close()

    def back(self):
        self.next_form = LogIn()
        self.next_form.show()
        self.close()

    def add(self):
        if self.answerEdit.text() == '' or self.qwestionEdit.text() == '':
            self.statusbar.showMessage('Некорректные данные')
            self.qwestionEdit.setText('')
            self.answerEdit.setText('')
            return
        s = self.qwestionEdit.text() + ',,,,' + self.answerEdit.text()
        self.answers.append(s)
        self.qwestionEdit.setText('')
        self.answerEdit.setText('')

    def clear(self):
        self.answerEdit.setText('')
        self.qwestionEdit.setText('')

    def load(self):
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
        post_in_db(['insert', 'test(key, t, author)', f'{self.codeEdit.text()} {self.answers} {self.login}'])
        self.statusbar.showMessage('Проверочная создана успешно')


class Results(QMainWindow, Ui_Res):
    def __init__(self, login, code):
        super().__init__()
        self.code = code
        self.new_form = None
        self.answers = []
        self.login = login
        self.setupUi(self)
        self.pushButton.clicked.connect(self.back)
        res = get_from_db(['results', 'test', f'author="{self.login}" and key="{self.code}"'])
        if not res:
            self.statusbar.showMessage('результатов по такому коду не найдено')
            return
        else:
            res = res[0][0]
        res = res.split(',,')
        res[1] = res[1].split('***')
        res[1] = '\n'.join(res[1])
        res = ';'.join(res)
        f = open(f't{self.code}.txt', mode='w')
        f1 = open(f't{self.code}.txt', mode='r')
        f.write(res)
        f.close()
        res = f1.read()
        self.textBrowser.setText(res)

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
        self.results = []
        # Внутри test пары вопрос ответ через *** а внутри через ,,,,
        self.test = test.split('***')
        self.test = list(map(lambda x: x.split(',,,,'), self.test))
        self.user_answers = ['' for _ in range(len(self.test))]
        self.saveButton.clicked.connect(self.save)
        self.previewButton.clicked.connect(self.preview)
        self.nextButton.clicked.connect(self.next)
        self.endButton.clicked.connect(self.end)
        self.current_qwe = 0
        self.qwestionText.setText(self.test[self.current_qwe][0])
        self.max_qwe = len(self.test) - 1
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.next_form = StudentMenu(self.login)
        self.next_form.show()
        self.close()

    def save(self):
        self.user_answers[self.current_qwe] = self.answerEdit.text()

    def preview(self):
        if self.current_qwe == 0:
            self.statusbar.showMessage('Некорректный запрос')
            return
        self.current_qwe = self.current_qwe - 1
        self.qwestionText.setText(self.test[self.current_qwe][0])

    def next(self):
        if self.current_qwe + 1 > self.max_qwe:
            self.statusbar.showMessage('Некорректный запрос')
            return
        self.current_qwe = self.current_qwe + 1
        self.qwestionText.setText(self.test[self.current_qwe][0])
        self.answerEdit.setText('')

    def end(self):
        logins = get_from_db(['logins', 'test', f'key="{self.key}"'])[0][0]
        if logins is not None:
            if self.login in logins.split('***'):
                self.statusbar.showMessage('Вы уже выполнили тестирование')
                return
        for i in range(self.max_qwe + 1):
            if self.user_answers[i] == self.test[i][1]:
                self.results.append(True)
            else:
                self.results.append(False)
        res = self.login + ',,' + str(self.results.count(True)) + ' of ' + str(len(self.results))
        pre = get_from_db(['results', 'test', f'key="{self.key}"'])[0][0]
        if pre is None:
            pre = res + '***'
        else:
            pre += res + '***'
        print(pre)
        post_in_db(['update', 'test', f'results="{pre}"', f'key="{self.key}"'])
        pre = get_from_db(['logins', 'test', f'key="{self.key}"'])[0][0]
        if pre is None:
            pre = self.login + '***'
        else:
            pre += self.login + '***'
        post_in_db(['update', 'test', f'logins="{pre}"', f'key="{self.key}"'])
        self.statusbar.showMessage('Ваш ответ записан')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstMenu()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
