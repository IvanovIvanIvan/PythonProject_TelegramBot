import telebot
from telebot import types
import sqlite3
import reqs

bot = reqs.bot


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Реализованы следующие команды: \n /start - Приветствие пользователя \n"
    +"/signin - регистрация или вход в аккаунт. Запрашивается, в первый ли раз пользователь заходит в бота, если да, то ему предлагается выбрать имя пользователя и пароль, иначе - войти в аккаунт. \n"
    +"/create - создание новой записи. Работает только, если пользователь вошёл в аккаунт. После написания команды предлагается выбрать заголовок для записи, а затем написать её текст. \n"
    +"/edit - редактирование записи. Работает только, если пользователь вошёл в аккаунт. После написания команды бот присылает список уже созданных записей и предлагает выбрать, какую необходимо отредактировать, затем предлагает написать новый текст записи. \n"
    +"/read - чтение записи. Работает только, если пользователь вошёл в аккаунт. После написания команды бот присылает список уже созданных записей и предлагает выбрать, какую необходимо прочитать. Затем, отправляет пользователю текст необходимой записи. \n"
    +"/delete - удаление записи. Работает только, если пользователь вошёл в аккаунт. После написания команды бот присылает список уже созданных записей и предлагает выбрать, какую необходимо удалить. \n"
    +"/export - экспорт записи. Работает только, если пользователь вошёл в аккаунт. После написания команды бот присылает список уже созданных записей и предлагает выбрать, какую необходимо экспортировать. Затем, отправляет пользователю .txt файл необходимой записи. \n"
    +"/logout - выход из аккаунта. \n"
    +"/deluser - удаление пользователя.")


@bot.message_handler(commands=['start'])
def reply(message):
    bot.send_message(message.chat.id, 'Hello! If you want to find out about the bot, type /help')


@bot.message_handler(commands=['signin'])
def main(message):
    base = sqlite3.connect('DiaryBot.db')
    cur = base.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(50) primary key, password varchar (50))')
    base.commit()
    cur.close()
    base.close()
    bot.register_next_step_handler(message, reqs.answer)

    bot.send_message(message.chat.id, 'Hello! Is it your first time using DiaryBot?')


@bot.message_handler(commands=['create'])
def entry(message):
    if reqs.signedin:
        bot.send_message(message.chat.id, 'Choose a heading for the entry')
        bot.register_next_step_handler(message, reqs.creating)
    else:
        bot.send_message(message.chat.id, 'You have to sign in first')


@bot.message_handler(commands=['edit'])
def entry(message):
    if reqs.signedin:
        diary = sqlite3.connect(reqs.name + '.db')
        curs = diary.cursor()
        curs.execute("SELECT date FROM entries")
        ansl = curs.fetchall()
        diary.commit()
        curs.close()
        diary.close()
        anss = ""
        for ans in ansl:
            anss+=ans[0]
            anss+='\n'
        if anss=="":
            bot.send_message(message.chat.id, "You haven't created any entries yet")
        else:
            bot.send_message(message.chat.id, anss)
            bot.send_message(message.chat.id, 'Choose an entry you want to edit')
            bot.register_next_step_handler(message, reqs.editing)
    else:
        bot.send_message(message.chat.id, 'You have to sign in first')


@bot.message_handler(commands=['read'])
def entry(message):
    if reqs.signedin:
        diary = sqlite3.connect(reqs.name + '.db')
        curs = diary.cursor()
        curs.execute("SELECT date FROM entries")
        ansl = curs.fetchall()
        diary.commit()
        curs.close()
        diary.close()
        anss = ""
        for ans in ansl:
            anss+=ans[0]
            anss+='\n'
        if anss=="":
            bot.send_message(message.chat.id, "You haven't created any entries yet")
        else:
            bot.send_message(message.chat.id, anss)
            bot.send_message(message.chat.id, 'Choose an entry you want to read')
            bot.register_next_step_handler(message, reqs.reading)
    else:
        bot.send_message(message.chat.id, 'You have to sign in first')
  

@bot.message_handler(commands=['delete'])
def entry(message):
    if reqs.signedin:
        diary = sqlite3.connect(reqs.name + '.db')
        curs = diary.cursor()
        curs.execute("SELECT date FROM entries")
        ansl = curs.fetchall()
        diary.commit()
        curs.close()
        diary.close()
        anss = ""
        for ans in ansl:
            anss+=ans[0]
            anss+='\n'
        if anss=="":
            bot.send_message(message.chat.id, "You haven't created any entries yet")
        else:
            bot.send_message(message.chat.id, anss)
            bot.send_message(message.chat.id, 'Choose an entry you want to delete')
            bot.register_next_step_handler(message, reqs.deleting)
    else:
        bot.send_message(message.chat.id, 'You have to sign in first')


@bot.message_handler(commands=['logout'])
def entry(message):
    if reqs.signedin:
        reqs.signedin = False
        bot.send_message(message.chat.id, 'Come back later!')
    else:
        bot.send_message(message.chat.id, 'You have to sign in first')


@bot.message_handler(commands=['deluser'])
def entry(message):
    if reqs.signedin:
        reqs.signedin = False
        base = sqlite3.connect('DiaryBot.db')
        cur = base.cursor()
        cur.execute("DELETE FROM users where name = '%s'" % reqs.name)
        base.commit()
        cur.close()
        base.close()
        bot.send_message(message.chat.id, 'Account successfully deleted')
    else:
        bot.send_message(message.chat.id, 'You have to sign in first')


@bot.message_handler(commands=['export'])
def entry(message):
    if reqs.signedin:
        diary = sqlite3.connect(reqs.name + '.db')
        curs = diary.cursor()
        curs.execute("SELECT date FROM entries")
        ansl = curs.fetchall()
        diary.commit()
        curs.close()
        diary.close()
        anss = ""
        for ans in ansl:
            anss+=ans[0]
            anss+='\n'
        if anss=="":
            bot.send_message(message.chat.id, "You haven't created any entries yet")
        else:
            bot.send_message(message.chat.id, anss)
            bot.send_message(message.chat.id, 'Choose an entry you want to export')
            bot.register_next_step_handler(message, reqs.exporting)
    else:
        bot.send_message(message.chat.id, 'You have to sign in first')


bot.polling(none_stop=True)