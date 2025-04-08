import telebot
from telebot import types
import requests
import json
import pandas as pd

bot = telebot.TeleBot('token')


def get_from_db(data):
    data = json.dumps(data)
    return requests.get('http://127.0.0.1:5000', data=data).json()


def post_in_db(data):
    data = json.dumps(data)
    requests.post('http://127.0.0.1:5000/', data=data)
    return None


def sign_up(message):
    login, password = message.text.split()
    logins = get_from_db(['login', 'user', 'id > 0'])
    logins = list(map(lambda x: x[0], logins))
    passwords = get_from_db(['password', 'user', f'login="{login}"'])
    passwords = list(map(lambda x: x[0], passwords))
    markup = types.InlineKeyboardMarkup()
    reg = types.InlineKeyboardButton('Попробовать ещё', callback_data='chance')
    back_to_menu = types.InlineKeyboardButton('Вернуться в меню', callback_data='back')
    markup.add(reg)
    markup.add(back_to_menu)
    if login not in logins:
        bot.send_message(message.chat.id, 'Такой логин не зарегистрирован.', reply_markup=markup)
    elif password not in passwords:
        bot.send_message(message.chat.id, 'Неправильный пароль', reply_markup=markup)
    else:
        try:
            logins = get_from_db(['login', 'tg', f'true'])
            tg_ids = get_from_db(['tg_id', 'tg', 'true'])
            print(logins, login)
            if [message.chat.id] in tg_ids:
                post_in_db(['update', 'tg', 'tg_id="-1"', f'tg_id="{message.chat.id}"'])
            if [login] in logins:
                post_in_db(['update', 'tg', f'tg_id="{message.chat.id}"', f'login="{login}"'])
                bot.send_message(message.chat.id, 'Вы успешно зарегистрировались, уже начинаем продавать ваши персональные данные')
            else:
                post_in_db(['insert', 'tg(login, password, tg_id)', f'{login} {password} {message.chat.id}'])
                bot.send_message(message.chat.id, 'Вы успешно зарегистрировались, уже начинаем продавать ваши персональные данные')
        except:
            bot.send_message(message.chat.id, 'Упс, что-то пошло не так')


def results(message):
    key = message.text
    login = get_from_db(['login', 'tg', f'tg_id="{message.chat.id}"'])
    login = list(map(lambda x: x[0], login))[0]
    result = get_from_db(['results', 'test', f'author="{login}" and key="{key}"'])
    result = list(map(lambda x: x[0], result))
    if len(result) == 0:
        markup = types.InlineKeyboardMarkup()
        reg = types.InlineKeyboardButton('Отправить код ещё раз', callback_data='check_results')
        back_to_menu = types.InlineKeyboardButton('Вернуться в меню', callback_data='back')
        markup.add(reg)
        markup.add(back_to_menu)
        bot.send_message(message.chat.id, 'К сожалению я не нашёл такой работы', reply_markup=markup)
    else:
        result = result[0].rstrip('***').split('***')
        print(result)
        for i in range(len(result)):
            result[i] = result[i].split(',,')
            login = result[i][0]
            username = get_from_db(['username', 'user', f'login="{login}"'])[0][0]
            result[i][0] = username
            result[i] = ';'.join(result[i])
        print(result)



        result = '\n'.join(result)
        parsed_data = []
        for entry in result:
            name, tasks = entry.split(";")
            correct, total = tasks.split(" of ")
            correct = int(correct)
            total = int(total)
            percentage = (correct / total) * 100  # Процент выполнения
            recommended_grade = "Отлично" if percentage >= 90 else "Хорошо" if percentage >= 70 else "Удовлетворительно" if percentage >= 50 else "Неудовлетворительно"  # Рекомендуемая оценка
            parsed_data.append({
                "Имя": name,
                "Верные задачи": correct,
                "Общее количество задач": total,
                "Процент выполнения": percentage,
                "Рекомендуемая оценка": recommended_grade
            })

        # Создаем DataFrame
        df = pd.DataFrame(parsed_data)

        # Сохраняем DataFrame в файл Excel
        df.to_excel("результаты.xlsx", index=False, sheet_name="Результаты")

        print("Файл 'результаты.xlsx' успешно создан!")




        markup = types.InlineKeyboardMarkup()
        back_to_menu = types.InlineKeyboardButton('Вернуться в меню', callback_data='back')
        markup.add(back_to_menu)
        bot.send_message(message.chat.id, result, reply_markup=markup)




@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    reg = types.InlineKeyboardButton('Регистрация', callback_data='registration')
    check_res = types.InlineKeyboardButton('Узнать результаты работы', callback_data='check_results')
    markup.add(reg)
    markup.add(check_res)
    bot.send_message(message.chat.id, 'Меню бота', reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def message_reply(call):
    if call.data == 'registration':
        m = bot.send_message(call.message.chat.id, 'Введие логин и пароль')
        bot.register_next_step_handler(m, sign_up)
    if call.data == 'check_results':
        m = bot.send_message(call.message.chat.id, 'Введите код доступа к вашей проверочной работе')
        bot.register_next_step_handler(m, results)
    if call.data == 'chance':
        m = bot.send_message(call.message.chat.id, 'И ещё одна попыточка)')
        bot.register_next_step_handler(m, sign_up)
    if call.data == 'back':
        start_message(call.message)



bot.infinity_polling()
