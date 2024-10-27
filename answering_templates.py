import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7058086495:AAEFiEvwp6q0elBLXc4zP4H9Jw4lFoe6o2A')

signedin = False
date = ''
name = ''
password = ''


def answer(message):
    if message.text.lower() == 'yes':
        bot.send_message(message.chat.id, 'OK, please enter your name to sign up')
        bot.register_next_step_handler(message, signame)
    if message.text.lower() == 'no':
        bot.send_message(message.chat.id, 'OK, please enter your name to log in')
        bot.register_next_step_handler(message, logname)


def signame(message):
    global name
    name = message.text.strip()
    base = sqlite3.connect('DiaryBot.db')
    cur = base.cursor()
    exists = cur.execute("SELECT * FROM users WHERE name = '%s'" % name).fetchall()
    base.commit()
    cur.close()
    base.close()

    if not exists:
        bot.send_message(message.chat.id, 'Nice to meet you, ' + name + '. ' + 'Now, choose a password')
        diary = sqlite3.connect(name + '.db')
        curs = diary.cursor()
        curs.execute('CREATE TABLE IF NOT EXISTS entries (date varchar(50) primary key, entry varchar (1000))')
        diary.commit()
        curs.close()
        diary.close()
        bot.register_next_step_handler(message, passname)
    else:
        bot.send_message(message.chat.id, 'This username is already taken, please, try another one')
        bot.register_next_step_handler(message, signame)


def passname(message):
    global name
    global signedin
    password = message.text.strip()

    base = sqlite3.connect('DiaryBot.db')
    cur = base.cursor()

    cur.execute("INSERT INTO users (name, password) VALUES ('%s', '%s')" % (name, password))
    base.commit()
    cur.close()
    base.close()

    signedin = True
    bot.send_message(message.chat.id, 'All set up! Have a nice time using our bot!')


def logname(message):
    global name
    name = message.text.strip()
    base = sqlite3.connect('DiaryBot.db')
    cur = base.cursor()
    exists = cur.execute("SELECT * FROM users WHERE name = '%s'" % name).fetchall()
    base.commit()
    cur.close()
    base.close()

    if exists:

        diary = sqlite3.connect(name + '.db')
        curs = diary.cursor()
        curs.execute('CREATE TABLE IF NOT EXISTS entries (date varchar(50) primary key, entry varchar (1000))')
        diary.commit()
        curs.close()
        diary.close()

        bot.send_message(message.chat.id, 'Nice to meet you, ' + name + '. ' + 'Enter your password, please')
        bot.register_next_step_handler(message, passlog)
    else:
        bot.send_message(message.chat.id, 'This username is not found, please, try again')


def passlog(message):
    global signedin
    global name
    global password
    password = message.text.strip()

    base = sqlite3.connect('DiaryBot.db')
    cur = base.cursor()

    checker = cur.execute("SELECT * FROM users WHERE (name, password) = ('%s', '%s')" % (name, password)).fetchone()
    base.commit()
    cur.close()
    base.close()

    if checker == (name, password):
        signedin = True
        bot.send_message(message.chat.id, 'All set up! Have a nice time using our bot!')
    else:
        bot.send_message(message.chat.id, 'Wrong password, please, try again. Use the commanв /signin')


def creating(message):
    global name
    global date
    global signedin
    date = message.text.strip()
    if date == '':
        bot.send_message(message.chat.id, 'You have to choose a name for the entry')
    else:
        diary = sqlite3.connect(name + '.db')
        curs = diary.cursor()
        exists = curs.execute("SELECT * FROM entries WHERE date = '%s'" % date).fetchall()
        diary.commit()
        curs.close()
        diary.close()
        if not exists:
            bot.send_message(message.chat.id, 'What would you like to write?')
            bot.register_next_step_handler(message, writing)
        else:
            bot.send_message(message.chat.id, 'You have already created an entry with this heading, please choose another one')


def writing(message):
    global date 
    global name
    diary = sqlite3.connect(name + '.db')
    strentry = message.text
    curs = diary.cursor()
    curs.execute("INSERT INTO entries (date, entry) VALUES ('%s', '%s')" % (date, strentry))
    diary.commit()
    curs.close()
    diary.close()
    bot.send_message(message.chat.id, '👌')


def editing(message):
    global date
    global name
    global signedin
    date = message.text.strip()
    diary = sqlite3.connect(name + '.db')
    curs = diary.cursor()
    exists = curs.execute("SELECT * FROM entries WHERE date = '%s'" % date).fetchall()
    diary.commit()
    if exists:
        bot.send_message(message.chat.id, 'What would you like to write?')
        curs.execute("DELETE FROM entries WHERE date = '%s'" % date)
        diary.commit()
        curs.close()
        diary.close()
        bot.register_next_step_handler(message, writing)
    else:
        bot.send_message(message.chat.id, 'There are no entries with such heading, if you want to create one, please use the command /create')


def reading(message):
    global date
    global name
    global signedin
    date = message.text.strip()
    diary = sqlite3.connect(name + '.db')
    curs = diary.cursor()
    exists = curs.execute("SELECT * FROM entries WHERE date = '%s'" % date).fetchall()
    diary.commit()
    if exists:
        entrytup = curs.execute("SELECT entry FROM entries WHERE date = '%s'" % date).fetchone()
        diary.commit()
        curs.close()
        diary.close()
        bot.send_message(message.chat.id, date + '\n' + '\n' + entrytup[0])
    else:
        bot.send_message(message.chat.id, 'There are no entries with such heading, please try again')
        

def deleting(message):
    global date
    global name 
    global signedin
    date = message.text.strip()
    diary = sqlite3.connect(name + '.db')
    curs = diary.cursor()
    exists = curs.execute("SELECT * FROM entries WHERE date = '%s'" % date).fetchall()
    diary.commit()
    if exists:
        curs.execute("DELETE FROM entries WHERE date = '%s'" % date)
        diary.commit()
        curs.close()
        diary.close()
        bot.send_message(message.chat.id, 'The entry has successfully been deleted')
    else:
        curs.close()
        diary.close()
        bot.send_message(message.chat.id, 'There are no entries with such heading, maybe it has already been deleted')


def exporting(message):
    global date
    global name
    global signedin
    date = message.text.strip()
    diary = sqlite3.connect(name + '.db')
    curs = diary.cursor()
    exists = curs.execute("SELECT * FROM entries WHERE date = '%s'" % date).fetchall()
    diary.commit()
    if exists:
        entrytup = curs.execute("SELECT entry FROM entries WHERE date = '%s'" % date).fetchone()
        diary.commit()
        curs.close()
        diary.close()
        expfile = date + '\n' + '\n' + entrytup[0]
        my_file = open('export_note.txt', 'w+')
        my_file.write(expfile)
        my_file.close()
        bot.send_document(message.chat.id, open(r'export_note.txt', 'rb'))
    else:
        bot.send_message(message.chat.id, 'There are no entries with such heading, please try again')
