import telebot, functions, random, time
bot = telebot.TeleBot('5891684002:AAF9GzovRLlRapruKpGQLvFxoVGVeuwgB4I')

score = {
    'player': 0,
    'tab': 0,
    'bot': 0
}
firststep = 0
lasttake = 28
curmes = ''
mainscore = {
    'player': 0,
    'bot': 0
}

def final():
    global lasttake, score, curmes, mainscore
    if score['bot'] == 0:
        mainscore['player'] += 1
        res =  f'ПОЗДРАВЛЯЮ!\nВы выйграли\n\nИгрок  Бот\n{str(mainscore["player"]).ljust(6)}{str(mainscore["bot"]).ljust(6)}'
    elif score['player'] == 0:
        mainscore['bot'] += 1
        res =  f'УВЫ!\nБот выйграл\n\nИгрок  Бот\n{str(mainscore["player"]).ljust(6)}{str(mainscore["bot"]).ljust(6)}'
    return res

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global firststep
    mark = functions.buttons('Новая игра')
    bot.send_message(message.chat.id, 'Добро пожаловать в CANDYS')
    bot.send_message(message.chat.id, 'ПРАВИЛА ИГРЫ:\n\n'+
                     'На столе лежит 117 конфет\n'+
                     'Игрок или бот делая ход, забирает определенное количество конфет (от 1 до 28).\n'+
                     'При этом все конфеты соперника переходят к ходящему.\n'+
                     'Побеждает тот кто делает последний ход.\n Нажмите [Новая игра]...', reply_markup=mark)
    bot.register_next_step_handler(message, newgame)

@bot.message_handler(content_types=['text'])
def newgame(message):
    global score, firststep, lasttake, curmes
    if message.text == 'Новая игра':
        score = {
            'player': 0,
            'tab': 117,
            'bot': 0
        }
        firststep = random.randint(1, 2)
        curmes = bot.send_message(message.chat.id, functions.showscore(score), reply_markup=functions.newgamebuttons(lasttake, score))
        if firststep == 2:
            bot.send_message(message.chat.id, 'Бот делает первый ход')
            score = functions.botstep(score)
            time.sleep(2)
            bot.edit_message_text(chat_id = message.chat.id, message_id = curmes.id, text = functions.showscore(score), reply_markup=functions.newgamebuttons(lasttake, score))

@bot.callback_query_handler(func=lambda call: True)

def playerstep(call):
    global lasttake, score, curmes, mainscore
    if score['tab'] > 0:
        if score['tab'] < 28:
            maxcandys = int(score['tab'])
        else:
            maxcandys = 28
        if call.data == '+':
            if lasttake < maxcandys:
                lasttake += 1
            else:
                lasttake = 1
            bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = curmes.id, reply_markup = functions.newgamebuttons(lasttake, score))
        elif call.data == '-':
            if lasttake > 1:
                lasttake -= 1
            else:
                lasttake = maxcandys
            bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = curmes.id, reply_markup = functions.newgamebuttons(lasttake, score))
        elif call.data == 'take':
            print(f'{score}  -  i take {lasttake} candys')
            score['tab'] -= lasttake
            score['player'] += lasttake + score['bot']
            score['bot'] = 0
            if score['tab'] > 0:
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = curmes.id, text = functions.showscore(score), reply_markup = functions.newgamebuttons(lasttake, score))
                score = functions.botstep(score)
                time.sleep(1)
                if score['tab'] > 0:
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = curmes.id, text = functions.showscore(score), reply_markup = functions.newgamebuttons(lasttake, score))
                else:
                    bot.delete_message(chat_id = call.message.chat.id, message_id = curmes.id)
                    bot.send_message(call.message.chat.id, functions.showscore(score), reply_markup = '')
                    bot.send_message(call.message.chat.id, f'{final()}\nНачните новую игру.', reply_markup = functions.buttons('Новая игра'))
                    bot.register_next_step_handler(call.message, newgame)
            if score['tab'] == 0:
                bot.delete_message(chat_id = call.message.chat.id, message_id = curmes.id)
                bot.send_message(call.message.chat.id, functions.showscore(score), reply_markup = '')
                bot.send_message(call.message.chat.id, f'{final()}\nНачните новую игру.', reply_markup = functions.buttons('Новая игра'))
                bot.register_next_step_handler(call.message, newgame)


bot.polling(none_stop=True, interval=0)