import telebot # библиотека telebot
from config import token # импорт токена
import random
import time
from datetime import datetime

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")



@bot.message_handler(func=lambda message: True)
def ban_user(message):
    if 'https://' in message.text: 
        user_id = message.from_user.id
        chat_id = message.chat.id 
        user_stat = bot.get_chat_member(chat_id, user_id).status
        if user_stat == 'administrator' or user_stat == 'creator':
            bot.reply_to(message, 'unable to ban because the user is akbar')
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")


@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)


@bot.message_handler(commands=['dice'])
def roll_dice(message):
    dice_message = bot.send_dice(message.chat.id)
    time.sleep(4)
    result = dice_message.dice.value
    bot.reply_to(message, f"Выпало число: **{result}**!")


# 6. Хендлер для команды /coin (Монетка)
@bot.message_handler(commands=['coin'])
def flip_coin(message):
    result = random.choice(["Орел", "Решка"])
    bot.reply_to(message, f"Монетка подброшена... Выпало: **{result}**!")


# 7. Хендлер для команды /time
@bot.message_handler(commands=['time'])
def get_time(message):
    current_time = datetime.now().strftime("%H:%M:%S")
    bot.reply_to(message, f"Текущее время: **{current_time}**")


bot.infinity_polling(none_stop=True)
