import hashlib
import os
import ast

from flask import Flask, request, send_file, jsonify
import sqlite3
import json

app = Flask(__name__)


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


@app.route('/registration', methods=['POST'])
def registration():
    if request.is_json:
        data = request.get_json()
        login = data['login']
        password = data['password']
        username = data['username']
        status = data['status']
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        logins = cur.execute('''select login from user where id > 0''').fetchall()
        logins = list(map(lambda x: x[0], logins))
        print(logins)
        if login in logins:
            return jsonify({"message": "Такой логин уже существует"}), 300
        n = 0
        if status == 'Учитель':
            n = 1
        salt, hashed = hash_password(password)
        try:
            cur.execute('insert into user(login, username, password, status) values(?, ?, ?, ?)',
                        [login, username, hashed, n])
            cur.execute('''insert into salts(login, salt) values(?, ?)''', [login, salt])
            con.commit()
            return jsonify({"message": "Пользователь зарегистрирован"}), 200
        except:
            return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/log_in', methods=['POST'])
def log_in():
    try:
        data = request.get_json()
        login = data['login']
        password = data['password']
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        logins = cur.execute('select login from user where id > 0')
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Неправильный логин или пароль"}), 300
        salt = cur.execute(f'select salt from salts where login="{login}"')
        salt = list(map(lambda x: x[0], salt))[0]
        hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Неправильный логин или пароль"}), 300
        status = cur.execute(f'select status from user where login="{login}"').fetchall()[0][0]
        con.commit()
        return jsonify({'status': status}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/new_test', methods=['POST'])
def new_test():
    data = request.get_json()
    login = data['login']
    password = data['password']
    key = data['key']
    name_of_work = data['name_of_work']
    answers = repr(data['answers'])
    questions = repr(data['questions'])
    points = repr(data['points'])
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    logins = cur.execute('select login from user where id > 0').fetchall()
    logins = list(map(lambda x: x[0], logins))
    if login not in logins:
        return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
    try:
        hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
        salt = cur.execute(f'select salt from salts where login="{login}"')
        salt = list(map(lambda x: x[0], salt))[0]
    except:
        return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
    eq_pass = verify_password(password, salt, hashed)
    if not eq_pass:
        return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

    try:
        cur.execute('insert into test(key, questions, answers, points, author) values(?, ?, ?, ?, ?)',
                    [key, questions, answers, points, login])
        cur.execute('insert into works(key, name) values(?, ?)', [key, name_of_work])
        con.commit()
        return jsonify({"message": "Работа успешно загружена"}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/load_images/<key>/<login>/<password>/<status>', methods=['POST'])
def load_images(key, login, password, status):
    print(key, login, password, status)
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    logins = cur.execute('select login from user where id > 0').fetchall()
    logins = list(map(lambda x: x[0], logins))
    if login not in logins:
        return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
    try:
        hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
        salt = cur.execute(f'select salt from salts where login="{login}"')
        salt = list(map(lambda x: x[0], salt))[0]
    except:
        return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
    eq_pass = verify_password(password, salt, hashed)
    if not eq_pass:
        return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

    if status == 'teacher':
        try:
            files = dict(request.files)
            for index in files.keys():
                image = files[index]
                image.save(f'images/{key}{index}.jpg')
            return jsonify({"message": "Работа успешно загружена"}), 200
        except:
            return jsonify({"message": "Упс, что-то пошло не так..."}), 500
    else:
        try:
            files = dict(request.files)
            for index in files.keys():
                image = files[index]
                image.save(f'images/{key}_{login}{index}.jpg')
            return jsonify({"message": "Работа успешно загружена"}), 200
        except:
            return jsonify({"message": "Упс, что-то пошло не так..."}), 500

@app.route('/results', methods=['POST'])
def results():
    try:
        data = request.get_json()
        login = data['login']
        password = data['password']
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        keys = cur.execute(f'select key from test where author="{login}"').fetchall()
        keys = list(map(lambda x: x[0], keys))
        response = ''
        for key in keys:
            work = cur.execute(f'select name from works where key="{key}"').fetchall()[0][0]
            response += f'Название работы: {work}, ключ работы: {key}' + '\n'''
        return jsonify({"message": response}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/student_menu', methods=['POST'])
def student_menu():
    try:
        data = request.get_json()
        login = data['login']
        password = data['password']
        key = data['key']
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        keys = cur.execute(f'select key from test where id > 0').fetchall()
        keys = list(map(lambda x: x[0], keys))
        if key not in keys:
            return jsonify({"message": "Ключ не действителен"}), 300
        logins = cur.execute(f'select logins from test where key="{key}"').fetchall()[0][0]
        if logins is None:
            logins = []
        else:
            logins = ast.literal_eval(logins)
        if login in logins:
            return jsonify({"message": "Вы уже писали эту работу"}), 300
        return jsonify({"message": "Всё хорошо."}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/tester', methods=['POST'])
def tester():
    try:
        data = request.get_json()
        login = data['login']
        password = data['password']
        key = data['key']
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        questions = ast.literal_eval(cur.execute(f'select questions from test where key="{key}"').fetchall()[0][0])
        answers = ast.literal_eval(cur.execute(f'select answers from test where key="{key}"').fetchall()[0][0])
        points = ast.literal_eval(cur.execute(f'select points from test where key="{key}"').fetchall()[0][0])
        pre = cur.execute(f'select results from test where key="{key}"').fetchall()[0][0]
        if pre == '':
            pre = []
        else:
            pre = ast.literal_eval(pre)
        con.commit()
        return jsonify({"questions": questions,
                        'answers': answers,
                        'points': points,
                        'pre': pre}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/send_image', methods=['GET'])
def send_image():
    try:
        data = ast.literal_eval(request.get_json())
        filename = data['filename']
        login = data['login']
        password = data['password']

        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        try:
            return send_file(filename + '.jpg', mimetype='image/jpeg')
        except:
            return '0'
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/update_results', methods=['POST'])
def update_results():
    try:
        data = request.get_json()
        login = data['login']
        res = data['res']
        key = data['key']
        password = data['password']
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        logins = cur.execute(f'select logins from test where key="{key}"').fetchall()[0][0]
        if logins is None:
            logins = []
        else:
            logins = ast.literal_eval(logins)
        pre = cur.execute(f'select results from test where key="{key}"').fetchall()[0][0]
        if pre == '':
            pre = []
        else:
            pre = ast.literal_eval(pre)
        if login in logins:
            return jsonify({"message": "Кажется, вы уже отправляли эту работу"}), 300
        pre.append(res)
        cur.execute(f'update test set results="{repr(pre)}" where key="{key}"')
        pre_log = cur.execute(f'select logins from test where key="{key}"').fetchall()[0][0]
        if pre_log is None:
            pre_log = []
        else:
            pre_log = ast.literal_eval(pre_log)
        pre_log.append(login)
        cur.execute(f'update test set logins="{repr(pre_log)}" where key="{key}"')
        con.commit()
        return jsonify({"message": "Работа завершена"}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500



@app.route('/tg', methods=['POST'])
def tg():
    try:
        data = request.get_json()
        login = data['login']
        chat_id = data['chat_id']
        password = data['password']

        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
        logins = cur.execute('select login from tg where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        tg_ids = cur.execute('select tg_id from tg where id > 0').fetchall()
        tg_ids = list(map(lambda x: x[0], tg_ids))
        if chat_id in tg_ids:
            cur.execute(f'update tg set tg_id="-1" where tg_id="{chat_id}"')
        if login in logins:
            cur.execute(f'update tg set tg_id="{chat_id}" where login="{login}"')
        else:
            cur.execute('insert into tg(login, password, tg_id) values(?, ?, ?)', [login, hashed, chat_id])
        con.commit()
        return jsonify({"message": "Вы зарегистрировались"}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/get_res', methods=['POST'])
def get_res():
    try:
        data = request.get_json()
        key = data['key']
        chat_id = data['chat_id']
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        login = cur.execute(f'select login from tg where tg_id="{chat_id}"').fetchall()[0][0]
        result = cur.execute(f'select results from test where author="{login}" and key="{key}"').fetchall()[0][0]
        result = ast.literal_eval(result)
        for i in range(len(result)):
            username = cur.execute(f'select username from user where login="{result[i][0]}"').fetchall()[0][0]
            result[i][0] = username
        points = cur.execute(f'select points from test where author="{login}" and key="{key}"').fetchall()[0][0]
        if len(result) == 0:
            return jsonify({"message": "К сожалению я не нашёл такой работы или результатов пока что нет"}), 300
        return jsonify({"result": result, 'points': ast.literal_eval(points)}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500

@app.route('/to_check_work', methods=['POST'])
def to_check_work():
    try:
        data = request.get_json()
        login = data['login']
        password = data['password']
        key = data['key']

        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        author = cur.execute(f'select author from test where key="{key}"').fetchall()
        #[0][0]
        if author == []:
            return jsonify({"message": "Что-то не так с ключом"}), 300
        print(author)
        author = author[0][0]
        if author != login:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        return jsonify({"message": "Всё хорошо."}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500



@app.route('/logins_by_key', methods=['POST'])
def logins_by_key():
    try:
        data = request.get_json()
        login = data['login']
        password = data['password']
        key = data['key']

        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        logins = cur.execute(f'select logins from test where key="{key}"').fetchall()[0][0]
        if logins is None:
            logins = []
        else:
            logins = ast.literal_eval(logins)
        usernames = []
        for login in logins:
            username = cur.execute(f'select username from user where login="{login}"').fetchall()[0][0]
            usernames.append(username)
        return jsonify({"logins": logins, 'usernames': usernames}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500


@app.route('/big_update', methods=['POST'])
def big_update():
    try:
        data = request.get_json()
        login = data['login']
        pre = data['res']
        key = data['key']
        password = data['password']
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        logins = cur.execute('select login from user where id > 0').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if login not in logins:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        try:
            hashed = cur.execute(f'select password from user where login="{login}"').fetchall()[0][0]
            salt = cur.execute(f'select salt from salts where login="{login}"')
            salt = list(map(lambda x: x[0], salt))[0]
        except:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300
        eq_pass = verify_password(password, salt, hashed)
        if not eq_pass:
            return jsonify({"message": "Что-то не так с вашей учётной записью"}), 300

        cur.execute(f'update test set results="{repr(pre)}" where key="{key}"')
        con.commit()
        return jsonify({"message": "Всё получилось."}), 200
    except:
        return jsonify({"message": "Упс, что-то пошло не так..."}), 500




if __name__ == '__main__':
    app.run(debug=True)
