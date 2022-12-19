import telebot
from telebot import types
import random

def buttons(buttons):
    mark = types.ReplyKeyboardRemove()
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark.row(buttons)
    return mark

def newgamebuttons(candys, score):
    if score['tab'] < 28:
        candys = score['tab']
    ib1 = types.InlineKeyboardButton('-', callback_data='-')
    ib2 = types.InlineKeyboardButton(candys, callback_data=candys)
    ib3 = types.InlineKeyboardButton('+', callback_data='+')
    ib4 = types.InlineKeyboardButton('Взять', callback_data='take')
    mark = types.InlineKeyboardMarkup()
    mark.row(ib1, ib2, ib3)
    mark.row(ib4)
    return mark

def showscore(score):
    res = 'СЧЕТ:\n\nИгрок - ' + str(score['player']) + '\nНа столе - ' + str(score['tab']) + '\nБот - ' + str(score['bot'])
    return res

def botstep(score):
    if score['tab'] <= 28:
        take = score['tab']
    else:
        take = random.randint(1, 28)
    score['bot'] = score['bot'] + take + score['player']
    score['tab'] = score['tab'] - take
    score['player'] = 0
    return score